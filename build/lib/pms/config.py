import os
import configparser

CONFIG_DIR = os.path.expanduser("~/.pms")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config")

def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)

def save_token(token, base_url):
    ensure_config_dir()
    config = configparser.ConfigParser()
    config["auth"] = {
        "access_token": token,
        "base_url": base_url
    }
    with open(CONFIG_PATH, "w") as f:
        config.write(f)

def get_token():
    if not os.path.exists(CONFIG_PATH):
        return None
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config["auth"].get("access_token")

def clear_token():
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)

def get_base_url():
    if not os.path.exists(CONFIG_PATH):
        # fallback default
        return "http://localhost:4004"
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config["auth"].get("base_url", "http://localhost:4004")
