# Edit, download, and export photos with Imagen API

## What is Imagen API?

Imagen API is an AI-powered solution that streamlines and automates post-production workflows for photographers. 
These are the main steps in the process:

1. **Edit photos** - Upload photos to edit them with an AI Profile and AI tools.
2. **Download edited files** - Download the edited photos.
3. **Export photos for delivery** - Export the edited photos in a project to JPEG format.

## Before you begin

Before editing photos with Imagen API, sign up for Imagen and ask the Imagen team for an API key. Also, learn how Imagen edits your photos and have a list of AI Profiles you want to use for editing.

Complete these steps:

1. [Sign up](https://support.imagen-ai.com/hc/en-us/articles/4938388678161-Where-and-how-do-I-signup) for Imagen.
2. Get an API key from the Imagen team. You’ll need the email address used to sign up for Imagen.
3. (Optional) For sample code in Python and a Postman collection, see the [Imagen API project](https://github.com/imagenai/imagen-api/tree/main) on GitHub.
4. Review the [Imagen API reference](https://api-beta.imagen-ai.com/v1/docs) docs.
5. Learn how Imagen edits photos in the Imagen app, or try the [API playground](https://account.imagen-ai.com/api-playground).
6. Check out different AI Profiles in the Profile Showcase, and choose one for editing. If you want to create a [Personal AI Profile](https://support.imagen-ai.com/hc/en-us/articles/6069763238289-Create-a-Personal-AI-Profile-Adobe-Lightroom-Classic), use the Imagen app.

## Get started

### Imagen base URL

The base URL for the Imagen API is [https://api-beta.imagen-ai.com/v1/](https://api-beta.imagen-ai.com/v1/).

### Authentication

Imagen API uses an API key for authentication. Add it as a header to your requests in text format. The header name is `x-api-key`.

Here is an example:

```
curl --location ‘https://api-beta.imagen-ai.com/v1/profiles/’ \
--header ‘x-api-key: <api_key>’ \
--header ‘Content-Type: application/json’ \
```

### Supported file formats for editing photos

Imagen API supports these file formats for editing photos:

* RAW (.nef, .cr2, .arw, .nrw, .crw, .srf, .sr2, .orf, .raw, .rw2, .raf, .ptx, .pef, .rwl, .srw, .cr3, .3fr, .fff)
* DNG
* JPEG

When Imagen returns the edited files, these are the respective formats:

| File format before edit | File format returned after edit |
| ----------------------- | ------------------------------- |
| RAW                     | XMP                             |
| DNG                     | DNG with embedded XMP           |
| JPEG                    | JPEG with embedded XMP          |
 
 
## Edit photos

### 1. Get a list of AI Profiles

Call GET `https://api-beta.imagen-ai.com/v1/profiles/` to get a list of AI Profiles available to edit your photos. 
The response includes the Personal AI Profiles you created in the Imagen app and all available Talent AI Profiles. Each AI Profile has a `profile_key` that identifies it. You will need this `profile_key` when sending photos to edit.

#### Response example

```
{
    "data": {
        "profiles": [
            {
                "profile_key": XXXXXX,
                "profile_name": "wedding",
                "profile_type": "Personal",
                "image_type": "RAW"
            },
            {
                "profile_key": XXXXXX,
                "profile_name": "wedding-lite-profile",
                "profile_type": "Personal",
                "image_type": "RAW"
            },
            {
                "profile_key": 14715,
                "profile_name": "LOVE & LIGHT",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 196,
                "profile_name": "WARM SKIN TONES",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 254,
                "profile_name": "BODY LANGUAGE",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 328,
                "profile_name": "BODY LANGUAGE - B&W",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 673,
                "profile_name": "SIMPLY SUBLIME",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 943,
                "profile_name": "TIMELESS COLOR",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 4042,
                "profile_name": "CALIFORNIA DREAMING",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 5699,
                "profile_name": "NATURAL FEELS",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 5700,
                "profile_name": "CLEAN & CRISP",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 5701,
                "profile_name": "TIERRA",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 9224,
                "profile_name": "CINEMATIC LUXURY",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 21427,
                "profile_name": "THE MODERN CLASSIC",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 21428,
                "profile_name": "SILVER FILM",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 29132,
                "profile_name": "MOMENTICOS",
                "profile_type": "Talent",
                "image_type": "JPG"
            },
            {
                "profile_key": 29133,
                "profile_name": "MOMENTICOS - B&W",
                "profile_type": "Talent",
                "image_type": "JPG"
            },
            {
                "profile_key": 35653,
                "profile_name": "LUXE COLOR",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 61725,
                "profile_name": "NATURAL LIGHT STUDIO",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 71025,
                "profile_name": "PEACHY BY PBX",
                "profile_type": "Talent",
                "image_type": "RAW"
            },
            {
                "profile_key": 163322,
                "profile_name": "ELEGANT HOME",
                "profile_type": "Talent",
                "image_type": "RAW"
            }
        ]
    }
}
```
### 2. Create a project

Call POST `https://api-beta.imagen-ai.com/v1/projects/` to create a project.
We recommend creating a project for each shoot. A project organizes your photos with the AI Profile you chose for editing these photos. 

The response is the `project_uuid` used to identify this project. Use this `project_uuid` until the end of this flow, where you export your photos to JPEG.

#### Response example

```
{
    "data": {
        "project_uuid": "<project_uuid>"
    }
}
```

### 3. Get temporary upload links to upload photos

Call POST `https://api-beta.imagen-ai.com/v1/projects/<PROJECT_UUID>/get_temporary_upload_links`.
In the request, include the photos to upload in the `files_list` param. Use `list` format.
The response includes a temporary link for each photo to Imagen’s S3 bucket on AWS. This link is the AWS presigned URL.

#### Request example

```
curl --location ‘https://api.dev.imagen-ai.com/v1/projects/<project_uuid>/get_temporary_upload_links’ \
--header ‘x-api-key: <api_key>’ \
--header ‘Content-Type: application/json’ \
--data ‘{
    “files_list”: [
        {“file_name”: “922A4846.raw”},
        {“file_name”: “922A4832.raw”},
        {“file_name”: “922A4818.raw”},
        {“file_name”: “922A4809.raw”}
    ]
}’
```

#### Response example

```
{
    "data": {
        "files_list": [
            {
                "file_name": "922A4846.raw",
                "upload_link": "<presigned URL for 922A4846.raw>"
            },
            {
                "file_name": "922A4832.raw",
                "upload_link": "<presigned URL for 922A4832.raw>"
            },
            {
                "file_name": "922A4818.raw",
                "upload_link": "<presigned URL for 922A4818.raw>"
            },
            {
                "file_name": "922A4809.raw",
                "upload_link": "<presigned URL for 922A4809.raw>"
            }
        ]
    }
}
```

### 4. Upload photos to Imagen’s S3 bucket on AWS

Upload photos to Imagen’s S3 bucket on AWS with the temporary upload links from the response in the previous step. Use any method you like. For sample code in Python, see `api_client.py` in the [Imagen API project](https://github.com/imagenai/imagen-api/tree/main) in GitHub.

For more information on uploading files with a presigned URL, see this [guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html) in the AWS documentation.

### 5. Send photos to edit 

Call POST `https://api-beta.imagen-ai.com/v1/projects/<PROJECT_UUID>/edit` to send the photos to edit with the AI Profile you chose.

In the request body, include the `profile_key` of the AI Profile you want to use. See the response from GET `https://api-beta.imagen-ai.com/v1/profiles/` to find the `profile_key` of your AI Profile. Also, include the AI tools you want to use.

#### Example of the request body

```
{
  "profile_key": <profile key>,
  "crop": false,
  "hdr_merge": false,
  "straighten": false,
  "subject_mask": false,
  "photography_type": "NO_TYPE",
  "callback_url": "string",
  "smooth_skin": false,
  "perspective_correction": false
}
```

The response is a message that the project was sent to edit successfully. If there is an error, contact Imagen for help.

### 6. Check the edit status

Call GET `https://api-beta.imagen-ai.com/v1/projects/<PROJECT_UUID>/edit/status` to get the current status of the editing process. 
Here are the statuses in the response:

* `PENDING` The photos haven’t been edited yet. Once you send the photos to edit, the status will change to `IN PROGRESS`.
* `IN PROGRESS` Imagen API is editing the photos as expected.
* `FAILED` Contact Imagen for help.
* `COMPLETED` Imagen API has finished editing the photos. Continue to download the edited photos.

## Download edited photos

### 1. Get temporary download links to download edited photos

After the edit status is returned as `COMPLETED`, call GET `https://api-beta.imagen-ai.com/v1/projects/<PROJECT_UUID>/edit/get_temporary_download_links`. 
In the request, include the photos to download in the `files_list` param. Use `list` format.
The response includes a temporary link for each photo to Imagen’s S3 bucket on AWS. This link is the AWS presigned URL.

#### Response example

```
{
    "data": {
        "files_list": [
            {
                "file_name": "922A4846.xmp",
                "upload_link": "<presigned URL for 922A4846.xmp>"
            },
            {
                "file_name": "922A4832.dng",
                "upload_link": "<presigned URL for 922A4832.xmp>"
            },
            {
                "file_name": "922A4818.dng",
                "upload_link": "<presigned URL for 922A4818.xmp>"
            },
            {
                "file_name": "922A4809.dng",
                "upload_link": "<presigned URL for 922A4809.xmp>"
            }
        ]
    }
}
```

### 2. Download photos locally

Download photos from Imagen’s S3 bucket on AWS with the temporary download links from the response in the previous step. Use any method you like. For sample code in Python, see `api_client.py` in the [Imagen API project](https://github.com/imagenai/imagen-api/tree/main) in GitHub.

For more information on downloading files with a presigned URL, see this [guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html) in the AWS documentation.

## Export photos for delivery

Imagen API exports all the photos in a project to JPEG format.

### 1. Export the photos in the project

Call POST `https://api-beta.imagen-ai.com/v1/projects/<PROJECT_UUID>/export`. The response includes the `project_uuid` and a message that the export was successful. If there is an error, contact Imagen for help.

### 2. Check the export status

Call GET `https://api-beta.imagen-ai.com/v1/projects/<PROJECT_UUID>/export/status`. The response includes the status of the export. Possible statuses are:

* `IN PROGRESS` Imagen API is exporting the photos as expected.
* `FAILED` Contact Imagen for help.
* `COMPLETED` Imagen API has finished exporting the photos to JPEG.
   
### 3. Download exported JPEG photos

#### Get temporary download links to download exported JPEG photos

After the export status is returned as `COMPLETED`, call GET `https://api-beta.imagen-ai.com/v1/projects/<PROJECT_UUID>/export/get_temporary_download_links`. 
In the request, include the exported photos to download in the `files_list` param. Use `list` format.
The response includes a temporary link for each photo to Imagen’s S3 bucket on AWS. This link is the AWS presigned URL.

```
{
    "data": {
        "files_list": [
            {
                "file_name": "922A4846.jpg",
                "upload_link": "<presigned URL for 922A4846.jpg>"
            },
            {
                "file_name": "922A4832.dng",
                "upload_link": "<presigned URL for 922A4832.jpg>"
            },
            {
                "file_name": "922A4818.dng",
                "upload_link": "<presigned URL for 922A4818.jpg>"
            },
            {
                "file_name": "922A4809.dng",
                "upload_link": "<presigned URL for 922A4809.jpg>"
            }
        ]
    }
}
```

#### Download exported JPEG photos locally

Download photos from Imagen’s S3 bucket on AWS with the temporary download links from the response in the previous step. Use any method you like. For sample code in Python, see `api_client.py` in the [Imagen API project](https://github.com/imagenai/imagen-api/tree/main) in GitHub.

For more information on downloading files with a presigned URL, see this [guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html) in the AWS documentation.

#### Deliver your photos

Your photos are now ready to deliver in JPEG format.









