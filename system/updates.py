import json
import requests
import hashlib
import rsa

# URL of the remote version.json file
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/Wiktor-M-21/PythonOS/main/system/version.json"
REMOTE_SIGNATURE_URL = "https://raw.githubusercontent.com/Wiktor-M-21/PythonOS/main/system/signature.sig"
# Path to the local version.json file
LOCAL_VERSION_PATH = "version.json"
# Path to the public key
PUBLIC_KEY_PATH = "public_key.pem"

def load_local_version():
    try:
        with open(LOCAL_VERSION_PATH, "r") as file:
            return file.read()
    except FileNotFoundError:
        print("Local version file not found.")
        return None

def load_remote_version():
    try:
        response = requests.get(REMOTE_VERSION_URL, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching remote version: {e}")
        return None

def load_remote_signature():
    try:
        response = requests.get(REMOTE_SIGNATURE_URL, timeout=5)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching signature: {e}")
        return None

def verify_signature(version_data, signature):
    try:
        with open(PUBLIC_KEY_PATH, "rb") as key_file:
            public_key = rsa.PublicKey.load_pkcs1(key_file.read())

        version_hash = hashlib.sha256(version_data.encode()).digest()
        rsa.verify(version_hash, signature, public_key)
        return True
    except rsa.VerificationError:
        print("Version file verification failed!")
        return False
    except FileNotFoundError:
        print("Public key not found.")
        return False

def check_for_update():
    local_data = load_local_version()
    remote_data = load_remote_version()
    remote_signature = load_remote_signature()

    if not local_data or not remote_data or not remote_signature:
        return

    if verify_signature(remote_data, remote_signature):
        local_version = json.loads(local_data).get("version", 0)
        remote_version = json.loads(remote_data).get("version", 0)
        release_date = json.loads(remote_data).get("release_date", "Unknown release date")
        
        if remote_version > local_version:
            print(f"Update available! New version: {remote_version}")
            print(f"Changelog: {json.loads(remote_data).get('changelog', 'No changelog available.')}")
            print(f"Release date: {release_date}")
        else:
            print("You are up to date.")
    else:
        print("The installed version.json is NOT legitimate!")

if __name__ == "__main__":
    check_for_update()