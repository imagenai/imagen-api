import argparse
import logging
import os.path
import time
from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus
from typing import Dict
from typing import List
from typing import Optional

import requests
from requests import Response
from retry import retry
from tqdm import tqdm

MAX_WORKERS = int(os.environ.get('MAX_WORKERS', 10))


class MissingAPIKeyException(Exception):
    pass


class MissingProfileDetailsException(Exception):
    pass


class InvalidProfileNameException(Exception):
    pass


class InvalidAPIKey(Exception):
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
        self.base_url = 'https://api-beta.imagen-ai.com/v1/'

    def get_profile_key(self, profile_name: str):
        response = requests.get(os.path.join(self.base_url, 'profiles'), headers=self.headers)
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise InvalidAPIKey('API key does not have permissions.')
        response.raise_for_status()
        profiles = response.json()['data']['profiles']
        for profile in profiles:
            if profile['profile_name'] == profile_name:
                return profile['profile_key']
        raise InvalidProfileNameException(f'Profile {profile_name} not found!')

    def create_project(self) -> str:
        response = requests.post(os.path.join(self.base_url, 'projects/'), headers=self.headers)
        if response.status_code >= 400:
            logging.getLogger().error(response.json())
        response.raise_for_status()
        return response.json()['data']['project_uuid']

    def send_project_for_edit(self, project_uuid: str, profile_key: str, crop: bool = False, straighten: bool = False,
                              subject_mask: bool = False, hdr_merge: bool = False, smooth_skin: bool = False,
                              callback_url: Optional[str] = None, perspective_correction: bool = False):
        response = requests.post(os.path.join(self.base_url, f'projects/{project_uuid}/edit'),
                                 headers=self.headers,
                                 json={'crop': crop, "straighten": straighten,
                                       'subject_mask': subject_mask,
                                       'profile_key': profile_key,
                                       'callback_url': callback_url,
                                       'hdr_merge': hdr_merge,
                                       'smooth_skin': smooth_skin,
                                       'perspective_correction': perspective_correction})
        if response.status_code >= 400:
            logging.getLogger().error(response.json())
        response.raise_for_status()

    @retry(exceptions=Exception, tries=3)
    def _upload_image(self, file_upload_details: Dict):
        upload_link = file_upload_details['upload_link']
        file_name = file_upload_details['file_name']
        headers = {}
        with open(os.path.join(self.input_dir, file_name), 'rb') as f:
            resp = requests.put(upload_link, data=f.read(), headers=headers)
            resp.raise_for_status()

    def upload_images(self, project_uuid: str):
        files = []
        for file_name in os.listdir(self.input_dir):
            if not os.path.isfile(os.path.join(self.input_dir, file_name)):
                print(f'Skipping {file_name}. not a valid file.')
                continue
            if file_name.startswith('.'):
                print(f'Skipping hidden file {file_name}')
                continue
            file_data = {'file_name': file_name}
            files.append(file_data)
        all_files_data = self.get_temporary_upload_links(project_uuid=project_uuid, files=files)
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            list(tqdm(executor.map(self._upload_image, all_files_data), total=len(all_files_data)))

    @retry(exceptions=Exception, tries=5, backoff=5)
    def get_project_status(self, project_uuid: str, is_export: bool = False):
        operation = 'export' if is_export else 'edit'
        try:
            response = requests.get(os.path.join(self.base_url, f'projects/{project_uuid}/{operation}/status'),
                                    headers=self.headers)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code.
            return response.json()['data']['status']
        except requests.RequestException as e:
            raise Exception(f'Error fetching project {operation} status: {e}')

    def wait_for_project_edit_to_complete(self, project_uuid: str):
        status = self.get_project_status(project_uuid)
        while status != self.STATUS_COMPLETED:
            if status == self.STATUS_FAILED:
                raise Exception('Project edit failed!')

            time.sleep(self.CHECK_STATUS_INTERVAL)
            status = self.get_project_status(project_uuid)
            print(f'Project edit status : {status}')

        print(f'Project {project_uuid} edit has completed successfully.')

    def wait_for_project_export_to_complete(self, project_uuid: str):
        status = self.get_project_status(project_uuid, is_export=True)
        while status != self.STATUS_COMPLETED:
            if status == self.STATUS_FAILED:
                raise Exception('Project export failed!')

            time.sleep(self.CHECK_STATUS_INTERVAL)
            status = self.get_project_status(project_uuid, is_export=True)
            print(f'Project export status : {status}')

        print(f'Project {project_uuid} export has completed successfully.')

    def send_project_for_export(self, project_uuid: str):
        response = requests.post(os.path.join(self.base_url, f'projects/{project_uuid}/export'), headers=self.headers)
        response.raise_for_status()

    @retry(exceptions=Exception, tries=3)
    def _download_artifact(self, file_info: Dict):
        response = requests.get(file_info["download_link"])
        response.raise_for_status()  # Ensure we got a 200 OK response

        # Save content to local file
        with open(os.path.join(self.output_dir, file_info["file_name"]), "wb") as file:
            file.write(response.content)

    def get_error_message(self, response: Response):
        return response.json()['error']['message']

    def get_temporary_upload_links(self, files: List[Dict], project_uuid: str):
        response = requests.post(os.path.join(self.base_url, f'projects/{project_uuid}/get_temporary_upload_links'),
                                 json={'files_list': files}, headers=self.headers)
        if response.status_code != HTTPStatus.OK:
            error_msg = self.get_error_message(response)
            print(f"Failed get temporary upload links. {error_msg}")
            raise Exception(error_msg)
        all_files_data = response.json()['data']['files_list']
        return all_files_data

    def get_temporary_download_links(self, project_uuid: str, is_export: bool = False):
        operation = 'export' if is_export else 'edit'
        response = requests.get(
            os.path.join(self.base_url, f'projects/{project_uuid}/{operation}/get_temporary_download_links'),
            headers=self.headers)
        if response.status_code != HTTPStatus.OK:
            error_msg = self.get_error_message(response)
            print(f"Failed get temporary download links. {error_msg}")
            raise Exception(error_msg)
        return response.json()['data']['files_list']

    def download_edited_files(self, project_uuid: str):
        files_download_info = self.get_temporary_download_links(project_uuid=project_uuid)
        os.makedirs(self.output_dir, exist_ok=True)
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            list(tqdm(executor.map(self._download_artifact, files_download_info), total=len(files_download_info)))

    def download_exported_files(self, project_uuid: str):
        files_download_info = self.get_temporary_download_links(project_uuid=project_uuid, is_export=True)
        os.makedirs(self.output_dir, exist_ok=True)
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            list(tqdm(executor.map(self._download_artifact, files_download_info), total=len(files_download_info)))


