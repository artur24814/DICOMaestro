.. _usage:

=============
Usage Guide
=============

This documentation describes the steps for developers to authenticate and interact with the API to manage their API keys and work with DICOM files.

.. contents::
   :local:
   :depth: 2

**Prerequisites**

Before interacting with the API, developers must have an account on our platform and obtain an access token. This token will be used for authentication in subsequent requests.

---------------
Authentication
---------------

1. Obtain an Access Token
-------------------------

To interact with the API, developers must first authenticate by obtaining an access token. This token will be used in the Authorization header to make authenticated requests.

**Endpoint:**

- URL: `/api/token/`
- Method: `POST`
- Description: This endpoint accepts user credentials and returns an access token and a refresh token.

**Request**

You need to send a `POST` request to the `api/token/` endpoint with the following payload:

.. code-block:: json

    {
      "email": "user5@example.com",
      "password": "securepassword123"
    }

**Response**

If authentication is successful, you'll receive a response containing the access and refresh tokens:

.. code-block:: json

    {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXV......"
    }

- **access**: Use this token in the `Authorization` header as `Bearer <access_token>` for authenticated requests.
- **refresh**: Use this token to refresh the access token when it expires.

------------------
Developer Profile
------------------

Once you have the access token, you need to create a developer profile before you can obtain an API key.

2. Create a Developer Profile
-----------------------------

To register your profile as a developer, send a POST request to the `api/developer/profiles/` endpoint with the following details.

**Endpoint:**

- URL: `/api/developer/profiles/`
- Method: `POST`
- Description: This endpoint creates a new developer profile.

**Request**

Include the Authorization header with your Bearer access token and the profile information in the request body:

.. code-block:: json

    {
      "purpose": "testing",
      "organization": "My Organization"
    }

**Response**

If the profile creation is successful, you will receive a 201 Created status along with the details of your new profile:

.. code-block:: json

    {
      "purpose": "testing",
      "organization": "My Organization"
    }

- Status 201 Created: Indicates that the profile has been successfully created.

-------------------
API Key Management
-------------------

After creating your developer profile, you can obtain and manage your API keys.

3. List and Create API Keys
----------------------------

Once your profile is set up, you can create and list your API keys.

**Endpoint:**

- URL: `/api-keys/`
- Method: `GET`, `POST`
- Description:
  - `GET`: Retrieves the list of API keys associated with your developer profile.
  - `POST`: Creates a new API key for your developer profile.

**Request**

To list the API keys, send a `GET` request with the `Authorization` header:

.. code-block:: http

    GET /api-keys/ HTTP/1.1
    Authorization: Bearer <access_token>

To create a new API key, send a `POST` request with the following `JSON` payload:

.. code-block:: http

    POST /api-keys/ HTTP/1.1
    Authorization: Bearer <access_token>

    {
      "name": "New API Key"
    }

**Response**

- **GET `/api-keys/`**:
  - Status 200 OK: A list of API keys.
- **POST `/api-keys/`**:
  - Status 201 Created: The newly created API key.

Example Response for `POST`:

.. code-block:: json

    {
      "id": 1,
      "name": "New API Key",
      "key": "API_KEY_12345"
    }

- **key**: This is the actual API key you will use to authenticate API requests.

4. Delete API Key
-----------------

You can delete an existing API key by specifying its ID.

**Endpoint:**

- URL: `/api-keys/delete/<str:pk>/`
- Method: `DELETE`
- Description: Deletes the specified API key.

**Request**

To delete an API key, send a `DELETE` request to the URL `/api-keys/delete/<pk>/` with the `Authorization` header:

.. code-block:: http

    DELETE /api-keys/delete/1/ HTTP/1.1
    Authorization: Bearer <access_token>

**Response**

If the deletion is successful, the API will return a 204 No Content status:

.. code-block:: json

    {
      "detail": "Key deleted successfully."
    }

---------------------
Example API Key Flow
---------------------

Here’s a step-by-step example to help you understand the process:

1. Obtain an Access Token
-------------------------

Send a `POST` request to the `/api/token/` endpoint with your email and password:

.. code-block:: json

    {
      "email": "user5@example.com",
      "password": "securepassword123"
    }

Response:
~~~~~~~~~~

.. code-block:: json

    {
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }

2. Create Developer Profile
---------------------------

Use the access token to create your developer profile by sending a `POST` request to `/api/developer/profiles/`:

.. code-block:: json

    {
      "purpose": "testing",
      "organization": "My Organization"
    }

Response:
~~~~~~~~~~

.. code-block:: json

    {
      "purpose": "testing",
      "organization": "My Organization"
    }

3. Create an API Key
--------------------

With the developer profile created, you can now request your API key. Send a `POST` request to `/api-keys/`:

.. code-block:: json

    {
      "name": "New API Key"
    }

Response:
~~~~~~~~~~

.. code-block:: json

    {
      "id": 1,
      "name": "New API Key",
      "key": "API_KEY_12345"
    }

--------------------------------------
DICOM File Upload and Image Retrieval
--------------------------------------

To upload a DICOM file for processing and retrieve image data, you need to send a `POST` request to the `/api/dicom/read/file/` endpoint. The request should include the following:

**Endpoint:**

- URL: `/api/dicom/read/file/`
- Method: `POST`
- Description: This endpoint allows developers to upload a DICOM file, process it, and receive a response with DICOM metadata along with image data in the desired format.

**Request**

- **Headers**:
  - `Authorization`: `ApiKey amRqSg....`
