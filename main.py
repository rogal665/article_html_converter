import os
import argparse
import logging
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from config_manager import load_config, save_config, reset_config, reset_api_key

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
        with open('.env', 'a') as env_file:
            env_file.write(f'OPENAI_API_KEY={api_key}\n')
        os.environ['OPENAI_API_KEY'] = api_key
        logging.info("Nowy klucz API zapisany w pliku .env.")
    return api_key


parser = argparse.ArgumentParser(description='Przetwarzanie artykułu za pomocą OpenAI API.')
parser.add_argument('--set_model', type=str, help='Ustaw model OpenAI i zapisz go w konfiguracji.')
parser.add_argument('--set_temperature', type=float, help='Ustaw parametr temperature i zapisz go w konfiguracji.')
parser.add_argument('--set_max_tokens', type=int, help='Ustaw parametr max_tokens i zapisz go w konfiguracji.')
parser.add_argument('--reset_config', action='store_true', help='Resetuj konfigurację do wartości domyślnych.')
parser.add_argument('--reset_api_key', action='store_true',
                    help='Usuń zapisany klucz API i poproś o nowy przy kolejnym uruchomieniu.')
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

if not any([args.set_model, args.set_temperature is not None, args.set_max_tokens is not None, args.reset_config,
            args.reset_api_key]):
    if not os.path.isfile(args.input_file):
        logging.error(f'Plik {args.input_file} nie istnieje.')
        exit(1)

    logging.info(f"Odczyt artykułu z pliku: {args.input_file}")
    with open(args.input_file, 'r', encoding='utf-8') as file:
        article_content = file.read()
    logging.info("Artykuł został pomyślnie odczytany.")

    prompt = (
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
        "3. **Place images appropriately within the text**:\n"
        "   - Determine an appropriate number of images based on the length of the article (e.g., one image per 3-4 paragraphs).\n"
        "   - **Do not place all images at the end of the article.**\n"
        "   - Insert images immediately after paragraphs where they enhance understanding or visual interest.\n"
        "   - Each image should be enclosed in a `<figure>` tag.\n"
        "   - Within `<figure>`, include:\n"
        "     - An `<img>` tag with `src=\"image_placeholder.jpg\"`.\n"
        "     - An `alt` attribute with a precise, 15-word description in the same language as the article.\n"
        "     - A `<figcaption>` with a brief caption, also in the same language.\n\n"
        "4. **Exclude CSS and JavaScript**: Do not include any CSS styles or JavaScript code.\n\n"
        "5. **Output only the HTML body content**:\n"
        "   - Do not include `<html>`, `<head>`, or `<body>` tags.\n"
        "   - Provide clean HTML code without wrapping it in code blocks or adding any extra text, explanations, or comments.\n\n"
        "6. **Ensure compliance with all instructions**: Follow all instructions carefully to produce the desired output.\n\n"
        "Article:\n"
        f"{article_content}"
    )

    api_key = get_api_key()
    client = OpenAI(api_key=api_key)

    try:
        logging.info("Wysyłanie żądania do OpenAI, proszę czekać na odpowiedź...")
        response = client.chat.completions.create(
            model=config['model'],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=config['max_tokens'],
            temperature=config['temperature'],
        )
        logging.info("Odpowiedź z serwera OpenAI została odebrana.")

        html_content = response.choices[0].message.content.strip()

        with open(args.output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
        logging.info(f"Artykuł został pomyślnie przetworzony i zapisany w pliku '{args.output_file}'.")

    except OpenAIError as e:
        logging.error(f'Błąd API OpenAI: {e}')
        print(f'Wystąpił błąd podczas komunikacji z OpenAI: {e}')
    except Exception as e:
        logging.error(f'Nieznany błąd: {e}')
        print(f'Wystąpił nieznany błąd: {e}')
