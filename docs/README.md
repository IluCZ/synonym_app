# Synonym Finder Application

A web application that helps users find synonyms for words and word combinations. The application uses multiple API sources to provide comprehensive synonym results and supports both single words and word combinations.

## Features

- Find synonyms for single words and word combinations
- Multiple API sources (Datamuse, API Ninjas)
- Advanced options for controlling synonym count
- Search history tracking
- Responsive web interface
- Error handling and logging
- Health monitoring
- Cross-platform support via Docker

## Project Structure

```
synonym_app/
├── frontend/
│   ├── app.py              # Streamlit frontend application
│   ├── requirements.txt    # Frontend dependencies
│   └── .streamlit/        # Streamlit configuration
├── backend/
│   ├── main.py            # FastAPI backend application
│   └── requirements.txt    # Backend dependencies
└── docker/
    ├── config/            # Configuration files
    ├── logs/             # Application logs
    ├── .dockerignore     # Docker ignore file
    ├── docker-compose.yml
    ├── Dockerfile.backend
    └── Dockerfile.frontend
```

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Internet connection (for accessing synonym APIs)
- Ports 8501 and 8000 available on your machine

## Installation and Running

1. Clone the repository or extract the provided ZIP file:
   ```bash
   git clone <repository-url>
   # or extract synonym_app.zip
   ```

2. Navigate to the docker directory:
   ```bash
   cd synonym_app/docker
   ```

3. Build and start the application:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend interface: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Usage Guide

1. Single Word Search:
   - Enter a word in the input field
   - Optionally adjust minimum and maximum synonyms in Advanced Options
   - Click "Find Synonyms"
   - View results and sources used

2. Word Combination Search:
   - Enter two words separated by space (e.g., "fast car")
   - Click "Find Synonyms"
   - View synonyms for each word and suggested combinations

3. History:
   - View your search history in the expandable section
   - Clear history with the "Clear History" button

## Error Handling

The application includes comprehensive error handling for:
- Connection issues
- API timeouts
- Invalid inputs
- Server errors
- No synonyms found

Error messages are displayed in the UI and logged for troubleshooting.

## Troubleshooting

1. If the application won't start:
   - Ensure Docker Desktop is running
   - Check if ports 8501 and 8000 are available
   - Review Docker logs: `docker-compose logs`

2. If no synonyms are found:
   - Verify your internet connection
   - Check the backend health at http://localhost:8000/health
   - Try a different word or phrase

3. For other issues:
   - Stop the application: Ctrl+C
   - Remove containers: `docker-compose down`
   - Rebuild: `docker-compose up --build`

## Development

To run the application in development mode:

1. Backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. Frontend:
   ```bash
   cd frontend
   pip install -r requirements.txt
   streamlit run app.py
   ```

## API Documentation

The backend API provides the following endpoints:

- `GET /health` - Health check endpoint
- `POST /synonyms` - Get synonyms for words
  - Parameters:
    - word (required): Word to find synonyms for
    - second_word (optional): Second word for combinations
    - min_synonyms (default: 3): Minimum number of synonyms
    - max_synonyms (default: 10): Maximum number of synonyms

Detailed API documentation is available at http://localhost:8000/docs when the application is running.



## Contact

For issues or questions, please contact:
richard.cibere@seznam.cz