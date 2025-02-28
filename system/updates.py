import requests
import hashlib
import json
import os

# Path to the local version file (e.g., stored in your OS)
LOCAL_VERSION_FILE = "system/local_version.json"

# Function to calculate a secure hash (e.g., SHA-256) of a string
def calculate_security_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Function to verify the security tag
def verify_security(version_data):
    provided_security_tag = version_data.get("security", "")

    # Recalculate the expected security hash
    version_string = f"{version_data['version']}-{version_data['release_date']}"
    expected_security_tag = calculate_security_hash(version_string)

    if provided_security_tag == expected_security_tag:
        return True
    else:
        print("Security verification failed! The update may not be official.")
        return False

# Function to fetch the latest version data from GitHub
def fetch_latest_version():
    version_file_url = "https://raw.githubusercontent.com/Wiktor-M-21/PythonOS/main/system/version.json"
    try:
        print("Fetching latest version data from GitHub...")
        response = requests.get(version_file_url)
        if response.status_code == 200:
            print("Successfully fetched version data.")
            return response.json()  # Parse the JSON response
        else:
            print(f"Failed to fetch version file from GitHub. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def load_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        print("Loading local version data...")
        with open(LOCAL_VERSION_FILE, "r") as file:
            return json.load(file)
    else:
        print("Local version file not found.")
        return None

def check_for_updates():
    print("Checking for updates...")
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

    # Compare versions
    latest_version = latest_version_data["version"]
    local_version = local_version_data["version"]

    if local_version < latest_version:
        print(f"A newer version (v{latest_version}) is available! You are using v{local_version}.")
        return True
    elif local_version == latest_version:
        print(f"You are using the latest version (v{local_version}).")
        return False
    else:
        print(f"You are using a newer version (v{local_version}) than the latest release (v{latest_version}).")

check_for_updates()