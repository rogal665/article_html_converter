import os
import argparse
import logging
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from config_manager import load_config, save_config, reset_config, reset_api_key
from tenacity import retry, wait_fixed, stop_after_attempt

logging.getLogger("httpx").setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

load_dotenv()


def get_api_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logging.info("Klucz API nie jest ustawiony, proszę o podanie klucza.")
        logging.getLogger().handlers[0].flush()  # Wymuś zapis logu przed wywołaniem input()
        api_key = input('Podaj swój klucz API OpenAI: ').strip()
        with open('.env', 'a', encoding='utf-8') as env_file:
            env_file.write(f'OPENAI_API_KEY={api_key}\n')
        os.environ['OPENAI_API_KEY'] = api_key
        logging.info("Nowy klucz API zapisany w pliku .env.")
    return api_key


def split_article_into_chunks(article_content, max_length=6000):
    article_content = article_content.strip()
    if len(article_content) <= max_length:
        return [article_content]

    chunks = []
    start = 0
    while start < len(article_content):
        end = start + max_length
        if end > len(article_content):
            end = len(article_content)

        possible_break_points = [article_content.rfind('\n', start, end),
                                 article_content.rfind('. ', start, end)]

        breakpoint_pos = max(possible_break_points)

        if breakpoint_pos == -1:
            breakpoint_pos = end

        chunk = article_content[start:breakpoint_pos].strip()
        if chunk:
            chunks.append(chunk)
        start = breakpoint_pos
        if article_content[start:start + 1] in ['.', '\n']:
            start += 1
    return chunks


def validate_config(config):
    # Sprawdzenie czy model, temperature, max_tokens mają poprawne wartości
    if 'model' not in config or not isinstance(config['model'], str) or not config['model']:
        raise ValueError("Nieprawidłowa konfiguracja: pole 'model' musi być niepustym stringiem.")
    if 'temperature' not in config or not (0 <= config['temperature'] <= 2):
        raise ValueError("Nieprawidłowa konfiguracja: pole 'temperature' musi być liczbą z zakresu 0-2.")
    if 'max_tokens' not in config or not (1 <= config['max_tokens'] <= 4096):
        raise ValueError("Nieprawidłowa konfiguracja: pole 'max_tokens' musi być liczbą w zakresie 1-4096.")


def validate_file_paths(input_file, output_file):
    # Walidacja ścieżek do plików
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Plik wejściowy {input_file} nie istnieje.")
    if not output_file or not isinstance(output_file, str):
        raise ValueError("Ścieżka do pliku wyjściowego jest nieprawidłowa.")


