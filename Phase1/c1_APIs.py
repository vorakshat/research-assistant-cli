'''
import requests

# 1. The CLient prepares the destination (URL) and action (GET)
response = requests.get("https://httpbin.org/json")

# 2. The Client prints the JSON payload sent back by the server
print(response.json())
'''

import os
from dotenv import load_dotenv

# 1. Look for the .env file and load its contents into memory
load_dotenv()

# 2. Safely pull the key using Python's built-in 'os' library
api_key = os.getenv("OPENAI_API_KEY")

# 3. Verify that it worked
print(f"Successfully loaded API Key: {api_key}")