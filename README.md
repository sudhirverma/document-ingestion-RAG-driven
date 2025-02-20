# Flask-based Application

## Overview
This is a Flask-based API application that integrates with AWS Bedrock MistralAI. The application is containerized using Docker and relies on PostgreSQL as the database.

## Prerequisites
Ensure you have the following installed:
- Docker
- Docker Compose
- Python 3.9+

## Environment Variables
Create a `.env` file in the project root directory and set the following AWS credentials:

```
AWS_ACCESS_KEY_ID=<your_aws_access_key_id>
AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
AWS_REGION=<your_aws_region>
```

These credentials will be used to interact with AWS Bedrock and MistralAI services.

## Running the Application

### Step 1: Start PostgreSQL Container
```
docker-compose up postgres
```

This will start a PostgreSQL container as defined in the `docker-compose.yml` file.

### Step 2: Start Flask API
The application is served using `uvicorn`.

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

This will start the Flask API server on `http://localhost:8000`.

## API Documentation
Swagger documentation is available at:

[http://localhost:8000/docs](http://localhost:8000/docs)

This will provide details about the available endpoints and their usage.

## Useful Commands
- Stop all running containers:
  ```
  docker-compose down
  ```
- Rebuild containers (if needed):
  ```
  docker-compose build
  ```

## Troubleshooting
If you encounter any issues, ensure the `.env` file is correctly set up and that Docker services are running.

## License
This project is licensed under the MIT License.

# document-ingestion-RAG-driven
# document-ingestion-RAG-driven
