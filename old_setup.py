import subprocess
import os
import sys
import datetime
from pathlib import Path

def ask_user_for_confirmation(prompt: str) -> bool:
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == "y":
            return True
        elif user_input == "n":
            return False
        else:
            print("Invalid input. please use only 'y' or 'n'.")

def check_and_install_requirements():
    """Prueft ob requirements installiert sind und installiert sie falls noetig"""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print("No requirements.txt found. Skipping dependency installation.")
        return True
    
    # Pruefe ob kagglehub bereits installiert ist
    try:
        import kagglehub
        print("kagglehub is already installed.")
        return True
    except ImportError:
        print("kagglehub not found. Installing requirements...")
        try:
            subprocess.check_call(
                [
                    sys.executable, 
                    "-m", 
                    "pip", 
                    "install", 
                    "-r", 
                    requirements_path
                ]
            )
            print("Requirements installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install requirements: {e}")
            return False

def check_dataset_exists(dataset_path: Path) -> bool:
    """Prueft ob der Dataset-Ordner existiert und Dateien enthaelt"""
    if not dataset_path.exists():
        return False
    
    try:
        files = list(dataset_path.glob("*"))
        return len(files) > 0
    except:
        return False

def is_dataset_recent(dataset_path: Path, max_age_days: int = 7) -> bool:
    """Prueft ob der Dataset in den letzten X Tagen aktualisiert wurde"""
    if not dataset_path.exists():
        return False
    
    last_modified = datetime.datetime.fromtimestamp(dataset_path.stat().st_mtime)
    age = datetime.datetime.now() - last_modified
    return age.days < max_age_days

def download_dataset(dataset_name: str) -> str:
    """Laedt den Dataset herunter oder gibt den Pfad zurueck"""
    try:
        import kagglehub
        
        # Versuche den lokalen Cache-Pfad zu finden
        cache_dir = Path.home() / ".cache" / "kagglehub" / "datasets"
        dataset_dir = cache_dir / dataset_name.replace("/", "-")
        
        if check_dataset_exists(dataset_dir) and is_dataset_recent(dataset_dir):
            print(f"Dataset '{dataset_name}' is already downloaded and recent (less than 7 days old).")
            print(f"   Path: {dataset_dir}")
            answer = ask_user_for_confirmation("Do you want to re-download anyway? (y/n): ")
            if answer:
                print("Re-downloading dataset...")
                path = kagglehub.dataset_download(dataset_name)
                print("Path to dataset files:", path)
                return path
            else:
                print("Using existing dataset.")
                return str(dataset_dir)
        else:
            if dataset_dir.exists() and not is_dataset_recent(dataset_dir):
                print(f"Dataset exists but is older than 7 days.")
            else:
                print(f"Dataset not found locally.")
            
            print("Downloading dataset...")
            path = kagglehub.dataset_download(dataset_name)
            print("Path to dataset files:", path)
            return path
            
    except ImportError:
        print("ERROR: kagglehub is not installed. Please install requirements first.")
        raise
    except Exception as e:
        print(f"Error checking dataset: {e}")
        print("Attempting fresh download...")
        try:
            import kagglehub
            path = kagglehub.dataset_download(dataset_name)
            print("Path to dataset files:", path)
            return path
        except Exception as e2:
            print(f"Failed to download dataset: {e2}")
            raise

if __name__ == "__main__":
    
    print("Python version:", sys.version)
    print("Python executable:", sys.executable)
    print("\nStarting Setup...")

    # Zuerst requirements installieren/pruefen
    if not check_and_install_requirements():
        print("Setup failed: Could not install requirements.")
        sys.exit(1)

    # Jetzt kann kagglehub importiert werden
    print("\nChecking dataset...")
    dataset_name = "sumn2u/garbage-classification-v2"
    
    try:
        dataset_path = download_dataset(dataset_name)
        print("\nSetup complete!")
        print(f"Dataset location: {dataset_path}")
    except Exception as e:
        print(f"\nSetup failed: {e}")
        sys.exit(1)