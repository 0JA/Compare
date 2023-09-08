import os
import subprocess
import argparse
from settings import CONFIG

def fetch_packages(env_type):
    '''Fetch packages based on environment type (global or virtual).'''
    print("Current working directory:", os.getcwd())

    # Derive the absolute path for the output file based on environment type
    if env_type == "global":
        output_file_path = os.path.join(CONFIG['OUTPUT_DIRECTORY'], CONFIG['GLOBALENV_FILENAME'])
        command = ["pip", "list", "--format=freeze"]
    else:  # "virtual"
        output_file_path = os.path.join(CONFIG['OUTPUT_DIRECTORY'], CONFIG['VIRTUALENV_FILENAME'])
        pip_path = os.path.join("Sandbox", "Scripts", "pip")
        command = [pip_path, "list", "--format=freeze"]

    # Create the output directory if it doesn't exist
    os.makedirs(CONFIG['OUTPUT_DIRECTORY'], exist_ok=True)

    result = subprocess.run(command, capture_output=True, text=True)
    
    with open(output_file_path, "w") as f:
        f.write(result.stdout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch packages from global or virtual environment.")
    parser.add_argument("env_type", choices=["global", "virtual"], help="Specify the environment type: global or virtual.")
    args = parser.parse_args()

    fetch_packages(args.env_type)