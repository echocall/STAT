import datetime
from pathlib import Path

def log_startup_event(message: str):
    log_path = Path("startup.log")  # You can change this path if desired
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_path.open("a") as f:
        f.write(f"[{timestamp}] {message}\n")

def log_startup_event(message: str):
    _write_log("startup.log", message)

def log_startup_error(error: Exception):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [ERROR] {type(error).__name__}: {error}"
    _write_log("startup.log", log_message)

def _write_log(filename: str, message: str):
    log_path = Path(filename)
    with log_path.open("a") as f:
        f.write(f"{message}\n")
