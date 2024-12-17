import pytest
import os
from main import split_article_into_chunks, validate_config, validate_file_paths

def test_split_article_into_chunks_short_text():
    text = "To jest krótki tekst."
    chunks = split_article_into_chunks(text, max_length=50)
    assert len(chunks) == 1
    assert chunks[0] == text

def test_split_article_into_chunks_long_text():
    text = "A" * 10000  # Bardzo długi tekst
    chunks = split_article_into_chunks(text, max_length=6000)
    assert len(chunks) > 1
    # Sprawdzamy czy długość każdego fragmentu jest <= 6000
    for chunk in chunks:
        assert len(chunk) <= 6000

def test_validate_config_ok():
    config = {"model": "gpt-3.5-turbo", "temperature": 0.5, "max_tokens": 1000}
    validate_config(config)  # Nie powinno rzucić wyjątku

def test_validate_config_bad_model():
    with pytest.raises(ValueError):
        validate_config({"model": "", "temperature": 0.5, "max_tokens": 1000})

def test_validate_file_paths_ok(tmp_path):
    input_file = tmp_path / "input.txt"
    input_file.write_text("test content")
    output_file = str(tmp_path / "output.html")
    validate_file_paths(str(input_file), output_file)  # Nie powinno rzucić wyjątku

def test_validate_file_paths_not_exist():
    with pytest.raises(FileNotFoundError):
        validate_file_paths("nonexistent.txt", "output.html")
