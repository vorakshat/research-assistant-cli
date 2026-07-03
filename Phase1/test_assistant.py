import os
import pytest
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv

# Import the core functions directly from your assistant script
from Phase1.research_assistant import conduct_research, initialize_assistant

# TEST 1: isolated environment and config validation
def test_env_loading():
    """Verify that the virtual environment successfully exposes our API Key vault."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    assert api_key is not None, "Testing Failed: GEMINI_API_KEY is missing from your .env file!"

# TEST 2: SIMULATING A SUCCESSFUL API CYCLE (200 OK)
# @patch intercepts the SDK client network call and replaces it with a fake
@patch("google.genai.Client")
def test_conduct_research_success(mock_client_class, caplog): # mock_client_class is a fake version of google.genai.Client
    """Simulates a flawless API call to ensure successful logs are firing."""
    
    # 1. Setup our Fake/Mocked response structure
    mock_response = MagicMock() # MagicMock is a blank-slate object provided by Python. You can tap any attribute onto it out of thin air, and it will just accept it.
    mock_response.text = "## SUMMARY\nFake summary data\n\n## KEY POINTS\n* Point 1\n\n## SUGGESTED FOLLOW-UP QUESTIONS\n* Question 1"
    
    # 2. Configure the fake client to return our fake response when called
    mock_client_instance = mock_client_class.return_value
    mock_client_instance.models.generate_content.return_value = mock_response

    # 3. Execute the function using the caplog context wrapper (captures logging streams)
    with caplog.at_level("INFO"):
        conduct_research(mock_client_instance, topic="Vector Embeddings")

    # 4. ASSERTIONS: Verify that our expected success log statements actually fired
    assert "Preparing payload for network dispatch." in caplog.text
    assert "Dispatching HTTP POST request via SDK to Gemini remote servers..." in caplog.text
    assert "HTTP Response package successfully received and parsed." in caplog.text
    
# TEST 3: SIMULATING A SERVER CRASH OR TIMEOUT (500/Connection Error)
@patch("google.genai.Client")
def test_conduct_research_api_failure(mock_client_class, caplog):
    """Forces the API network call to raise an Exception to verify error logs fire."""

    # 1. Force the fake client's generate method to violently crash with an exception
    mock_client_instance = mock_client_class.return_value
    mock_client_instance.models.generate_content.side_effect = Exception("Simulated Network Timeout")

    # 2. Run the function under the logging scanner
    with caplog.at_level("ERROR"):
        conduct_research(mock_client_instance, topic="Quantum Computing")

    # 3. ASSERTIONS: Verify the try/except layer caught it cleanly and logged the ERROR level
    assert "Network call failed or timed out! API Exception Details:" in caplog.text
    assert "Simulated Network Timeout" in caplog.text

# TEST 4: EDGE CASE - EMPTY USER STRINGS
@patch("google.genai.Client")
def test_conduct_research_empty_input(mock_client_class, caplog):
    """Verifies that input validation handles empty space strings gracefully."""
    mock_client_instance = mock_client_class.return_value
    
    with caplog.at_level("WARNING"):
        conduct_research(mock_client_instance, topic="   ")

    # Verify our input validation script issued a warning log instead of hitting the network
    assert "User submitted an empty input string." in caplog.text
    mock_client_instance.models.generate_content.assert_not_called()
    