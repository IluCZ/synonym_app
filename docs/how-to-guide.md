# Deploy and Use the Synonym App

This application helps users find synonyms for words and word combinations through multiple API sources. It provides 3-10 relevant synonyms for your search terms through a simple web interface.

When deploying and using this application, ensure you have:
- Docker Desktop installed
- Active internet connection
- API Ninjas key (signup at api-ninjas.com, add to `.env` file as `API_NINJAS_KEY=your_key`)

1. Start Docker Desktop and complete registration or login
2. Open terminal in Docker by clicking the >_ symbol
3. Navigate to the project directory using CD command
4. Execute command: `docker-compose up --build`
5. Wait for the "Application started successfully" message

Once deployed:
1. Open your web browser and navigate to http://localhost:8501
2. Wait for the application to load
3. Enter word or phrase in the search field
4. Click "Find Synonyms" button
5. For additional features and settings, click "How to use" dropdown

Using application you will get:
- Generated synonyms (3-10 words) from either API Ninjas or Datamuse source
- For multiple word search:
  * Individual synonyms for each word
  * Combined synonyms of both words together

Useful links:
- API Documentation: http://localhost:8000/docs
- API Ninjas: https://api-ninjas.com/
- Datamuse API: https://www.datamuse.com/api/
- Support Contact: richard.cibere@seznam.cz



