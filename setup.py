import subprocess
import os
import sys
import kagglehub

def ask_user_for_confirmation(prompt: str) -> bool:
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == "y":
            return True
        elif user_input == "n":
            return False
        else:
            print("Invalid input. please use only 'y' or 'n'.")

def in_conda() -> bool:
    return "conda" in sys.executable

def in_venv() -> bool:
    # Prüfen, ob das Skript in einer virtuellen Umgebung läuft
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

if __name__ == "__main__":

    if in_conda():
        print("Detected conda environment:", os.environ.get("CONDA_DEFAULT_ENV"))
    elif in_venv():
        print("Detected virtual environment:", sys.prefix)
    else:
        print("No conda environment detected. Aborting...")
        raise EnvironmentError()
    
    print("Starting Setup...")

        subprocess.check_call(
            [
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "-r", 
                os.path.join(
                    os.path.dirname(__file__), 
                    "requirements.txt"
                )
            ]
        )
        # Download latest version
        path = kagglehub.dataset_download("sumn2u/garbage-classification-v2")
        
        print("Path to dataset files:", path)
            print("Done!")


    print("Setup complete!")