def run(input_dir: str, output_dir: str, profile_key: Optional[str] = None, profile_name: Optional[str] = None,
        api_key: Optional[str] = None, callback_url: Optional[str] = None, hdr_merge: Optional[bool] = False,
        smooth_skin: Optional[bool] = False,
        crop: Optional[bool] = False, straighten: Optional[bool] = False,
        subject_mask: Optional[bool] = False, export: Optional[bool] = False,
        perspective_correction: Optional[bool] = False):
    if not profile_key and not profile_name:
        raise MissingAPIKeyException
    imagen_client = ImagenAPIClient(input_dir=input_dir, output_dir=output_dir,
                                    api_key=api_key)
    # Get profile key
    if not profile_key:
        profile_key = imagen_client.get_profile_key(profile_name=profile_name)
    # Create project
    project_uuid = imagen_client.create_project()
    # Upload all images
    imagen_client.upload_images(project_uuid=project_uuid)
    # Send project for editing
    imagen_client.send_project_for_edit(project_uuid=project_uuid, profile_key=profile_key,
                                        callback_url=callback_url, hdr_merge=hdr_merge, crop=crop,
                                        straighten=straighten,
                                        subject_mask=subject_mask,
                                        smooth_skin=smooth_skin,
                                        perspective_correction=perspective_correction)
    # Wait until project status is completed
    imagen_client.wait_for_project_edit_to_complete(project_uuid=project_uuid)
    # Download all the artifacts
    if export:
        imagen_client.send_project_for_export(project_uuid=project_uuid)
        imagen_client.wait_for_project_export_to_complete(project_uuid=project_uuid)
        imagen_client.download_exported_files(project_uuid=project_uuid)
    else:
        imagen_client.download_edited_files(project_uuid=project_uuid)


# Running the function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some paths and a profile name.")

    parser.add_argument('--input_dir', type=str, required=True, help='Path to the input directory')
    parser.add_argument('--output_dir', type=str, required=True, help='Path to the output directory')
    parser.add_argument('--profile_name', type=str, required=False, help='Name of the profile')
    parser.add_argument('--api_key', type=str, required=False, help='API key')
    parser.add_argument('--callback_url', type=str, required=False, help='Callback url', default=None)
    parser.add_argument('--profile_key', type=str, required=False, help='The key of the profile')
    parser.add_argument('--hdr_merge', action='store_true', help='Do you want use hdr merge?')
    parser.add_argument('--crop', action='store_true', help='Do you want to use crop?')
    parser.add_argument('--straighten', action='store_true', help='Do you want to use straighten?')
    parser.add_argument('--subject_mask', action='store_true', help='Do you want to use subject_mask?')
    parser.add_argument('--export', action='store_true', help='Whether to export to jpg or not')
    parser.add_argument('--smooth_skin', action='store_true', help='Enable smooth skin?')
    parser.add_argument('--perspective_correction', action='store_true', help='Enable perspective correction?')

    args = parser.parse_args()

    run(input_dir=args.input_dir, output_dir=args.output_dir, profile_name=args.profile_name,
        api_key=args.api_key, callback_url=args.callback_url, hdr_merge=args.hdr_merge, profile_key=args.profile_key,
        crop=args.crop, straighten=args.straighten, subject_mask=args.subject_mask, export=args.export,
        smooth_skin=args.smooth_skin, perspective_correction=args.perspective_correction)
