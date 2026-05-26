import os
from dotenv import load_dotenv

# A sample data-cleaning helper utility function you might use in your CLI
def format_user_query(raw_string):
    return raw_string.strip().capitalize()

# --- ACTUAL TESTING FUNCTIONS ---

def test_query_formatting():
    """Test that our input string utility cleans whitespace and capitalizes properly."""
    sample_input = "  what is machine learning?   "
    cleaned_output = format_user_query(sample_input)
    
    # 'assert' checks if a condition evaluates to True. If it fails, the test fails.
    assert cleaned_output == "What is machine learning?"

def test_env_loading():
    """Verify that the virtual environment successfully exposes our API Key."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    assert api_key is not None, "Testing Failed: GEMINI_API_KEY is missing from your .env file!"