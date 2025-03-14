import requests
import json
import os


try:
    import rsa
except ImportError as e:
    print("To continue, you must install rsa")
    os.system("pip3 install rsa")
    import rsa

# Constants
VERSION_FILE = "system/version.json"
UPDATE_URL = "https://raw.githubusercontent.com/Wiktor-M-21/PythonOS/main/system/version.json"
PUBLIC_KEY_PATH = "system/public_key.pem"  # Store your public key here

# Load public key
def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())

# Verify signature
def verify_signature(data: str, signature: bytes, public_key):
    try:
        rsa.verify(data.encode(), signature, public_key)
        return True
    except rsa.VerificationError:
        return False

# Get the current local version
def get_local_version():
    if not os.path.exists(VERSION_FILE):
        return None
    with open(VERSION_FILE, "r") as f:
        return json.load(f)

# Save new version locally as an exact copy of version.json
def save_new_version(version_data):
    with open(VERSION_FILE, "w") as f:
        json.dump(version_data, f, indent=4)

# Fetch the latest update
def fetch_latest_version():
    response = requests.get(UPDATE_URL)
    if response.status_code == 200:
        return response.json()
    return None

# Check for updates
def check_for_updates():
    print("Checking for updates...")
    latest_version = fetch_latest_version()
    if not latest_version:
        print("Failed to retrieve update information.")
        return True
    
    local_version = get_local_version()
    
    # Ensure update is legit
    public_key = load_public_key()
    signature = bytes.fromhex(latest_version.get("signature", ""))
    version_data = json.dumps({k: v for k, v in latest_version.items() if k != "signature"}, separators=(",", ":"))
    
    if not verify_signature(version_data, signature, public_key):
        print("Update verification failed! Possible tampering detected.")
        return True
    
    # Compare versions
    if local_version and local_version == latest_version:
        print("You are already on the latest version.")
        return True
    
    print(f"New update available! Version {latest_version['Major version']}.{latest_version['Detailed Version']}")
    print("Changelog:")
    for change in latest_version["changelog"].split(","):
        print(f"- {change.strip()}")
    return False
        

if __name__ == "__main__":
    check_for_updates()
