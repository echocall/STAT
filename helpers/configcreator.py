import configparser
from pathlib import Path
from platform import system
import os

# Load config
config_path = Path("config.txt")
config = configparser.ConfigParser()
config.optionxform = str  # Preserve case for keys

def write_config():
    # Write updated config
    with config_path.open("w") as f:
        config.write(f)

def set_paths():
    if config_path.exists():
        config.read(config_path)
    else:
        config["Preferences"] = {}
        config["Paths"] = {}
        config["Toggles"] = {}

    defaultrootpath = get_default_install_path("STAT")

    config["Paths"]["defaultrootpath"] = defaultrootpath
    config["Paths"]["osrootpath"] = defaultrootpath
    config["Paths"]["gamespath"] = defaultrootpath + "\STAT\statassets\games"
    config["Paths"]["templatespath"] = defaultrootpath + "\STAT\statassets\\templates"
    config["Paths"]["assetspath"] = "\\assets"
    config["Paths"]["effectspath"] = "\\effects"
    config["Paths"]["eventspath"] = "\\events"
    config["Paths"]["imagespath"] = "\\images"


def get_default_install_path(app_name) -> str:
    # using sytem to check which operating system
    if system == "Windows":
        primary_path = Path("C:/Program Files") / app_name
        fallback_path = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / app_name
    elif system == "Darwin":  # macOS
        primary_path = Path("/Applications") / app_name
        fallback_path = Path.home() / "Applications" / app_name
    elif system == "Linux":
        primary_path = Path("/opt") / app_name
        fallback_path = Path.home() / f".local/share/{app_name}"
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

    # Try primary path, fallback to user path if not writable
    try:
        primary_path.mkdir(parents=True, exist_ok=True)
        test_file = primary_path / ".write_test"
        test_file.touch()
        test_file.unlink()
        return primary_path
    except PermissionError:
        fallback_path.mkdir(parents=True, exist_ok=True)
        return fallback_path