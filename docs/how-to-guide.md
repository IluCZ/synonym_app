# How to Deploy and Use the Synonym App

## Rationale
Finding accurate synonyms quickly is essential for writers, students, and professionals. The Synonym App solves this challenge by:
- Providing instant access to multiple synonym sources for comprehensive results
- Supporting both single words and word combinations for more contextual results
- Maintaining search history for frequent words and phrases
- Ensuring reliable results through redundant API sources
- Offering a simple, intuitive web interface for easy access

## Prerequisites

Before deploying the Synonym App, ensure your environment meets these requirements:

System Requirements:
- Docker Desktop installed and running
- 4GB RAM minimum
- 10GB free disk space
- Stable internet connection

Network Requirements:
- Ports 8501 (frontend) and 8000 (backend) available
- No firewall blocking Docker connections
- Internet access for API calls

API Access (Required):
- Active API Ninjas account (register at https://api-ninjas.com/)
- Valid API key from API Ninjas dashboard
- Note: Keep your API key secure and never share it

## Procedure

To deploy and start using the Synonym App, follow these steps:

1. Set Up API Access:
   - Register at API Ninjas website
   - Log in to your dashboard
   - Copy your API key
   - Create `.env` file in the docker directory:
     ```
     API_NINJAS_KEY=your_key_here
     ```
   Result: `.env` file created with valid API key

2. Prepare Application:
   - Extract synonym_app.zip to your local machine
   - Open terminal/command prompt
   - Navigate to docker directory:
     ```bash
     cd synonym_app/docker
     ```
   Result: Working directory set to docker folder

3. Start Application:
   - Build and start containers:
     ```bash
     docker-compose up --build
     ```
   - Wait for build process to complete
   - Check for successful startup messages
   Result: Both frontend and backend containers running

4. Access Interface:
   - Open web browser
   - Navigate to http://localhost:8501
   - Verify Synonym Finder interface loads
   Result: Application interface visible and responsive

5. Perform Initial Test:
   - Enter a simple word (e.g., "happy")
   - Click "Find Synonyms"
   - Wait for results
   Result: List of synonyms displayed with API sources

## Validation

Verify that your installation is working correctly:

1. Check Container Status:
   ```bash
   docker ps
   ```
   Expected output: Two containers running (frontend, backend)

2. Verify API Connection:
   - Access http://localhost:8000/health
   - Expected response: {"status": "healthy"}

3. Test Core Functionality:
   - Basic word search
   - Word combination search
   - Advanced options adjustment
   Expected: Successful results for each test

4. Verify Features:
   - Search history appears
   - Source information displays
   - Error messages show when needed

## Troubleshooting

If you encounter issues, follow these steps:

1. Container Startup Issues:
   - Verify Docker Desktop is running
   - Check for port conflicts:
     ```bash
     netstat -ano | findstr "8501"
     netstat -ano | findstr "8000"
     ```
   - Review logs:
     ```bash
     docker-compose logs
     ```

2. No API Results:
   - Verify API key in `.env` file
   - Check internet connection
   - Confirm API service status at API Ninjas dashboard
   - Review backend logs:
     ```bash
     docker-compose logs backend
     ```

3. Interface Not Loading:
   - Clear browser cache
   - Try different browser
   - Restart containers:
     ```bash
     docker-compose down
     docker-compose up --build
     ```

4. Performance Issues:
   - Check system resources
   - Verify internet speed
   - Monitor container resources:
     ```bash
     docker stats
     ```

## Related Resources

- [Docker Desktop Installation](https://docs.docker.com/desktop/install/windows-install/)
- [API Ninjas Registration](https://api-ninjas.com/register)
- [API Ninjas Documentation](https://api-ninjas.com/api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## Contact and Support

For issues or questions:
- Email: richard.cibere@seznam.cz
- GitHub Issues: Create an issue in the repository