import requests
import hashlib
import json
import os

# Path to the local version file (on the user's system)
LOCAL_VERSION_FILE = "system/version.json"

# Function to calculate a secure hash (e.g., SHA-256) of a string
def calculate_security_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Function to verify the security tag
def verify_security(local_security_tag, github_version_data):
    """
    Verify the security tag by comparing the local security tag with the one generated from GitHub data.
    """
    # Generate the expected security tag from GitHub data
    version_string = f"{github_version_data['version']}-{github_version_data['release_date']}"
    expected_security_tag = calculate_security_hash(version_string)

    # Compare the local and expected security tags
    if local_security_tag == expected_security_tag:
        return True
    else:
        print("Security verification failed! The update may not be official.")
        return False

# Function to fetch the latest version data from GitHub
def fetch_latest_version():
    """
    Fetch the latest version data from GitHub.
    Returns the parsed JSON data if successful, otherwise None.
    """
    version_file_url = "https://raw.githubusercontent.com/Wiktor-M-21/PythonOS/main/system/version.json"
    try:
        response = requests.get(version_file_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch version file from GitHub. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to load the local version data
def load_local_version():
    """
    Load the local version data from the local version file.
    Returns the parsed JSON data if successful, otherwise None.
    """
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as file:
            return json.load(file)
    else:
        print("Local version file not found.")
        return None

# Function to check for updates
def check_for_updates():
    """
    Check for updates by comparing the local version with the latest version from GitHub.
    """
    # Load the local version data
    local_version_data = load_local_version()
    if local_version_data is None:
        print("Failed to load local version data.")
        return False

    # Fetch the latest version data from GitHub
    github_version_data = fetch_latest_version()
    if github_version_data is None:
        print("Failed to fetch latest version data.")
        return False

    # Verify the security tag
    local_security_tag = local_version_data.get("security", "")
    if not verify_security(local_security_tag, github_version_data):
        print("Security verification failed. The update may not be official.")
        return False

    # Compare versions
    latest_version = github_version_data["version"]
    local_version = local_version_data["version"]

    if local_version < latest_version:
        print(f"A newer version (v{latest_version}) is available! You are using v{local_version}.")
        return True
    elif local_version == latest_version:
        print(f"You are using the latest version (v{local_version}).")
        return False
    else:
        print(f"You are using a newer version (v{local_version}) than the latest release (v{latest_version}).")
        return False

# Run the update check
check_for_updates()