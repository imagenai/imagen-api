import argparse
import os.path
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List
from typing import Optional

import requests
from retry import retry
from tqdm import tqdm

MAX_WORKERS = int(os.environ.get('MAX_WORKERS', 10))


class MissingAPIKeyException(Exception):
    pass


class MissingProfileDetailsException(Exception):
    pass


class InvalidProfileNameException(Exception):
    pass


class ImagenAPIClient:
    STATUS_COMPLETED = 'Completed'
    STATUS_FAILED = 'Failed'
    CHECK_STATUS_INTERVAL = 30  # seconds

    def __init__(self, input_dir: str, output_dir: str, api_key: str):
        if not api_key:
            raise MissingAPIKeyException
        api_key = api_key if api_key else os.environ.get('API_KEY')
        self.api_key = api_key
        self.headers = {'x-api-key': self.api_key}
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.project_uuid = None
        self.base_url = 'https://api-beta.imagen-ai.com/v1'

    def get_profile_key(self, profile_name: str):
        """
        Retrieves the profile key for a given profile name.

        Args:
            profile_name (str): Name of the profile to fetch the key for.

        Returns:
            str: The profile key corresponding to the given profile name.

        Raises:
            InvalidProfileNameException: If the profile name is not found.
        """
        response = requests.get(os.path.join(self.base_url, 'profiles'), headers=self.headers)
        response.raise_for_status()
        profiles = response.json()['data']['profiles']
        for profile in profiles:
            if profile['profile_name'] == profile_name:
                return profile['profile_key']
        raise InvalidProfileNameException(f'Profile {profile_name} not found!')

    def create_project(self) -> str:
        """
        Creates a new project and returns its UUID.

        Returns:
            str: The UUID of the newly created project.
        """
        response = requests.post(os.path.join(self.base_url, 'projects/'), headers=self.headers)
        response.raise_for_status()
        return response.json()['data']['project_uuid']

    def send_project_for_edit(self, project_uuid: str, profile_key: str, crop: bool = False, straighten: bool = False,
                              subject_mask: bool = False, hdr_merge: bool = False):
        """
        Sends a project for editing with the specified parameters.

        Args:
            project_uuid (str): The UUID of the project.
            profile_key (str): The profile key.
            crop (bool): Whether to crop the image.
            straighten (bool): Whether to straighten the image.
            subject_mask (bool): Whether to apply a subject mask.
            hdr_merge (bool): Whether to apply HDR merge.

        Returns:
            None
        """
        response = requests.post(os.path.join(self.base_url, 'projects', project_uuid, 'edit'),
                                 headers=self.headers,
                                 json={'crop': crop, "straighten": straighten,
                                       'subject_mask': subject_mask,
                                       'profile_key': profile_key,
                                       'hdr_merge': hdr_merge})
        response.raise_for_status()

    @retry(exceptions=Exception, tries=3)
    def _upload_image(self, file_upload_details: Dict):
        upload_link = file_upload_details['upload_link']
        file_name = file_upload_details['file_name']
        headers = {}
        with open(os.path.join(self.input_dir, file_name), 'rb') as f:
            resp = requests.put(upload_link, data=f.read(), headers=headers)
            resp.raise_for_status()

    def get_upload_links(self, project_uuid: str) -> List[str]:
        """
        Retrieves temporary upload links for files in the input directory.

        Args:
            project_uuid (str): The UUID of the project to get upload links for.

        Returns:
            list: A list of dictionaries containing file names and their respective upload links.
        """
        files = []
        for file_path in os.listdir(self.input_dir):
            file_data = {'file_name': os.path.basename(file_path)}
            files.append(file_data)
        response = requests.post(os.path.join(self.base_url, f'projects/{project_uuid}/get_temporary_upload_links'),
                                 json={'files_list': files}, headers=self.headers)
        response.raise_for_status()
        return response.json()['data']['files_list']

    def upload_images(self, files_upload_link: List[str]):
        """
        Uploads images to the provided upload links.

        Args:
            files_upload_link (list): A list of dictionaries containing file names and their respective upload links.

        Returns:
            None
        """
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            list(tqdm(executor.map(self._upload_image, files_upload_link), total=len(files_upload_link)))

    def get_project_status(self, project_uuid):
        try:
            response = requests.get(
                os.path.join(self.base_url, 'projects', project_uuid, 'edit', 'status'),
                headers=self.headers
            )
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code.
            return response.json()['data']['status']
        except requests.RequestException as e:
            raise Exception(f'Error fetching project status: {e}')

    def wait_for_project_to_complete(self, project_uuid: str):
        """
        Retrieves the current status of a project.

        Args:
            project_uuid (str): The UUID of the project.

        Returns:
            str: The current status of the project.
        """
        status = self.get_project_status(project_uuid)
        while status != self.STATUS_COMPLETED:
            if status == self.STATUS_FAILED:
                raise Exception('Project failed!')

            time.sleep(self.CHECK_STATUS_INTERVAL)
            status = self.get_project_status(project_uuid)
            print(f'Status = {status}')

        print(f'Project {project_uuid} edit status is completed')

    @retry(exceptions=Exception, tries=3)
    def _download_artifact(self, file_info: Dict):
        response = requests.get(file_info["download_link"])
        response.raise_for_status()  # Ensure we got a 200 OK response

        # Save content to local file
        with open(os.path.join(self.output_dir, file_info["file_name"]), "wb") as file:
            file.write(response.content)

    def download_artifacts(self, project_uuid: str):
        """
        Downloads all artifacts for a completed project.

        Args:
            project_uuid (str): The UUID of the project.

        Returns:
            None
        """
        response = requests.get(
            os.path.join(self.base_url, 'projects', project_uuid, 'edit', 'get_temporary_download_links'),
            headers=self.headers)
        response.raise_for_status()
        files_download_info = response.json()['data']['files_list']
        os.makedirs(self.output_dir, exist_ok=True)
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            list(tqdm(executor.map(self._download_artifact, files_download_info), total=len(files_download_info)))


def run(input_dir: str, output_dir: str, profile_key: Optional[str] = None, profile_name: Optional[str] = None,
        api_key: Optional[str] = None):
    if not profile_key and not profile_name:
        raise MissingAPIKeyException
    imagen_client = ImagenAPIClient(input_dir=input_dir, output_dir=output_dir,
                                    api_key=api_key)
    # Get profile key
    if not profile_key:
        profile_key = imagen_client.get_profile_key(profile_name=profile_name)
    # Create project
    project_uuid = imagen_client.create_project()
    # Get upload links
    files_upload_link = imagen_client.get_upload_links(project_uuid=project_uuid)
    # Upload all images
    imagen_client.upload_images(files_upload_link=files_upload_link)
    # Send project for editing
    imagen_client.send_project_for_edit(project_uuid=project_uuid, profile_key=profile_key)
    # Wait until project status is completed
    imagen_client.wait_for_project_to_complete(project_uuid=project_uuid)
    # Download all the artifacts
    imagen_client.download_artifacts(project_uuid=project_uuid)


# Running the function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some paths and a profile name.")

    parser.add_argument('--input_dir', type=str, required=True, help='Path to the input directory')
    parser.add_argument('--output_dir', type=str, required=True, help='Path to the output directory')
    parser.add_argument('--profile_name', type=str, required=True, help='Name of the profile')
    parser.add_argument('--api_key', type=str, required=False, help='API key')

    args = parser.parse_args()

    run(input_dir=args.input_dir, output_dir=args.output_dir, profile_name=args.profile_name,
        api_key=args.api_key)
