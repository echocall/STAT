import configparser
from pathlib import Path
from platform import system
import os
import sys
from nicegui import app

# Helper for PyInstaller compatibility
def resource_path(relative_path: str) -> Path:
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        base_path = Path(".").resolve()
    return base_path / relative_path

# Global config path and config object 
config_path = resource_path("config.txt")
config = configparser.ConfigParser()
# preserve case
config.optionxform = str  

def write_config():
    with config_path.open("w") as f:
        config.write(f)

def set_paths():
    if config_path.exists():
        config.read(config_path)
    else:
        # Create with default sections and paths
        config["Preferences"] = {
            "darkmode": "True",
            "font": "NotoSerif"
        }
        config["Paths"] = {
            "assetspath": "\\assets",
            "effectspath": "\\effects",
            "eventspath": "\\events",
            "imagespath": "\\images"
        }
        config["Toggles"] = {
            "firstsetup": "False",
            "showwelcome": "False",
            "showexplanations": "True",
            "customroot": "False"
        }

   # Only reset root paths if user hasn't set a custom one
    if config["Toggles"].get("customroot", "False") != "True":
        defaultrootpath = get_default_install_path("STAT")
        config["Paths"]["defaultrootpath"] = str(defaultrootpath)
        config["Paths"]["osrootpath"] = str(defaultrootpath)
        config["Paths"]["gamespath"] = "/statassets/games"
        config["Paths"]["templatespath"] = "/statassets/templates"

    # Write config if it was just created or modified
    write_config()

def get_default_install_path(app_name) -> Path:
    if system() == "Windows":
        primary_path = Path("C:/Program Files") / app_name
        fallback_path = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / app_name
    elif system() == "Darwin":  # macOS
        primary_path = Path("/Applications") / app_name
        fallback_path = Path.home() / "Applications" / app_name
    elif system() == "Linux":
        primary_path = Path("/opt") / app_name
        fallback_path = Path.home() / f".local/share/{app_name}"
    else:
        raise RuntimeError(f"Unsupported OS: {system()}")

    try:
        primary_path.mkdir(parents=True, exist_ok=True)
        test_file = primary_path / ".write_test"
        test_file.touch()
        test_file.unlink()
        return primary_path
    except PermissionError:
        fallback_path.mkdir(parents=True, exist_ok=True)
        return fallback_path

def load_config(config_file: str) -> dict:
    configParser = configparser.ConfigParser()
    configParser.read(config_file)

    config_dict = {}
    for section in configParser.sections():
        config_dict[section] = dict(configParser[section])
    return config_dict

def get_config_as_dict(configfilename: str) -> dict:
    config_path = resource_path(configfilename)
    if not os.path.exists(config_path):
        create_default_config(configfilename)
    return load_config(config_path)

def save_config(config_dict: dict, configfilename: str):
    config = configparser.ConfigParser()
    for section, entries in config_dict.items():
        config[section] = entries
    with open(resource_path(configfilename), 'w') as configfile:
        config.write(configfile)

def create_default_config(configfilename: str):
    config = configparser.ConfigParser()

    default_root = get_default_install_path("STAT")

    config["Preferences"] = {
        "darkmode": "True",
        "font": "NotoSerif"
    }

    config["Paths"] = {
        "osrootpath":  str(default_root),
        "defaultrootpath":  str(default_root),
        "customosrootpath": "",
        "templatespath": "/statassets/templates",
        "gamespath": "/statassets/games",
        "debugpath": "/statassets",
        "savespath": "/saves",
        "assetspath": "/assets",
        "defaultassetspath": "/assets/default",
        "customassetspath": "/assets/custom",
        "effectspath": "/effects",
        "defaulteffectspath": "/effects/default",
        "customeffectspath": "/effects/custom",
        "eventspath": "/events",
        "defaulteventspath": "/events/default",
        "customeventspath": "/events/custom",
        "imagespath": "/images"
    }

    config["Toggles"] = {
        "firstsetup": "False",
        "showwelcome": "False",
        "showexplanations": "True",
        "customroot": "False"
    }

    # Write to file
    with open(resource_path(configfilename), 'w') as configfile:
        config.write(configfile)


config.read(config_path)

# Export these
__all__ = ["set_paths", "write_config", "config", "config_path", "load_config", "save_config", "create_default_config" ]
