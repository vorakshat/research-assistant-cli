import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load the vault environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Initialize the official Gemini Client
client = genai.Client(api_key=api_key)

# 3. Define the prompting Structure
# System Instructions give the AI its core persona/rules.
system_instruction = "You are a witty, concise AI Engineering mentor. Answer in 2 sentences max."

# User Content is your actual question.
user_prompt = "Why should an engineer use environment variables?"

print("Sending request to Gemini...")

# 4. Trigger the Request/Response Cycle
response = client.models.generate_content(
    model='gemini-2.5-flash', # The ultra-fast, free-tier standard model
    contents=user_prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.7 # Controls creativity (0.0 is robotic/exact, 1.0 is highly creative)
    # max_output_tokens = An integer value restricting the maximum length of the generation response. Used as a hard budget ceiling.
    # response_mime_type = Forces the model to respond in a strict structural data format rather than standard conversational text.
    # top_k: Forces the model to look only at the top K most probable next words.
    # top_p (Nucleus Sampling): Accumulates the probability of the top choices until they equal a percentage. If top_p=0.95, it looks at the smallest pool of words whose combined likelihood adds up to 95%, cutting off the erratic, strange 5% tail.
    )
)

# 5. Print the text response sent back by the server
print("\n--- Gemini's Response ---")
print(response.text)