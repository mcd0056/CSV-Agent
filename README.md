# FastAPI Application

This project is a FastAPI application designed to provide a simple chat interface and a feature to upload CSV files. It includes CORS middleware for cross-origin requests, automatic temp directory management for uploaded files, and redirection to a static HTML page for the root path.

## Features

- **Chat Interface**: Allows sending messages which are processed by a custom agent.
- **CSV Upload**: Supports uploading CSV files, storing them temporarily.
- **CORS Enabled**: Configured to allow cross-origin requests.
- **Static Files Serving**: Serves static files from a specified directory.
- **Startup and Shutdown Events**: Custom actions during startup and shutdown, like managing a temporary directory for file uploads.

## Requirements

To run this project, you'll need:

- Python 3.8+
- FastAPI
- Uvicorn
- Python-dotenv
- Pydantic
- Any additional dependencies listed in `requirements.txt`.

## Installation

Clone the repository and navigate into the project directory:


- git clone https://yourprojectrepository.git
- cd yourprojectdirectory

* Install the necessary dependencies:
- pip install -r requirements.txt


## Usage
- Start the application by running:
- uvicorn main:app --reload

* The application will be available at http://localhost:8000.


## Docker Install
Docker Deployment
A Dockerfile and docker-compose.yml are provided for containerization and easy deployment.

- Build and run the Docker container using:
- docker-compose up --build


## API Endpoints
- GET /: Redirects to static/index.html.
- POST /chat/: Accepts a message and returns a response from the agent.
- POST /upload_csv/: Uploads a CSV file and stores it temporarily.


## Environment Variables
This application uses environment variables for configuration. See the .env file for reference.

OPENAI_API_KEY = "ENTER YOUR OPENAI API KEY INTO .ENV File"

## Swagger Docs
- http://localhost:8000/docs/