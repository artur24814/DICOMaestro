# DICOMaestro

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
