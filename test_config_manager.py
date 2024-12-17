import os
import json
import pytest
from config_manager import load_config, save_config, reset_config, DEFAULT_CONFIG, CONFIG_FILE

def test_load_config_no_file():
    if os.path.isfile(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    config = load_config()
    assert config == DEFAULT_CONFIG

def test_save_config():
    test_config = {"model": "gpt-3.5-turbo", "temperature": 1.0, "max_tokens": 512}
    save_config(test_config)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert data == test_config

def test_reset_config():
    reset_config()
    config = load_config()
    assert config == DEFAULT_CONFIG
