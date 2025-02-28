import requests
import hashlib
import json
import os

LOCAL_VERSION_FILE = "system/version.json"

def calculate_security_hash(version, release_date):
    """Generate a security hash from version and release date."""
    version_string = f"{version}-{release_date}"
    return hashlib.sha256(version_string.encode()).hexdigest()

def fetch_latest_version():
    """Fetch the latest version.json from GitHub."""
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

def load_local_version():
    """Load the local version.json file."""
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as file:
            return json.load(file)
    else:
        print("Local version file not found.")
        return None

def save_local_version(updated_data):
    """Save the updated local version.json with a new security tag."""
    with open(LOCAL_VERSION_FILE, "w") as file:
        json.dump(updated_data, file, indent=4)
    print("Local version file updated successfully.")

def check_for_updates():
    """Check for updates and insert a security tag if needed."""
    local_version_data = load_local_version()
    if local_version_data is None:
        print("Failed to load local version data.")
        return False

    github_version_data = fetch_latest_version()
    if github_version_data is None:
        print("Failed to fetch latest version data.")
        return False

    # Extract version numbers
    latest_version = github_version_data["version"]
    local_version = local_version_data.get("version", 0)

    # Extract release dates
    latest_release_date = github_version_data["release_date"]
    local_release_date = local_version_data.get("release_date", "")

    # Generate expected security tag
    expected_security_tag = calculate_security_hash(latest_version, latest_release_date)
    
    # Check if local security tag exists and matches
    local_security_tag = local_version_data.get("security", "")
    
    if local_security_tag == expected_security_tag:
        print(f"Security tag is correct: {local_security_tag}")
    else:
        print("⚠️ Security tag mismatch! Updating...")
        local_version_data["security"] = expected_security_tag
        save_local_version(local_version_data)

    # Check for version updates
    if local_version < latest_version:
        print(f"A newer version (v{latest_version}) is available! You are using v{local_version}.")
        return True
    elif local_version == latest_version:
        print(f"You are using the latest version (v{local_version}).")
        return False
    else:
        print(f"⚠️ You are using a newer version (v{local_version}) than the latest release (v{latest_version}).")
        return False