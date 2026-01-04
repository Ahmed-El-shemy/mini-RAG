# Mini-RAG API with FastAPI

A simple file management and data processing API built with **FastAPI**, designed as a foundation for RAG (Retrieval-Augmented Generation) systems.

## Features
- **File Upload**: Upload and validate files with configurable size and type restrictions.
- **Configuration Management**: Environment-based settings using Pydantic.
- **API Documentation**: Auto-generated Swagger UI and ReDoc.

## Tech Stack
- **Framework**: FastAPI
- **Configuration**: Pydantic Settings with `.env` support
- **Validation**: Custom file validation controllers

## Project Structure

```
mini-RAG/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── routes/                 # API route definitions
│   │   └── basy.py            # Base routes (health check, info)
│   ├── infrastructure/         # Core infrastructure components
│   │   ├── config.py          # Application settings
│   │   ├── BaseController.py  # Base controller class
│   │   ├── Datacontroller.py  # File validation controller
│   │   └── data.py            # Data upload routes
│   ├── enums/                 # Enumerations and constants
│   ├── models/                # Data models
│   └── services/              # Business logic services
├── requirement.txt            # Project dependencies
├── .env.example              # Example environment variables
└── README.md                 # This file
```

## Setup

1. **Clone & Enter Directory**
   ```bash
   cd mini-RAG
   ```

2. **Create Virtual Environment & Install Dependencies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirement.txt
   ```

3. **Configure Environment Variables**
   
   Create a `.env` file in the root directory:
   ```env
   APP_NAME=Mini-RAG
   APP_VERSION=1.0.0
   OPENAI_API_KEY=your_api_key_here
   FILDE_ALLOWED_TYPES=["application/pdf", "text/plain"]
   ```

## Run docker compose Services

```bash
 $ cd docker 
 $ cp .env.example .env
 $ docker-compose up -d
```

 -update '.env' with your cerdentials

## stop docker compose Services

```bash
 $ sudo docker stop $(sudo docker ps -aq )
```

## remove docker compose Services

```bash
 $ sudo docker rm $(sudo docker ps -aq )
```


## remove docker images

```bash
 $ sudo docker rmi $(sudo docker images -q)
```

## remove docker volumes

```bash
 $ sudo docker volume rm $(sudo docker volume ls -q)
```

## remove all docker

```bash
 $ sudo docker system prune --all
```


## Running the App

Run the server using `uvicorn` from the project root:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage

Visit the automatic documentation at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

### Endpoints

- **GET `/`**: Get application information (name and version).
- **POST `/api/v1/data/upload/{project_id}`**: Upload files with validation.

## Development

### Adding New Routes
1. Create a new router file in `app/routes/`
2. Import and include the router in `app/main.py`

### Configuration
Add new settings to `app/infrastructure/config.py` and update your `.env` file accordingly.

## License

This project is for learning purposes.
