# <img src="frontend/public/logo512.png" alt="Diagram aplikacji" width="25" /> DICOMaestro

<strong>DICOMaestro</strong> is a free, open-source application for viewing DICOM images and sequences,
exploring metadata, and creating custom DICOM files via an API for developers.
Built with privacy and security in mind, the application does not store any image data,
ensuring compliance with data protection requirements.

Whether you are a medical professional, researcher, or developer,
DICOMaestro provides powerful tools for working with medical imaging data,
along with flexible APIs for integrating its features into your own applications.

Key Features
* DICOM Image Viewer:
Supports single images and sequences such as CT scans or MRIs.
* Metadata Viewer:
Displays detailed metadata from DICOM files.
* Custom DICOM File Creation:
Generate new DICOM files using the developer-friendly API.
* Secure and Private:
Processes data locally without storing sensitive information.

## API Documentation for Developers
This documentation describes the steps for developers to authenticate and interact with the API to manage their API keys and work with DICOM files.

### Prerequisites
Before interacting with the API, developers must have an account on our platform and obtain an access token. This token will be used for authentication in subsequent requests.

## Authentication
### 1. Obtain an Access Token
To interact with the API, developers must first authenticate by obtaining an access token. This token will be used in the Authorization header to make authenticated requests.

Endpoint
* URL: `/api/token/`
* Method: `POST`
* Description: This endpoint accepts user credentials and returns an access token and a refresh token.
#### Request
You need to send a `POST` request to the `api/token/` endpoint with the following payload:

```json
{
  "email": "user5@example.com",
  "password": "securepassword123"
}
```
#### Response
If authentication is successful, you'll receive a response containing the access and refresh tokens:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXV......"
}
```
* access: Use this token in the `Authorization` header as   `Bearer <access_token>` for authenticated requests.
* refresh: Use this token to refresh the access token when it expires.
## Developer Profile
Once you have the access token, you need to create a developer profile before you can obtain an API key.

### 2. Create a Developer Profile
To register your profile as a developer, send a POST request to the `api/developer/profiles/` endpoint with the following details.

Endpoint
* URL: `/api/developer/profiles/`
* Method: `POST`
* Description: This endpoint creates a new developer profile.
#### Request
Include the Authorization header with your Bearer access token and the profile information in the request body:

```json
{
  "purpose": "testing",
  "organization": "My Organization"
}
```
#### Response
If the profile creation is successful, you will receive a 201 Created status along with the details of your new profile:

```json
{
  "purpose": "testing",
  "organization": "My Organization"
}
```
* Status 201 Created: Indicates that the profile has been successfully created.

## API Key Management
After creating your developer profile, you can obtain and manage your API keys.

### 3. List and Create API Keys

Once your profile is set up, you can create and list your API keys.

Endpoint
* URL: /api-keys/
* Method: `GET`, `POST`
* Description:
    * `GET`: Retrieves the list of API keys associated with your developer profile.
    * `POST`: Creates a new API key for your developer profile.
#### Request
To list the API keys, send a `GET` request with the `Authorization` header:

```http
GET /api-keys/ HTTP/1.1
Authorization: Bearer <access_token>
```
To create a new API key, send a `POST` request with the following `JSON` payload:

```http
POST /api-keys/ HTTP/1.1
Authorization: Bearer <access_token>

