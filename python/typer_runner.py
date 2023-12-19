from typing import Optional

import typer

from api_client import ImagenAPIClient

app = typer.Typer()


@app.command()
def run(
        input_dir: str = typer.Option(..., "--input_dir", help="Path to the input directory"),
        output_dir: str = typer.Option(..., "--output_dir", help="Path to the output directory"),
        profile_name: str = typer.Option(..., "--profile_name", help="Name of the profile"),
        api_key: Optional[str] = typer.Option(None, "--api_key", help="API key"),
        callback_url: Optional[str] = typer.Option(None, "--callback_url", help="Callback url")
):
    """
    This script processes images using the Imagen AI API. It allows users to specify input and output directories,
    profile name, API key, and an optional callback URL. It handles the uploading, editing, and downloading of images.

        Usage examples: python your_script.py --input_dir=./images --output_dir=./output --profile_name="default"
        --api_key="yourapikey" python your_script.py --input_dir=./images --output_dir=./output
        --profile_name="default" --api_key="yourapikey" --callback_url="http://example.com/callback"

    """
    if not profile_name:
        typer.echo("Error: Profile name is required.")
        raise typer.Abort()

    imagen_client = ImagenAPIClient(input_dir=input_dir, output_dir=output_dir, api_key=api_key)

    # Get profile key
    profile_key = imagen_client.get_profile_key(profile_name=profile_name)

    # Create project
    project_uuid = imagen_client.create_project()

    # Upload all images
    imagen_client.upload_images(project_uuid=project_uuid)

    # Send project for editing
    imagen_client.send_project_for_edit(project_uuid=project_uuid, profile_key=profile_key, callback_url=callback_url)

    # Wait until project status is completed
    imagen_client.wait_for_project_to_complete(project_uuid=project_uuid)

    # Download all the artifacts
    imagen_client.download_artifacts(project_uuid=project_uuid)

    typer.echo("Processing completed successfully.")


if __name__ == "__main__":
    app()
