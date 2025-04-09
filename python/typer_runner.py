import os

import typer
from InquirerPy import prompt, inquirer

from api_client import run

app = typer.Typer()


def get_folder_path(message: str) -> str:
    return inquirer.text(
        message=message,
        validate=lambda input_dir: os.path.isdir(input_dir.replace("\ ", " ").strip()),
    ).execute()


def get_input(prompt_message: str) -> str:
    return inquirer.text(message=prompt_message).execute()


def get_boolean_choice(parameter_name: str):
    questions = [
        {
            "type": "list",
            "name": "choice",
            "message": f"Do you want to {parameter_name}?",
            "choices": ["Yes", "No"],
        },
    ]
    answers = prompt(questions)
    return answers['choice'] == "Yes"


@app.command()
def run_typer():
    """
    Execute the Imagen AI Image Processing Script. This script interfaces with the Imagen AI API to facilitate the
    processing of images. It requires inputs such as the directories for the source and destination of images,
    profile information, and API credentials. It supports various image processing options like HDR merging, cropping,
    straightening, and subject masking. Additionally, it provides an export feature.

    Usage Example:
    python your_script.py --input_dir=./images --output_dir=./output --profile_name="default" --api_key="yourapikey"
    python your_script.py --input_dir=./images --output_dir=./output --profile_name="default" --api_key="yourapikey" --callback_url="http://example.com/callback"
    """

    # Request user inputs for directories, profile, and API key
    input_dir = get_folder_path("Enter the directory (absolute path) for input images (Mandatory): ").replace("\ ",
                                                                                                              " ").strip()
    output_dir = get_folder_path("Enter the directory (absolute path) for processed images (Mandatory): ").replace("\ ",
                                                                                                                   " ").strip()

    profile_key = get_input("Enter your profile key:  ")
    api_key = get_input("Enter your unique API Key (Mandatory): ")

    callback_url = get_input("Enter your callback URL (Optional): ")

    # Inquire about image processing preferences
    hdr_merge = get_boolean_choice("Enable HDR Merge: ")
    crop = get_boolean_choice("Enable Cropping: ")
    straighten = get_boolean_choice("Enable Straightening: ")
    subject_mask = get_boolean_choice("Enable Subject Masking: ")
    smooth_skin = get_boolean_choice("Enable Smooth Skin: ")
    window_pull = get_boolean_choice("Enable Window Pull: ")
    sky_replacement = get_boolean_choice("Enable Sky Replacement: ")
    sky_replacement_template_id = None
    if sky_replacement:
        sky_replacement_template_id = int(get_input("Enter the Sky Template ID: [1-3] "))

    export = get_boolean_choice("Enable Export: ")

    # Execute the main processing function with the provided parameters
    run(input_dir=input_dir, output_dir=output_dir,
        profile_key=profile_key, profile_name=profile_name, api_key=api_key, callback_url=callback_url,
        hdr_merge=hdr_merge, crop=crop, straighten=straighten, subject_mask=subject_mask, smooth_skin=smooth_skin,
        window_pull=window_pull,
        sky_replacement=sky_replacement, sky_replacement_template_id=sky_replacement_template_id,
        export=export)


if __name__ == "__main__":
    app()
