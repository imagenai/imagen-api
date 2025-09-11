# Imagen API


Imagen is an AI-powered solution that eliminates hours of busy work from post-production for professional photographers. Imagen API streamlines and automates the photographer’s post-production editing workflow, similar to the Imagen app.

This Imagen API project gives you the tools and components to jumpstart your development with the Imagen API, including a Python package with sample code for a client and a Postman collection to test the endpoints.


## Set up the Imagen API project

1. Clone the repository:

```bash
git clone git@github.com:imagenai/imagen-api.git
```

2. Navigate to the directory you need.  
     
   For the Python client, go to:

```bash
cd python
```

   For the Postman collection, go to:

```bash
cd postman
```

## Python sample code 

The `/python` directory contains the Python package for the Imagen API Client. It includes scripts and instructions for using the Imagen API with Python. See `README.MD` for details and examples of using the script to run the Imagen API Client.

## Postman 

Inside the `/postman` directory, there is a Postman collection with HTTP requests for getting profile keys, creating projects, uploading files, editing photos, and exporting edited photos.

> When testing in Postman, disable `Content-Type` in the request headers.


1. Import `postman/imagen-api.postman_collection.json` into Postman.  
     
2. Set the `API_BASE_URL` to `https://api.imagen.ai/v1`.  
     
3. Set the `API_KEY` with the key you received from Imagen.  
     
4. Read the docs in the next section to get started testing endpoints. 

## Read the docs 

| Link to doc | Description |
| :---- | :---- |
| [How-tos and full workflow](https://support.imagen-ai.com/hc/en-us/articles/19137253415965-Automate-your-post-production-workflow-with-Imagen-API) | Step-by-step guide to use the Imagen API with code examples |
| [Reference](https://api-beta.imagen-ai.com/v1/redoc) | Imagen API reference documentation for each endpoint |
| [Imagen help center](https://support.imagen-ai.com/hc/en-us) | In-depth guides, FAQs, tutorials, and everything about Imagen |

## License 

The Imagen API project is licensed under the Apache License 2.0. For more details on the terms and conditions, see `LICENSE.txt` in the `main` directory.
