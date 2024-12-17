import os
import json

CONFIG_FILE = 'config.json'
ENV_FILE = '.env'

DEFAULT_CONFIG = {
    "model": "gpt-4o",
    "temperature": 0.7,
    "max_tokens": 2048
}


def load_config():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return DEFAULT_CONFIG.copy()


def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)


def reset_config():
    save_config(DEFAULT_CONFIG)


def reset_api_key():
    if os.path.isfile(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            lines = f.readlines()
        with open(ENV_FILE, 'w') as f:
            for line in lines:
                if not line.startswith('OPENAI_API_KEY'):
                    f.write(line)
        print("Klucz API został usunięty z pliku .env.")
