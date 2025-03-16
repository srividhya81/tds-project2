# tds-project2

## Overview
The `tds-project2` is a FastAPI application designed to handle various data processing tasks and provide a set of APIs for file uploads and data manipulation. This project includes multiple endpoints that allow users to interact with the application seamlessly.

## Features
- FastAPI framework for building APIs
- Various endpoints for data processing and file handling
- Support for file uploads
- JSON response format for API interactions

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd tds-project2
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application
To run the FastAPI application locally, use the following command:
```
uvicorn api.main:app --reload
```
This will start the server at `http://127.0.0.1:8000`.

## API Documentation
The API documentation can be accessed at `http://127.0.0.1:8000/docs` once the server is running.

## Deployment
This application can be deployed on Vercel. The configuration for deployment is specified in the `vercel.json` file.

## Usage
Refer to the API documentation for details on how to use the various endpoints provided by the application.