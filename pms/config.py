# pms/config.py

import os
import configparser

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".pms")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config")

def get_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
    return config

def save_token(token, base_url):
    config = get_config()
    if not config.has_section("auth"):
        config.add_section("auth")
    config.set("auth", "access_token", token)
    config.set("auth", "base_url", base_url)
    with open(CONFIG_PATH, "w") as f:
        config.write(f)

def get_token():
    config = get_config()
    if config.has_section("auth") and config.has_option("auth", "access_token"):
        return config.get("auth", "access_token")
    return None

def clear_token():
    config = get_config()
    if config.has_section("auth"):
        config.remove_option("auth", "access_token")
    with open(CONFIG_PATH, "w") as f:
        config.write(f)

def get_base_url():
    config = get_config()
    if config.has_section("auth") and config.has_option("auth", "base_url"):
        return config.get("auth", "base_url")
    return "http://localhost:4004"
