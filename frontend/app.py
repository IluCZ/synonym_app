import streamlit as st
import httpx
from typing import Dict, Optional, Any
import os
import asyncio
from datetime import datetime
import logging

# Configure logging for error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session state for search history
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Backend configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
TIMEOUT_SECONDS = 10.0

# Page configuration
st.set_page_config(
    page_title="Synonym Finder",
    page_icon="📚",
    layout="centered"
)

# Application styling
CUSTOM_CSS = """
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .result-box {
        padding: 20px;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    .word-title {
        color: #0e1117;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .suggestion-box {
        padding: 10px;
        background-color: #e1e5eb;
        border-radius: 3px;
        margin: 5px;
        display: inline-block;
    }
    .history-item {
        padding: 10px;
        margin: 5px 0;
        background-color: #f0f2f6;
        border-radius: 5px;
    }
    .stButton button {
        background-color: #FF8C00;
        color: white;
        border: none;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #FF7000;
    }
    .stTextInput input {
        border: 2px solid #ccc;
        background-color: white;
    }
"""

st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)
st.title("📚 Synonym Finder")

async def get_synonyms(word: str, second_word: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Fetch synonyms from the backend API with error handling
    
    Args:
        word: Primary word to find synonyms for
        second_word: Optional second word for phrase search
        
    Returns:
        Dictionary containing synonyms and metadata, or None if error occurs
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/synonyms",
                json={
                    "word": word,
                    "second_word": second_word,
                    "min_synonyms": min_synonyms,
                    "max_synonyms": max_synonyms
                },
                timeout=TIMEOUT_SECONDS
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.TimeoutError:
            st.error("⏱️ Request timed out. Please try again.")
            logger.error(f"Timeout occurred while fetching synonyms for: {word}")
            return None
            
        except httpx.RequestError as e:
            st.error("🔌 Cannot connect to backend service. Please check if the service is running.")
            logger.error(f"Connection error: {str(e)}")
            return None
            
        except httpx.HTTPStatusError as e:
            error_messages = {
                404: "🔍 No synonyms found for this word.",
                400: "❌ Invalid input. Please check your word and try again.",
                503: f"⚠️ Service temporarily unavailable: {str(e)}",
            }
            st.error(error_messages.get(e.response.status_code, f"⚠️ Server error: {str(e)}"))
            logger.error(f"HTTP error {e.response.status_code}: {str(e)}")
            return None
            
        except Exception as e:
            st.error("💥 An unexpected error occurred. Please try again later.")
            logger.error(f"Unexpected error in get_synonyms: {type(e).__name__}: {str(e)}")
            return None

def add_to_history(input_text: str, results: Dict[str, Any]) -> None:
    """
    Add search results to history with error handling
    
    Args:
        input_text: The searched word(s)
        results: The synonym results from the API
    """
    try:
        st.session_state.search_history.append({
            'input': input_text,
            'results': results,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        logger.error(f"Error adding to history: {str(e)}")
        st.warning("Unable to save to search history")

def clear_input() -> None:
    """Clear the input field"""
    try:
        st.session_state.word = ""
    except Exception as e:
        logger.error(f"Error clearing input: {str(e)}")

def display_word_synonyms(title: str, synonyms: list[str]) -> None:
    """Display synonyms for a word in a formatted box"""
    st.markdown(f"### {title}")
    for synonym in synonyms:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="word-title">{synonym}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def display_suggestions(first_synonyms: list[str], second_synonyms: list[str]) -> None:
    """Display suggested word combinations"""
    st.markdown("### Suggested Combinations")
    suggestions = [
        f"{syn1} {syn2}"
        for syn1 in first_synonyms[:3]
        for syn2 in second_synonyms[:3]
    ]
    
    for suggestion in suggestions:
        st.markdown(
            f'<div class="suggestion-box">{suggestion}</div>',
            unsafe_allow_html=True
        )

# Main input form
with st.form(key="input_form"):
    word = st.text_input(
        "Enter word or phrase",
        help="Enter a single word or multiple words (e.g., 'fast' or 'fast car')",
        key="word"
    )
    
    with st.expander("Advanced Options"):
        col1, col2 = st.columns(2)
        with col1:
            min_synonyms = st.number_input(
                "Minimum synonyms",
                min_value=1,
                max_value=10,
                value=3
            )
        with col2:
            max_synonyms = st.number_input(
                "Maximum synonyms",
                min_value=min_synonyms,
                max_value=10,
                value=10
            )
    
    col3, col4 = st.columns(2)
    with col3:
        submitted = st.form_submit_button("Find Synonyms")
    with col4:
        clear = st.form_submit_button("Clear Input", on_click=clear_input)

# Process form submission
if submitted:
    if not word:
        st.error("Please enter at least one word")
    else:
        try:
            words = word.split()
            input_text = words[0]
            second_word = words[1] if len(words) > 1 else None

            with st.spinner("Finding synonyms..."):
                results = asyncio.run(get_synonyms(
                    input_text.strip(),
                    second_word.strip() if second_word else None
                ))
                
                if results and "synonyms" in results:
                    st.success("Synonyms found!")
                    add_to_history(word, results)
                    
                    if results.get("second_word_synonyms"):
                        col1, col2 = st.columns(2)
                        with col1:
                            display_word_synonyms(f"Synonyms for '{results['word']}'", results["synonyms"])
                        with col2:
                            display_word_synonyms("Synonyms for second word", results["second_word_synonyms"])
                        display_suggestions(results["synonyms"], results["second_word_synonyms"])
                    else:
                        display_word_synonyms(f"Synonyms for '{results['word']}'", results["synonyms"])
                    
                    st.info(f"Sources used: {', '.join(results['sources'])}")
                else:
                    st.warning("No synonyms found or an error occurred.")
                    
        except Exception as e:
            logger.error(f"Error processing form submission: {str(e)}")
            st.error("An error occurred while processing your request. Please try again.")

# Search History section
with st.expander("Search History"):
    try:
        if st.session_state.search_history:
            if st.button("Clear History"):
                st.session_state.search_history = []
                st.experimental_rerun()
            
            for item in reversed(st.session_state.search_history):
                st.markdown(
                    f"""
                    <div class="history-item">
                        <strong>Search:</strong> {item['input']}<br>
                        <strong>Time:</strong> {item['timestamp']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No search history yet")
    except Exception as e:
        logger.error(f"Error displaying search history: {str(e)}")
        st.error("Unable to display search history")

# User Guide section
with st.expander("How to Use"):
    st.markdown("""
    ### Using the Synonym Finder
    
    1. **Input**:
       - Enter a single word or multiple words
       - Examples: "fast" or "fast car"
    
    2. **Advanced Options**:
       - Adjust minimum and maximum number of synonyms
       - Default: min=3, max=10
    
    3. **Features**:
       - Clear button to reset input
       - Search history tracking
       - Combined suggestions for multiple word searches
    
    4. **Tips**:
       - Use clear, specific words for better results
       - Check the history to review past searches
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Created as part of the DocOps Test Task</p>
        <p>Uses multiple API sources for comprehensive results</p>
    </div>
    """,
    unsafe_allow_html=True
)