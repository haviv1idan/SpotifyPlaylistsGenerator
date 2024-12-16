import json

from pathlib import Path

DATA_FILE = Path("users.json")

# Helper functions to interact with the JSON file
def read_users():
    """Read all users from the JSON file."""
    # Ensure the JSON file exists
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w") as f:
            return json.dump([], f)  # Initialize with an empty list
    
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_users(users):
    """Write the list of users to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)
