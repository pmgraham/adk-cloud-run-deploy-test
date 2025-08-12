# standard library imports
import json
from uuid import uuid4
import subprocess

# third party imports
import requests


# --- 1. Configuration ---
BASE_URL = "cloud-run-url"
APP_NAME = "travel-planner-app" # should match the APP_NAME variable in the deploy.sh file or request will fail
USER_ID = "sample-user" # this can be anything; used mostly for tracking access patterns in log files.
SESSION_ID = str(uuid4()) # simply creating a unique session id to test the request

PROMPT = "I need a hotel in Atlanta Oct 10 - 20"

try:
    # Execute the gcloud command to get the identity token
    token = subprocess.check_output(
        ['gcloud', 'auth', 'print-identity-token']
    ).decode('utf-8').strip()
    print("Successfully retrieved gcloud auth token.")
except (subprocess.CalledProcessError, FileNotFoundError):
    print("ERROR: Failed to get gcloud auth token.")
    print("Please ensure the gcloud CLI is installed and you are authenticated ('gcloud auth login').")
    exit()

# Define the request headers. You can add a bearer token here if you need to generate an auth token.
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# --- 2. First Request: Create the session ---
print(f"--- Step 1: Creating session '{SESSION_ID}' ---")
url_step1 = f"{BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{SESSION_ID}"
print(f"URL: POST {url_step1}")

# Make the first POST request (no payload needed to create)
response_step1 = requests.post(url_step1, headers=HEADERS)
print(f"Step 1 Status Code: {response_step1.status_code}\n")

# --- 3. Second Request: Run the agent ---
print(f"--- Step 2: Sending message to agent in session '{SESSION_ID}' ---")
url_step2 = f"{BASE_URL}/run_sse" # run_sse is the url you need to submit post requests to for any deployed adk service

# this JSON schema is required for the post request for the adk deployed service
payload_step2 = {
    "app_name": APP_NAME,
    "user_id": USER_ID,
    "session_id": SESSION_ID,
    "new_message": {
        "role": "user",
        "parts": [{
            "text": PROMPT
        }]
    },
    "streaming": False # We want a single response, not a stream
}
print(f"URL: POST {url_step2}")

# Make the second POST request
response_step2 = requests.post(url_step2, headers=HEADERS, json=payload_step2)
print(f"Step 2 Status Code: {response_step2.status_code}")

# --- 4. Parse the Response and Extract the LLM Answer ---

# Get the raw text from the response and remove any leading/trailing whitespace
raw_response_text = response_step2.text.strip()
print(raw_response_text)
# json_string = ""

# # Check if the response starts with the "data:" prefix
# if raw_response_text.startswith("data:"):
#     print("--> SSE 'data:' prefix found. Stripping it before parsing.")
#     # If it does, get the substring that comes AFTER "data: "
#     json_string = raw_response_text.removeprefix("data:").strip()
# else:
#     # Otherwise, assume the whole response is the JSON string
#     json_string = raw_response_text

# # Now, parse the cleaned JSON string into a Python dictionary
# response_json = json.loads(json_string)

# # --- Here is the answer from the LLM ---
# print("\n--- LLM Response ---")

# # Safely access the nested text from the agent's response
# llm_text = "No message found."
# if "content" in response_json and "parts" in response_json["content"]:
#     parts = response_json["content"]["parts"]
#     if parts and "text" in parts[0]:
#         llm_text = parts[0]["text"]

# # print(llm_text)

# formatted_json_response = json.dumps(response_json, indent=4)

# print("\n--- Full Parsed JSON Response ---")
# print(formatted_json_response)

# print("\nScript finished.")