- **Body**: The request body should contain the following parameters:
  - `file`: The DICOM file to be uploaded.
  - `fields` (optional): A comma-separated list of specific DICOM fields you wish to retrieve. If this is not provided, all fields will be included.
  - `return_format` (optional): The desired image format for the response. Valid values are gif, png, and jpeg.

Example Request:
~~~~~~~~~~~~~~~~

.. code-block:: http

    POST /api/dicom/read/file/ HTTP/1.1
    Host: localhost:8080
    Authorization: ApiKey amRqSgZZ.CLevHmvt7WJucw2gKA5sGhEUs2Fh6Svq
    Content-Type: multipart/form-data

    --boundary
    Content-Disposition: form-data; name="file"; filename="dicom-file.dcm"
    Content-Type: application/dicom

    <binary DICOM file content>

    --boundary
    Content-Disposition: form-data; name="fields"

    PatientName,StudyDate,Modality

    --boundary
    Content-Disposition: form-data; name="return_format"

    png
    --boundary--

**Parameters**:
- `file` (required): The DICOM file to upload. Must be one of the following formats: `.dcm`, `.DCM`, `.zip`.
- `fields` (optional): A comma-separated list of specific DICOM fields to retrieve. If not provided, all available fields will be returned.
- `return_format` (optional): The image format you prefer for the response. Valid options are: `gif`, `png`,  `jpeg`

**Response**

Upon successful processing of the file, you will receive a response containing DICOM metadata and the image in the requested format.

**Example Response:**

.. code-block:: json

    {
      "SOPClassUID": "1.2.840.10008.5.1.4.1.1.12.1",
      "SOPInstanceUID": "1.3.12.2.1107.5.4.3.321890.19960124.162922.29",
      "StudyDate": "19941013",
      "StudyTime": "141917",
      "Modality": "XA",
      "LossyImageCompressionRetired": "01",
      "PatientName": "Rubo DEMO",
      "PatientID": "556342B",
      "PatientBirthDate": "19951025",
      "PatientSex": "M",
      "FrameTime": "33",
      "RadiationSetting": "GR",
      "PositionerPrimaryAngle": "-32",
      "PositionerSecondaryAngle": "2",
      "StudyInstanceUID": "1.3.12.2.1107.5.4.3.123456789012345.19950922.121803.6",
      "SeriesInstanceUID": "1.3.12.2.1107.5.4.3.123456789012345.19950922.121803.8",
      "SeriesNumber": "1",
      "SamplesPerPixel": "1",
      "PhotometricInterpretation": "MONOCHROME2",
      "NumberOfFrames": "96",
      "FrameIncrementPointer": "(0018,1063)",
      "Rows": "512",
      "Columns": "512",
      "BitsAllocated": "8",
      "BitsStored": "8",
      "HighBit": "7",
      "PixelIntensityRelationship": "LIN",
      "RecommendedViewingMode": "NAT",
      "RWavePointer": "[20, 53, 77]",
      "PixelData": "b'\\xfe\\xff\\x00\\xe0\\x80\\x01\\x00\\x00\\x00.....",
      "ImageFormat": "PNG",
      "Images": ["iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAAAAADRE4s...", "d...", ""]
    }


Explanation of Response Fields:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **ImageType**: Describes the type of image (e.g., derived, primary).
- **SOPClassUID**: The unique identifier for the DICOM SOP class.
- **SOPInstanceUID**: The unique identifier for the specific instance of the DICOM image.
- **PatientName**: Name of the patient.
- **Modality**: Type of medical imaging modality used (e.g., XA for X-ray angiography).
- **PixelData**: The pixel data of the image (in binary format).
- **ImageFormat**: The format of the image returned (e.g., PNG).
- **Images**: A list of base64-encoded image data for each image.


----------------
API Usage Limits
----------------

Each developer has access to the DICOM file upload endpoint up to 1000 times per month. To check your remaining usage, you can use the following endpoint:

To view the daily and monthly usage for your developer profile, send a `GET` request to the activity-summary endpoint.

**Endpoint**
- URL: `api/developer/profiles/activity-summary/`
- Method: `GET`
- Description: Retrieves the daily and monthly usage statistics for your API access.

Request
~~~~~~~~

- **Headers**:
    - `Authorization`: `Bearer <access_token>`

Example Request:
~~~~~~~~~~~~~~~~~~

.. code-block:: http

    GET /api/developer/profiles/activity-summary/ HTTP/1.1
    Host: localhost:8080
    Authorization: Bearer <access_token>

Response
~~~~~~~~~~

You will receive a response with your daily and monthly usage:

.. code-block:: json

    {
      "daily_activity": [
        {
          "day": "2025-01-05",
          "count": 1
        }
      ],
      "monthly_total": 1
    }

- **daily_activity**: An array showing how many requests have been made each day.
- **monthly_total**: The total number of requests made for the current month.

Error Handling: API Limit Exceeded
-----------------------------------

If the monthly usage limit is exceeded, you will receive a `429 Too Many Requests` response. The response will contain an error message indicating that the limit has been reached, and you will need to wait until the new month to refresh your quota.

Example Response for Exceeded Limit:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "error": "Monthly API request for '/api/dicom/read/file/' limit exceeded.",
      "quota": 1000,
      "requests_used": 1001
    }

- **error**: A description of the error, including the endpoint and the exceeded limit.
- **quota**: The maximum number of requests allowed per month for that endpoint.
- **requests_used**: The number of requests that have been used during the current month.

Once the limit is reached, you will need to wait for the start of the new month for your API request quota to reset.