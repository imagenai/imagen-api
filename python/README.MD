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

## Contributing

Contributions to the Imagen API Client are welcome. Please fork the repository, make your changes, and submit a pull
request.


