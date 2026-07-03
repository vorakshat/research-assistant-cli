import requests

# 1. The CLient prepares the destination (URL) and action (GET)
response = requests.get("https://httpbin.org/json")

# 2. The Client prints the JSON payload sent back by the server
print(response.json())
