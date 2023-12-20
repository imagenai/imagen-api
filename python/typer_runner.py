from typing import Optional

import typer

from api_client import ImagenAPIClient, MissingAPIKeyException

app = typer.Typer()


@app.command()
def run_gui(
        input_dir: str,
        output_dir: str,
        profile_name: Optional[str] = None,
        api_key: Optional[str] = None,
        callback_url: Optional[str] = None,
        profile_key: Optional[str] = None,
        hdr_merge: bool = False,
        crop: bool = False,
        straighten: bool = False,
        subject_mask: bool = False,
        export: bool = False
):
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
                                        subject_mask=subject_mask)

    # Wait until project status is completed
    imagen_client.wait_for_project_edit_to_complete(project_uuid=project_uuid)

    # Download all the artifacts
    if export:
        imagen_client.send_project_for_export(project_uuid=project_uuid)
        imagen_client.wait_for_project_export_to_complete(project_uuid=project_uuid)
        imagen_client.download_exported_files(project_uuid=project_uuid)
    else:
        imagen_client.download_edited_files(project_uuid=project_uuid)


@app.command()
def run(
        input_dir: str = typer.Option(..., "--input_dir", help="Path to the input directory",
                                      prompt="Please insert your image for editing folder name/location"),
        output_dir: str = typer.Option(..., "--output_dir", help="Path to the output directory",
                                       prompt="Please insert your image edited output folder name/location"),
        profile_name: Optional[str] = typer.Option(None, "--profile_name", help="Name of the profile",
                                                   prompt="Please insert your profile project name"),
        api_key: Optional[str] = typer.Option(None, "--api_key", help="API key",
                                              prompt="Please insert your unique API Key"),
        callback_url: Optional[str] = typer.Option(None, "--callback_url", help="Callback URL"),
        profile_key: Optional[str] = typer.Option(None, "--profile_key", help="The key of the profile"),
        hdr_merge: bool = typer.Option(False, "--hdr_merge", help="Use HDR merge"),
        crop: bool = typer.Option(False, "--crop", help="Use crop"),
        straighten: bool = typer.Option(False, "--straighten", help="Use straighten"),
        subject_mask: bool = typer.Option(False, "--subject_mask", help="Use subject mask"),
        export: bool = typer.Option(False, "--export", help="Export to jpg")):
    """
    This script processes images using the Imagen AI API. It allows users to specify input and output directories,
    profile name, API key, and an optional callback URL. It handles the uploading, editing, and downloading of images.

        Usage examples: python your_script.py --input_dir=./images --output_dir=./output --profile_name="default"
        --api_key="yourapikey" python your_script.py --input_dir=./images --output_dir=./output
        --profile_name="default" --api_key="yourapikey" --callback_url="http://example.com/callback"

    """
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
                                        subject_mask=subject_mask)

    # Wait until project status is completed
    imagen_client.wait_for_project_edit_to_complete(project_uuid=project_uuid)

    # Download all the artifacts
    if export:
        imagen_client.send_project_for_export(project_uuid=project_uuid)
        imagen_client.wait_for_project_export_to_complete(project_uuid=project_uuid)
        imagen_client.download_exported_files(project_uuid=project_uuid)
    else:
        imagen_client.download_edited_files(project_uuid=project_uuid)


if __name__ == "__main__":
    app()
