import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
from typing import List, Dict, Set, Optional, Tuple
import asyncio
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join('logs', 'app.log'))
    ]
)
logger = logging.getLogger(__name__)

class WordRequest(BaseModel):
    """Request model for synonym lookup"""
    word: str = Field(..., min_length=1, max_length=100, description="Word to find synonyms for")
    second_word: Optional[str] = Field(None, description="Optional second word for phrases")
    min_synonyms: int = Field(default=3, ge=1, le=10, description="Minimum synonyms to return")
    max_synonyms: int = Field(default=10, ge=1, le=10, description="Maximum synonyms to return")

class SynonymResponse(BaseModel):
    """Response model for synonym results"""
    word: str
    synonyms: List[str]
    second_word_synonyms: Optional[List[str]] = None
    sources: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)

class SynonymAPI:
    def __init__(self):
        # Initialize API configurations
        self.apis = {
            "ninjas": {
                "url": "https://api.api-ninjas.com/v1/thesaurus",
                "params": lambda word: {"word": word},
                "headers": {
                    "X-Api-Key": os.getenv('NINJAS_API_KEY', 'oFp6FIbNI+5DQGSfDkmMag==0UFNr61a8PcsRKDm')
                }
            },
            "datamuse": {
                "url": "https://api.datamuse.com/words",
                "params": lambda word: {
                    "ml": word,
                    "rel_syn": word,
                    "max": 15
                }
            }
        }
        self.cache: Dict[str, Dict] = {}

    async def get_synonyms_from_api(self, api_name: str, word: str) -> List[str]:
        """
        Get synonyms from a specific API
        Args:
            api_name: Name of the API to use
            word: Word to find synonyms for
        Returns:
            List of synonyms
        """
        try:
            async with httpx.AsyncClient() as client:
                api_config = self.apis[api_name]
                url = api_config["url"]
                
                # Prepare request parameters
                request_kwargs = {
                    "params": api_config["params"](word),
                    "timeout": 5.0
                }
                if "headers" in api_config:
                    request_kwargs["headers"] = api_config["headers"]

                # Make API request
                response = await client.get(url, **request_kwargs)
                logger.info(f"{api_name} response status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    # Process response based on API
                    if api_name == "datamuse":
                        return [item["word"] for item in data if "word" in item 
                               and len(item["word"].split()) == 1]
                    elif api_name == "ninjas":
                        return [s for s in data.get("synonyms", []) 
                               if len(s.split()) == 1]
                return []

        except Exception as e:
            logger.error(f"Error with {api_name}: {str(e)}")
            return []

    async def get_word_synonyms(self, word: str, min_synonyms: int = 3) -> Tuple[List[str], List[str]]:
        """
        Get synonyms for a word using multiple APIs if needed
        Args:
            word: Word to find synonyms for
            min_synonyms: Minimum number of synonyms required
        Returns:
            Tuple of (synonyms list, sources list)
        """
        sources = []
        all_synonyms = []

        # Try API Ninjas first
        ninjas_synonyms = await self.get_synonyms_from_api("ninjas", word)
        if ninjas_synonyms:
            all_synonyms.extend(ninjas_synonyms)
            sources.append("ninjas")

        # Try Datamuse if needed
        if len(all_synonyms) < min_synonyms:
            datamuse_synonyms = await self.get_synonyms_from_api("datamuse", word)
            if datamuse_synonyms:
                all_synonyms.extend([s for s in datamuse_synonyms if s not in all_synonyms])
                sources.append("datamuse")

        return all_synonyms, sources

    async def get_combined_synonyms(self, word: str, second_word: Optional[str] = None, 
                                  min_synonyms: int = 3, max_synonyms: int = 10) -> Dict:
        """
        Get synonyms for one or two words
        Args:
            word: Primary word
            second_word: Optional second word for phrases
            min_synonyms: Minimum synonyms required
            max_synonyms: Maximum synonyms to return
        Returns:
            Dictionary with synonym results
        """
        word = word.strip().lower()
        
        # Get synonyms for first word
        first_synonyms, sources = await self.get_word_synonyms(word, min_synonyms)
        
        if not first_synonyms:
            raise HTTPException(
                status_code=404,
                detail=f"No synonyms found for '{word}'. Please try a different word."
            )

        # Limit to max_synonyms
        first_synonyms = first_synonyms[:max_synonyms]
        
        # Handle second word if provided
        second_word_synonyms = None
        if second_word:
            second_word = second_word.strip().lower()
            second_synonyms, second_sources = await self.get_word_synonyms(second_word)
            if second_synonyms:
                second_word_synonyms = second_synonyms[:max_synonyms]
                sources.extend(s for s in second_sources if s not in sources)

        return {
            "word": word,
            "synonyms": first_synonyms,
            "second_word_synonyms": second_word_synonyms,
            "sources": sources,
            "timestamp": datetime.now()
        }

# Initialize FastAPI app
app = FastAPI(
    title="Synonym API",
    description="API for finding synonyms with support for single words and word pairs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize API service
synonym_service = SynonymAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information"""
    return """
    <html>
        <head>
            <title>Synonym API</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 20px; 
                }
                .container { 
                    background-color: #f5f5f5; 
                    padding: 20px; 
                    border-radius: 5px; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to Synonym API</h1>
                <p>This API provides synonyms for words with these features:</p>
                <ul>
                    <li>Single word synonyms with high quality results</li>
                    <li>Optional second word support for phrase building</li>
                    <li>Multiple API sources for comprehensive results</li>
                </ul>
                <h2>Available endpoints:</h2>
                <ul>
                    <li><a href="/docs">/docs</a> - Interactive API documentation</li>
                    <li><a href="/redoc">/redoc</a> - Alternative API documentation</li>
                    <li>/synonyms - POST endpoint for getting synonyms</li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.post("/synonyms", response_model=SynonymResponse)
async def get_synonyms(request: WordRequest):
    """
    Get synonyms for a word with optional second word
    Args:
        request: WordRequest model with word and options
    Returns:
        SynonymResponse with results
    """
    if not request.word.strip():
        raise HTTPException(status_code=400, detail="Word cannot be empty")

    if request.min_synonyms > request.max_synonyms:
        raise HTTPException(
            status_code=400,
            detail="Minimum synonyms cannot be greater than maximum synonyms"
        )

    result = await synonym_service.get_combined_synonyms(
        request.word,
        second_word=request.second_word,
        min_synonyms=request.min_synonyms,
        max_synonyms=request.max_synonyms
    )

    return SynonymResponse(**result)

if __name__ == "__main__":
    import uvicorn
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000)