# How to Deploy and Use the Synonym App

## Rationale
The Synonym App helps users find synonyms for words and word combinations using multiple API sources. The application provides a user-friendly web interface for searching synonyms and maintains a search history. Using Docker ensures consistent deployment across different platforms and simplifies the installation process.

## Prerequisites
Before deploying the Synonym App, ensure that your system meets the following requirements:

- Docker Desktop is installed and running on your machine
- Ports 8501 and 8000 are available and not used by other applications
- Minimum system requirements:
  - 4GB RAM
  - 10GB free disk space
  - Internet connection for accessing synonym APIs

## Procedure
To deploy and start using the Synonym App, follow these steps:

1. Prepare the deployment environment:
   - Download and extract the `synonym_app.zip` file to your local machine
   - Open a terminal or command prompt
   - Navigate to the docker directory:
     ```bash
     cd synonym_app/docker
     ```

2. Start the application:
   - Execute the following command to build and start the containers:
     ```bash
     docker-compose up --build
     ```
   - Wait for both frontend and backend services to start
   - You should see messages indicating successful startup for both services

3. Access the application:
   - Open your web browser
   - Navigate to http://localhost:8501
   - The Synonym Finder interface should appear

4. Use the application:
   - Enter a word or phrase in the input field
   - [Optional] Expand "Advanced Options" to adjust the number of synonyms
   - Click "Find Synonyms"
   - View the results displayed below the input form
   - [Optional] Check the search history in the expandable section

5. Monitor the application:
   - Check that both services are running:
     ```bash
     docker ps
     ```
   - You should see two containers: frontend and backend
   - Verify the backend health at http://localhost:8000/health

6. Stop the application:
   - Press Ctrl+C in the terminal where the application is running
   - Wait for both containers to stop gracefully

## Validation
To verify that the application is working correctly:

1. Check container status:
   - Open a new terminal
   - Run `docker ps`
   - Verify both frontend and backend containers are running

2. Test the application:
   - Enter a simple word like "happy"
   - Click "Find Synonyms"
   - You should receive at least 3 synonyms
   - The sources used should be displayed

3. Verify features:
   - Test search history functionality
   - Try advanced options
   - Test with multiple words

## Troubleshooting
If you encounter issues:

1. Container startup fails:
   - Verify Docker Desktop is running
   - Check if ports 8501 and 8000 are available
   - Review logs with `docker-compose logs`

2. Application not responding:
   - Refresh the browser page
   - Restart the containers:
     ```bash
     docker-compose down
     docker-compose up --build
     ```

3. No synonyms found:
   - Check your internet connection
   - Verify backend health at http://localhost:8000/health
   - Review backend logs for API errors

## Related Links
- [Docker Desktop Installation Guide](https://docs.docker.com/desktop/install/windows-install/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)