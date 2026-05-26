import os
import sys
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Logging and Initial Configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'), # Permanently tracks history
        logging.StreamHandler(sys.stdout) # Displays ststus in terminal
    ]
)

# Force the Google GenAI SDK logger to only speak up if there is a WARNING or ERROR
logging.getLogger("google.genai").setLevel(logging.WARNING)

def initialize_assistant() -> genai.Client:
    """Loads environment variables and returns an initialized Gemini client."""
    logging.info("Initializing environment variables...")
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_actual_free_gemini_key_here":
        logging.critical("CRITICAL: GEMINI_API_KEY is missing or unconfigured in .env file.")
        print('\n[Configuration Error]: Please set a valid GEMINI_API_KEY inside your local .env file.')
        sys.exit(1)

    logging.info("Vault security verification passed. API Key located.")

    # Initialize and return the official Google GenAI SDK Client
    return genai.Client(api_key=api_key)

# 2. Core Research Assistant Logic

def conduct_research(client: genai.Client, topic: str):
    """Packages the research prompt with explicit system guidelines and hits the API"""

    # Strict core constrains that sit completely above conversational text
    system_instruction = (
        "You are an elite, highly structured Research Assistant CLI tool.\n"
        "Your task is to analyze the user's topic and return your response split "
        "EXPLICITLY into the following three Markdown sections:\n\n"
        "## SUMMARY\n"
        "[Provide a concise, clear 3-4 sentence overview of the topic]\n\n"
        "## KEY POINTS\n"
        "[List exactly 4 crucial concepts or key takeaways using bullet points]\n\n"
        "## SUGGESTED FOLLOW-UP QUESTIONS\n"
        "[Provide exactly 3 logical, deep questions the user could research next]"
    )

    # Simple input validation utility
    cleaned_topic = topic.strip()
    if not cleaned_topic:
        logging.warning("User submitted an empty input string.")
        print("[Warning]: Topic cannot be empty. Please enter something meaningful.")
        return
    
    logging.info(f"Preparing payload for network dispatch. Topic: '{cleaned_topic}'")

    # Graceful Error Handling Layer to weap the network Request/Response Cycle
    try: 
        logging.info("Dispatching HTTP POST request via SDK to Gemini remote servers...")
        print("\n⏳ Fetching analysis from Gemini servers... Please wait.\n")

        response = client.models.generate_content(
            model='gemini-2.5-flash', # Blazing fast, free-tier optimized brain
            contents=cleaned_topic,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3 # Low temperature for accurate, analytical, structured layouts
            )
        )

        logging.info("HTTP Response package successfully received and parsed.")
        
        # Displaying the final markdown structured text directly to the user
        print("=" * 50)
        print(response.text)
        print("=" * 50)
        
    except Exception as e:
        # Prevents violent script crashes, logs the backtrace info, and keeps app stable
        logging.error(f"Network call failed or timed out! API Exception Details: {e}")
        print("\n❌[System Error]: Unable to reach Gemini servers right now.")
        print("Please verify your internet connection or check 'app.log' for details.")


# 3. Interactive CLI Runtime Loop

def main():
    # Initialize our SDK configuration securely
    client = initialize_assistant()
    
    print("\nWelcome to your Personal Research Assistant CLI!")
   
     # Enter an interactive loop so the user can query multiple things without restarting
    while True:
        try:
            print("\nWhat topic would you like to investigate today?")
            user_input = input("Research Topic (or type 'exit' to quit) -> ")
            
            if user_input.strip().lower() == 'exit':
                logging.info("User requested runtime exit sequence.")
                print("\nGoodbye! Happy engineering.")
                break
                
            conduct_research(client, topic=user_input)
            
        except KeyboardInterrupt:
            # Catching Ctrl+C exits gracefully without displaying a massive stack trace
            logging.info("User forced termination via KeyboardInterrupt.")
            print("\n\nSession terminated cleanly. Goodbye!")
            break

if __name__ == "__main__":
    main()