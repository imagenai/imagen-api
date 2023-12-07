# Imagen API Client

## Description

This Python script provides an interface to interact with the Imagen API, designed for efficient image processing and
manipulation. It handles concurrent requests and includes robust error handling features.

## Installation

To use the Imagen API Client, follow these steps:

1. Clone the repository:
   ```
   git clone git@github.com:imagenai/imagen-api.git
   ```
2. Install required dependencies from the `requirements.txt` file:
   ```
   pip install -r requirements.txt
   ```

## Usage
To use this script:
1. Provide the necessary input and output directory paths.
2. Specify the profile name or profile key if available.
3. Call the `run` function with the required parameters.

Run the script from the command line, providing necessary arguments:

```
python api_client.py --input-dir [input directory] --output-dir [output directory] --api-key [your API key]
```

## API Key

To use this script, you need an API key from Imagen. Obtain your key by getting in touch with Imagen
at [amit.shuster@imagen-ai.com](mailto:amit.shuster@imagen-ai.com) and either pass it as a command line argument or set it as an
environment variable `API_KEY`.

## Error Handling

The script includes custom exceptions for missing API keys and invalid inputs, ensuring reliable operation.

## Understanding the  Data Flow

The script follows a specific sequence of operations to achieve its functionality:

1. **Initialization:**
   - The `ImagenAPIClient` is initialized with input and output directories, as well as an API key for authentication.

2. **Profile Key Retrieval:**
   - The `get_profile_key` method fetches the profile key associated with a given profile name.

3. **Project Creation:**
   - A new project is created using the `create_project` method, which returns a project UUID.

4. **Upload Links Generation:**
   - The `get_upload_links` method is called to generate temporary upload links for the images stored in the input directory.

5. **Image Upload:**
   - Images are uploaded to the provided links using the `upload_images` method.

6. **Project Editing:**
   - The `send_project_for_edit` method sends the project for editing based on specified parameters like crop, straighten, etc.

7. **Status Monitoring:**
   - The script continuously checks the project's status using `get_project_status` until the project is completed.

8. **Downloading Artifacts:**
   - Once the project is completed, the `download_artifacts` method downloads the processed images to the output directory.


## Dependencies
- `requests` for making API calls.
- `concurrent.futures` for handling concurrent uploads and downloads.
- `tqdm` for progress bars in console output.
- `retry` for retrying failed operations.

## Authors
Idan Dagan & Shahar Polak 


## Contributing

Contributions to the Imagen API Client are welcome. Please fork the repository, make your changes, and submit a pull
request.


