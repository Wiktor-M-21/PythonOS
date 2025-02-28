import requests
import hashlib
import json
import os

LOCAL_VERSION_FILE = "system/version.json"

def calculate_security_hash(version, release_date):
    """Generate a SHA-256 security hash based on version and release date."""
    version_string = f"{version}-{release_date}"
    return hashlib.sha256(version_string.encode()).hexdigest()

def verify_security(local_security_tag, github_version_data):
    """Verify security by generating a hash from GitHub data and comparing it to the local tag."""
    expected_security_tag = calculate_security_hash(
        github_version_data["version"], github_version_data["release_date"]
    )
    
    if local_security_tag == expected_security_tag:
        return True
    else:
        print("Security verification failed! The update may not be official.")
        return False

def fetch_latest_version():
    """Fetch the latest version information from GitHub."""
    version_file_url = "https://raw.githubusercontent.com/Wiktor-M-21/PythonOS/main/system/version.json"
    try:
        response = requests.get(version_file_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to fetch version file from GitHub. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return None

def load_local_version():
    """Load the local version file."""
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as file:
            return json.load(file)
    else:
        print("⚠️ Local version file not found.")
        return None

def check_for_updates():
    """Check if a newer version is available and verify security."""
    local_version_data = load_local_version()
    if local_version_data is None:
        print("❌ Failed to load local version data.")
        return False

    github_version_data = fetch_latest_version()
    if github_version_data is None:
        print("❌ Failed to fetch latest version data.")
        return False

    # Verify security using the expected hash from GitHub data
    local_security_tag = local_version_data.get("security", "")
    if not verify_security(local_security_tag, github_version_data):
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
        print(f"⚠️ You are using a newer version (v{local_version}) than the latest release (v{latest_version}).")
        return False

# Run update check
check_for_updates()