{
  "name": "New API Key"
}
```
#### Response
* GET `/api-keys/`:
    * Status 200 OK: A list of API keys.
* POST `/api-keys/`:
    * Status 201 Created: The newly created API key.

Example Response for `POST`:

```json
{
  "id": 1,
  "name": "New API Key",
  "key": "API_KEY_12345"
}
```
* key: This is the actual API key you will use to authenticate API requests.
4. Delete API Key

You can delete an existing API key by specifying its ID.

Endpoint
* URL: `/api-keys/delete/<str:pk>/`
* Method: `DELETE`
* Description: Deletes the specified API key.
### Request
To delete an API key, send a `DELETE` request to the URL `/api-keys/delete/<pk>/` with the `Authorization` header:

```http
DELETE /api-keys/delete/1/ HTTP/1.1
Authorization: Bearer <access_token>
```
### Response
If the deletion is successful, the API will return a 204 No Content status:

```json
{
  "detail": "Key deleted successfully."
}
```
## Example API Key Flow
Here’s a step-by-step example to help you understand the process:

### Step 1: Obtain an Access Token
Send a POST request to the `/api/token/` endpoint with your email and password:

```json
{
  "email": "user5@example.com",
  "password": "securepassword123"
}
```
Response:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
### Step 2: Create Developer Profile
Use the access token to create your developer profile by sending a `POST` request to `/api/developer/profiles/`:

```json
{
  "purpose": "testing",
  "organization": "My Organization"
}
```
### Response:

```json
{
  "purpose": "testing",
  "organization": "My Organization"
}
```
### Step 3: Create an API Key
With the developer profile created, you can now request your API key. Send a `POST` request to `/api-keys/`:

```json
{
  "name": "New API Key"
}
```
### Response:

```json
{
  "id": 1,
  "name": "New API Key",
  "key": "API_KEY_12345"
}
```

## DICOM File Upload and Image Retrieval

To upload a DICOM file for processing and retrieve image data, you need to send a `POST` request to the `/api/dicom/read/file/` endpoint. The request should include the following:

Endpoint
* URL: `/api/dicom/read/file/`
* Method: `POST`
* Description: This endpoint allows developers to upload a DICOM file, process it, and receive a response with DICOM metadata along with image data in the desired format.
#### Request
* Headers:
    * `Authorization`: `ApiKey amRqSg....`
* Body: The request body should contain the following parameters:

    * `file`: The DICOM file to be uploaded.
    * `fields` (optional): A comma-separated list of specific DICOM fields you wish to retrieve. If this is not provided, all fields will be included.
    * `return_format` (optional): The desired image format for the response. Valid values are gif, png, and jpeg.
#### Example Request:
```http
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
```
Parameters:
* `file` (required): The DICOM file to upload. Must be one of the following formats: `.dcm`, `.DCM`, `.zip`.
* `fields` (optional): A comma-separated list of specific DICOM fields to retrieve. If not provided, all available fields will be returned.
* `return_format` (optional): The image format you prefer for the response. Valid options are:
    * `gif`
    * `png`
    * `jpeg`
#### Response
Upon successful processing of the file, you will receive a response containing DICOM metadata and the image in the requested format.

Example Response:

```json
{
  "ImageType": "['DERIVED', 'PRIMARY', 'SINGLE PLANE', 'SINGLE A']",
  "SOPClassUID": "1.2.840.10008.5.1.4.1.1.12.1",
  "SOPInstanceUID": "1.3.12.2.1107.5.4.3.321890.19960124.162922.29",
  "StudyDate": "19941013",
  "StudyTime": "141917",
  "Modality": "XA",
  "LossyImageCompressionRetired": "01",
  "SourceImageSequence": "[(0008,1150) Referenced SOP Class UID            UI: X-Ray Angiographic Image Storage\n(0008,1155) Referenced SOP Instance UID         UI: 1.3.12.2.1107.5.4.3.321890.19960124.162922.28]",
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
  "MaskSubtractionSequence": "[(0028,6101) Mask Operation                      CS: 'NONE'\n(0028,6110) Mask Frame Numbers                  US: 0]",
  "PixelData": "b'\\xfe\\xff\\x00\\xe0\\x80\\x01\\x00\\x00\\x00.....",
  "ImageFormat": "PNG",
  "Images": ["iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAAAAADRE4s...", "d...", ....]
}
```
#### Explanation of Response Fields:
* `ImageType`: Describes the type of image (e.g., derived, primary).
* `SOPClassUID`: The unique identifier for the DICOM SOP class.
* `SOPInstanceUID`: The unique identifier for the specific instance of the DICOM image.
* `PatientName`: Name of the patient.
* `Modality`: Type of medical imaging modality used (e.g., XA for X-ray angiography).
* `PixelData`: The pixel data of the image (in binary format).
* `ImageFormat`: The format of the image returned (e.g., PNG).
* `Images`: A list of base64-encoded image data for each image.

## API Usage Limits

Each developer has access to the DICOM file upload endpoint up to 1000 times per month. To check your remaining usage, you can use the following endpoint:

To view the daily and monthly usage for your developer profile, send a `GET` request to the `activity-summary` endpoint.

Endpoint
* URL: `api/developer/profiles/activity-summary/`
* Method: GET
* Description: Retrieves the daily and monthly usage statistics for your API access.
#### Request
* Headers:
    * `Authorization`: `Bearer <access_token>`
#### Example Request:
```http
GET /api/developer/profiles/activity-summary/ HTTP/1.1
Host: localhost:8080
Authorization: Bearer <access_token>
```
#### Response
You will receive a response with your daily and monthly usage:

```json
{
  "daily_activity": [
    {
      "day": "2025-01-05",
      "count": 1
    }
  ],
  "monthly_total": 1
}
```
* `daily_activity`: An array showing how many requests have been made each day.
* `monthly_total`: The total number of requests made for the current month.
## Error Handling: API Limit Exceeded
If the monthly usage limit is exceeded, you will receive a 429 Too Many Requests response. The response will contain an error message indicating that the limit has been reached, and you will need to wait until the new month to refresh your quota.

#### Example Response for Exceeded Limit:

```json
{
  "error": "Monthly API request for '/api/dicom/read/file/' limit exceeded.",
  "quota": 1000,
  "requests_used": 1001
}
```
* `error`: A description of the error, including the endpoint and the exceeded limit.
* `quota`: The maximum number of requests allowed per month for that endpoint.
* `requests_used`: The number of requests that have been used during the current month.

Once the limit is reached, you will need to wait for the start of the new month for your API request quota to reset.

## Installation
### Prerequisites:
* Python 3.8+
* Node.js 16+
* PostgreSQL
### Backend Setup (Django):

* Clone the repository:
    
    ```bash
    git clone https://github.com/yourusername/DICOMaestro.git  
    cd DICOMaestro/backend
    ```
* Create a virtual environment:
    ```bash
    python -m venv env  
    source env/bin/activate
    ``` 
* Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
* Configure the .env file with your database credentials.

* Run database migrations:
    ```bash
    python manage.py migrate
    ```
* Start the backend server:
    ```bash
    python manage.py runserver
    ```
### Frontend Setup (React):
* Navigate to the frontend directory:
    ```bash
    cd ../frontend
    ```
* Install dependencies:
    ```bash
    npm install
    ```
* Start the development server:
    ```bash
    npm start
    ```

### Alternative Setup Using Docker:
You can also use Docker to set up both the backend and frontend with the docker-compose.dev.yml file.

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/DICOMaestro.git
    cd DICOMaestro
    ```
