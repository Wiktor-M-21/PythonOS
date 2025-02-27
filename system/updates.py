import requests
import hashlib
import json
import os

# Path to the local version file (e.g., stored in your OS)
LOCAL_VERSION_FILE = "local_version.json"

# Function to calculate a secure hash (e.g., SHA-256) of a string
def calculate_security_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Function to verify the security tag
def verify_security(version_data):
    # Extract the security tag from the version data
    provided_security_tag = version_data.get("security", "")
    
    # Calculate the expected security tag
    version_string = f"{version_data['version']}-{version_data['release_date']}"
    expected_security_tag = calculate_security_hash(version_string)
    
    # Compare the provided and expected security tags
    if provided_security_tag == expected_security_tag:
        return True
    else:
        print("Security verification failed! The update may not be official.")
        return False

# Function to fetch the latest version data from GitHub
def fetch_latest_version():
    version_file_url = "https://raw.githubusercontent.com/Wiktor-M-21/PythonOS/main/system/version.json"
    try:
        response = requests.get(version_file_url)
        if response.status_code == 200:
            return response.json()  # Parse the JSON response
        else:
            print("Failed to fetch version file from GitHub.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to load the local version data
def load_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as file:
            return json.load(file)
    else:
        print("Local version file not found.")
        return None

# Function to check for updates
def check_for_updates():
    # Fetch the latest version data from GitHub
    latest_version_data = fetch_latest_version()
    if latest_version_data is None:
        print("Failed to fetch latest version data.")
        return

    # Verify the security tag
    if not verify_security(latest_version_data):
        print("Security verification failed. The update may not be official.")
        return

    # Load the local version data
    local_version_data = load_local_version()
    if local_version_data is None:
        print("Failed to load local version data.")
        return