def generate_prompt(chunk):
    return (
        "You are a web development expert specializing in converting articles into well-structured HTML code. "
        "Your goal is to transform the provided article into HTML content that is properly structured with appropriate HTML tags, including strategically placed images to enhance understanding and visual appeal. "
        "Remember that if the quality of your work is insufficient, someone may get hurt, but if your work is of a high standard, you will certainly get a tip.\n\n"
        "Instructions:\n"
        "1. **Do not change or modify the text**: Use the article text exactly as provided without altering, paraphrasing, or adding new content.\n\n"
        "2. **Structure the content with HTML tags**:\n"
        "   - Use `<h1>` for the main title.\n"
        "   - Use `<h2>`, `<h3>`, etc., for headings and subheadings.\n"
        "   - Use `<p>` for paragraphs.\n"
        "   - Use `<ul>`/`<ol>` and `<li>` for lists.\n"
        "   - Use other semantic tags like `<blockquote>`, `<strong>`, `<em>` where appropriate.\n\n"
        "3. **Place images appropriately within the text**:"
        "   - Determine an appropriate number of images based on the length of the article (e.g., one image per 3-4 paragraphs)."
        "   - **Do not place all images at the end of the article.**"
        "   - Insert images immediately after paragraphs where they enhance understanding or visual interest."
        "   - Each image should be enclosed in a `<figure>` tag."
        "   - Within `<figure>`, include:"
        "     - An `<img>` tag with `src=\"image_placeholder.jpg\"`."
        "     - An `alt` attribute with a precise, 15-word description in the same language as the article."
        "     - A `<figcaption>` with a brief caption, also in the same language."
        "4. **Exclude CSS and JavaScript**: Do not include any CSS styles or JavaScript code.\n\n"
        "5. **Output only the HTML body content**:\n"
        "   - Do not include `<html>`, `<head>`, or `<body>` tags.\n"
        "   - Provide clean HTML code without wrapping it in code blocks or adding any extra text, explanations, or comments.\n\n"
        "6. **Ensure compliance with all instructions**: Follow all instructions carefully to produce the desired output.\n\n"
        f"Article:\n{chunk}"
    )


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def request_openai_completion(client, config, prompt):
    return client.chat.completions.create(
        model=config['model'],
        messages=[{"role": "user", "content": prompt}],
        max_tokens=config['max_tokens'],
        temperature=config['temperature'],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Przetwarzanie artykułu za pomocą OpenAI API.')
    parser.add_argument('--set_model', type=str, help='Ustaw model OpenAI i zapisz go w konfiguracji.')
    parser.add_argument('--set_temperature', type=float, help='Ustaw parametr temperature i zapisz go w konfiguracji.')
    parser.add_argument('--set_max_tokens', type=int, help='Ustaw parametr max_tokens i zapisz go w konfiguracji.')
    parser.add_argument('--reset_config', action='store_true', help='Resetuj konfigurację do wartości domyślnych.')
    parser.add_argument('--reset_api_key', action='store_true',
                        help='Usuń zapisany klucz API i poproś o nowy przy następnym uruchomieniu.')
    parser.add_argument('--input_file', type=str, default='artykul.txt', help='Ścieżka do pliku z artykułem.')
    parser.add_argument('--output_file', type=str, default='artykul.html', help='Ścieżka do pliku wyjściowego.')
    args = parser.parse_args()

    config = load_config()

    if args.set_model:
        config['model'] = args.set_model
        save_config(config)
        logging.info('Model został zaktualizowany i zapisany w konfiguracji.')

    if args.set_temperature is not None:
        config['temperature'] = args.set_temperature
        save_config(config)
        logging.info('Parametr temperature został zaktualizowany i zapisany w konfiguracji.')

    if args.set_max_tokens is not None:
        config['max_tokens'] = args.set_max_tokens
        save_config(config)
        logging.info('Parametr max_tokens został zaktualizowany i zapisany w konfiguracji.')

    if args.reset_config:
        reset_config()
        config = load_config()
        logging.info('Konfiguracja została zresetowana do wartości domyślnych.')

    if args.reset_api_key:
        reset_api_key()
        logging.info('Klucz API został usunięty. Program poprosi o jego wprowadzenie przy następnym uruchomieniu.')

    # Jeśli nie wykonano czynności konfiguracyjnych, przetwarzamy artykuł
    if not any([
        args.set_model,
        args.set_temperature is not None,
        args.set_max_tokens is not None,
        args.reset_config,
        args.reset_api_key
    ]):
        try:
            validate_file_paths(args.input_file, args.output_file)
            validate_config(config)
        except (FileNotFoundError, ValueError) as e:
            logging.error(f"Błąd walidacji: {e}")
            exit(1)

        logging.info(f"Odczyt artykułu z pliku: {args.input_file}")
        with open(args.input_file, 'r', encoding='utf-8') as file:
            article_content = file.read()
        logging.info("Artykuł został pomyślnie odczytany.")

        # Dzielenie artykułu na mniejsze części, jeśli jest zbyt długi
        chunks = split_article_into_chunks(article_content, max_length=6000)
        logging.info(f"Artykuł został podzielony na {len(chunks)} fragment(ów).")

        api_key = get_api_key()
        client = OpenAI(api_key=api_key)

        all_html_parts = []
        for i, chunk in enumerate(chunks, start=1):
            logging.info(f"Przetwarzanie fragmentu {i}/{len(chunks)}...")
            prompt = generate_prompt(chunk)
            try:
                response = request_openai_completion(client, config, prompt)
                html_content = response.choices[0].message.content.strip()
                all_html_parts.append(html_content)
            except OpenAIError as e:
                logging.error(f'Błąd API OpenAI podczas przetwarzania fragmentu {i}: {e}')
            except Exception as e:
                logging.error(f'Nieznany błąd podczas przetwarzania fragmentu {i}: {e}')

        final_html = "\n".join(all_html_parts)

        try:
            with open(args.output_file, 'w', encoding='utf-8') as file:
                file.write(final_html)
            logging.info(f"Artykuł został pomyślnie przetworzony i zapisany w pliku '{args.output_file}'.")
        except Exception as e:
            logging.error(f"Wystąpił błąd przy zapisywaniu do pliku {args.output_file}: {e}")