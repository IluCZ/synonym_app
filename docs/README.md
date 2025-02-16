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

## Tech Stack

- Frontend: Streamlit (Python)
- Backend: FastAPI (Python)
- Containerization: Docker & Docker Compose
- APIs: Datamuse, API Ninjas

## Project Structure

```
synonym_app/
├── frontend/
│   ├── app.py              # Streamlit frontend application
│   ├── requirements.txt    # Frontend dependencies
│   └── .streamlit/        # Streamlit configuration
├── backend/
│   ├── main.py            # FastAPI backend application
│   ├── test_api.py        # API tests
│   └── requirements.txt    # Backend dependencies
├── docker/
│   ├── config/            # Configuration files
│   ├── logs/             # Application logs
│   ├── .dockerignore     # Docker ignore file
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
└── docs/                  # Documentation files
```

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (version 20.10 or higher)
- Internet connection (for accessing synonym APIs)
- Available ports:
  - 8501 (Frontend)
  - 8000 (Backend API)

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd synonym_app
   ```

2. Navigate to the docker directory:
   ```bash
   cd docker    # Important: You must be in the docker directory!
   ```

3. Start the application:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: [http://localhost:8501](http://localhost:8501)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## Development Setup

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Usage Guide

### Single Word Search
1. Enter a word in the input field
2. (Optional) Adjust minimum and maximum synonyms in Advanced Options
3. Click "Find Synonyms"
4. View results and sources used

### Word Combination Search
1. Enter two words separated by space (e.g., "fast car")
2. Click "Find Synonyms"
3. View synonyms for each word and suggested combinations

## API Documentation

### Endpoints

#### Health Check
```
GET /health
```
Returns the current health status of the API.

#### Get Synonyms
```
POST /synonyms
```
Parameters:
- `word` (required): Word to find synonyms for
- `second_word` (optional): Second word for combinations
- `min_synonyms` (default: 3): Minimum number of synonyms
- `max_synonyms` (default: 10): Maximum number of synonyms

## Error Handling

The application includes comprehensive error handling for:
- Connection issues
- API timeouts
- Invalid inputs
- Server errors
- No synonyms found

Errors are logged and displayed in the UI with user-friendly messages.

## Troubleshooting

### Docker Issues

1. Make sure you're in the correct directory:
   ```bash
   cd synonym_app/docker
   ```

2. If the application won't start:
   - Ensure Docker Desktop is running
   - Check if ports 8501 and 8000 are available
   - Review Docker logs: `docker-compose logs`

3. To rebuild the application:
   ```bash
   # Stop the application
   docker-compose down

   # Remove containers and rebuild
   docker-compose up --build
   ```

### Application Issues

1. If no synonyms are found:
   - Verify your internet connection
   - Check the backend health at http://localhost:8000/health
   - Try a different word or phrase

2. If experiencing slow responses:
   - Check your internet connection speed
   - Verify that both API services are operational
   - Try reducing the maximum number of synonyms requested

## Testing

Run backend tests:
```bash
cd backend
pytest test_api.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## Contact

For issues or questions:
- Email: richard.cibere@seznam.cz
- GitHub Issues: [Create an issue](repository-issues-url)