2. Create a `.env` file: In the root directory of the project, create a .env file and configure it with the following values:

    ```env
    SECRET_KEY='super_secret'
    DEBUG=True

    DB_HOST='db'
    DB_DB='postgres'
    DB_PORT=5432
    DB_USER='postgres'
    DB_PASSWORD='super_password'

    DJANGO_ALLOWED_HOSTS='localhost 0.0.0.0 127.0.0.1'

    CSRF_TRUSTED_ORIGINS='http://localhost:80'
    ```
3. Build and start the containers: From the root directory, use the following command to build and start the Docker containers using `docker-compose.dev.yml`:

    ```bash
    docker-compose -f docker-compose.dev.yml up --build
    ```
    This will set up both the backend (Django) and frontend (React) in Docker containers.

4. Access the Application: Once the containers are running, you can access the application by opening your browser and navigating to:

    * `http://localhost:80` for the frontend
    * `http://localhost:80/api/` for the backend API (Django)


### Usage

Open your browser and navigate to `http://localhost:3000`.

Use the intuitive web interface to upload and view DICOM files, explore metadata, or interact with the API.
Refer to the API documentation (/api/docs) for integrating DICOMaestro into your applications.

## Contributing
We welcome contributions from the community! Here's how you can help:

* Report Issues: Use the GitHub issue tracker to report bugs or suggest features.
* Submit Pull Requests: Fork the repository, make your changes, and submit a pull request.
* Improve Documentation: Help us improve the installation and usage guides.
## Guidelines:
Follow the PEP 8 standard for Python code.
Use ESLint to lint JavaScript code.
Ensure your changes are covered by tests.
## License
DICOMaestro is licensed under the MIT License, making it free to use, modify, and distribute. See the LICENSE file for details.

#### Start using DICOMaestro today to simplify your work with medical imaging data!
