# Imagen API Python Client

## Description

This Python script provides an interface to interact with the Imagen API, designed for efficient image processing and manipulation. It handles concurrent requests and includes robust error handling features.

## Installation

To use the Imagen API Python Client, follow these steps:

1. Clone the repository (if not done already) and make sure you are in the `python` directory:
   ```
   git clone git@github.com:imagenai/imagen-api.git
   cd python
   ```
2. Install required dependencies from the `requirements.txt` file:
   ```
   python3 -m pip install -r requirements.txt
   ```

## Usage

Run the script from the command line, providing necessary arguments:

```
python3 api_client.py --input_dir [input directory] --output_dir [output directory] --api_key [your API key] --profile_name [name of a profile]
```

## API Key

To use this script, you need an API key from Imagen. Obtain your key by getting in touch with Imagen at [support@imagen-ai.com](mailto:support@imagen-ai.com), please specify that you are interested in the APIs and how many photos do you edit yearly. Then, either pass it as a command line argument or set it as an environment variable `API_KEY`.

## Error Handling

The script includes custom exceptions for missing API keys and invalid inputs, ensuring reliable operation.

## Contributing

Contributions to the Imagen API Client are welcome. Please fork the repository, make your changes, and submit a pull request.