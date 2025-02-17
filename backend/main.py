import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
from typing import List, Dict, Set, Optional, Union
from datetime import datetime
import logging

# Load environment variables
load_dotenv()

# Configure logging for tracking errors and events
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WordRequest(BaseModel):
    """Request model for synonym lookup with validation"""
    word: str = Field(..., min_length=1, max_length=100, description="Word to find synonyms for")
    second_word: Optional[str] = Field(None, max_length=100, description="Optional second word")
    min_synonyms: int = Field(default=3, ge=1, le=10, description="Minimum number of synonyms")
    max_synonyms: int = Field(default=10, ge=1, le=10, description="Maximum number of synonyms")

class SynonymResponse(BaseModel):
    """Response model for synonym results"""
    word: str
    synonyms: List[str]
    second_word_synonyms: Optional[List[str]] = None
    sources: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)

# Custom exceptions for better error handling
class SynonymAPIError(Exception):
    """Base exception for API errors"""
    pass

class ExternalAPIError(SynonymAPIError):
    """Exception for external API failures"""
    def __init__(self, api_name: str, message: str):
        self.api_name = api_name
        self.message = message
        super().__init__(f"{api_name}: {message}")

class NoSynonymsFound(SynonymAPIError):
    """Exception when no synonyms are found"""
    pass

class SynonymAPI:
    def __init__(self) -> None:
        # Primary and fallback API configurations
        self.apis: Dict[str, Dict] = {
            "datamuse": {
                "url": "https://api.datamuse.com/words",
                "params": lambda word: {
                    "ml": word,
                    "rel_syn": word,
                    "max": 15
                }
            },
            "ninjas": {
                "url": "https://api.api-ninjas.com/v1/thesaurus",
                "params": lambda word: {"word": word},
                "headers": {
                    "X-Api-Key": os.getenv('API_NINJAS_KEY')
                }
            }
        }
        self.cache: Dict[str, Dict] = {}

    async def get_synonyms_from_api(self, api_name: str, word: str) -> List[str]:
        """
        Fetch and process synonyms from a specific API
        
        Args:
            api_name: Name of the API to use
            word: Word to find synonyms for
            
        Returns:
            List of synonyms
            
        Raises:
            ExternalAPIError: When API request fails
        """
        if not isinstance(word, str):
            raise ValueError("Word must be a string")

        try:
            async with httpx.AsyncClient() as client:
                api_config = self.apis[api_name]
                request_kwargs = {
                    "params": api_config["params"](word),
                    "timeout": 5.0
                }
                
                if "headers" in api_config:
                    request_kwargs["headers"] = api_config["headers"]

                logger.info(f"Requesting synonyms for '{word}' from {api_name}")
                response = await client.get(api_config["url"], **request_kwargs)
                
                if not response.is_success:
                    raise ExternalAPIError(api_name, f"HTTP {response.status_code}")

                data = response.json()
                synonyms: List[str] = []

                try:
                    if api_name == "datamuse":
                        synonyms = [item["word"] for item in data if "word" in item 
                                and len(item["word"].split()) == 1]
                    elif api_name == "ninjas":
                        synonyms = [s for s in data.get("synonyms", []) 
                                if len(s.split()) == 1]
                except KeyError as e:
                    raise ExternalAPIError(api_name, f"Invalid response format: {str(e)}")

                logger.info(f"Found {len(synonyms)} synonyms from {api_name}")
                return synonyms if synonyms else []

        except httpx.TimeoutError:
            raise ExternalAPIError(api_name, "Request timeout")
        except httpx.RequestError as e:
            raise ExternalAPIError(api_name, f"Request failed: {str(e)}")
        except Exception as e:
            raise ExternalAPIError(api_name, f"Unexpected error: {str(e)}")

    async def get_combined_synonyms(
        self, 
        word: str, 
        second_word: Optional[str] = None,
        min_synonyms: int = 3, 
        max_synonyms: int = 10
    ) -> Dict:
        """
        Get synonyms from multiple API sources with fallback support
        
        Args:
            word: Primary word to find synonyms for
            second_word: Optional second word for phrase synonyms
            min_synonyms: Minimum number of synonyms required
            max_synonyms: Maximum number of synonyms to return
            
        Returns:
            Dictionary containing synonyms and metadata
            
        Raises:
            NoSynonymsFound: When minimum number of synonyms not found
        """
        word = word.strip().lower()
        sources: List[str] = []
        all_synonyms: Set[str] = set()
        errors: List[str] = []

        # Try each API for the first word
        for api_name in self.apis:
            try:
                synonyms = await self.get_synonyms_from_api(api_name, word)
                if synonyms:
                    all_synonyms.update(synonyms)
                    sources.append(api_name)
            except ExternalAPIError as e:
                errors.append(str(e))
                logger.warning(f"API error: {str(e)}")
                continue

        # Process second word if provided
        second_word_synonyms = None
        if second_word:
            second_word = second_word.strip().lower()
            second_synonyms: Set[str] = set()
            
            for api_name in self.apis:
                try:
                    synonyms = await self.get_synonyms_from_api(api_name, second_word)
                    if synonyms:
                        second_synonyms.update(synonyms)
                        if api_name not in sources:
                            sources.append(api_name)
                except ExternalAPIError as e:
                    errors.append(str(e))
                    continue
            
            if second_synonyms:
                second_word_synonyms = list(second_synonyms)[:max_synonyms]

        # Check if we have enough synonyms
        if len(all_synonyms) < min_synonyms:
            error_msg = f"Not enough synonyms found for '{word}'"
            if errors:
                error_msg += f" (API Errors: {', '.join(errors)})"
            raise NoSynonymsFound(error_msg)

        return {
            "word": word,
            "synonyms": list(all_synonyms)[:max_synonyms],
            "second_word_synonyms": second_word_synonyms,
            "sources": sources,
            "timestamp": datetime.now()
        }

app = FastAPI(
    title="Synonym API",
    description="API for finding synonyms with support for single words and word pairs",
    version="1.0.0"
)

# CORS middleware is needed for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

synonym_service = SynonymAPI()

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/synonyms", response_model=SynonymResponse)
async def get_synonyms(request: WordRequest) -> SynonymResponse:
    """Get synonyms for a word with optional second word"""
    try:
        result = await synonym_service.get_combined_synonyms(
            request.word,
            second_word=request.second_word,
            min_synonyms=request.min_synonyms,
            max_synonyms=request.max_synonyms
        )
        return SynonymResponse(**result)

    except NoSynonymsFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExternalAPIError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)