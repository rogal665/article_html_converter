# Konwerter Artykułów do HTML z wykorzystaniem OpenAI API

[English version below](#article-to-html-converter-using-openai-api)

...

Konwerter Artykułów do HTML z wykorzystaniem OpenAI API
Jest to prosta aplikacja w Pythonie, która odczytuje tekst artykułu i konwertuje go na dobrze ustrukturyzowany kod HTML za pomocą OpenAI API. Wygenerowany HTML zawiera odpowiednie nagłówki, paragrafy oraz strategicznie rozmieszczone miejsca na obrazy, aby zwiększyć zrozumienie i atrakcyjność wizualną.

Funkcje
Integracja z OpenAI: Łączy się z OpenAI API w celu przetworzenia tekstu i wygenerowania kodu HTML.
Konfigurowalna konfiguracja: Pozwala na ustawienie modelu OpenAI, temperatury i maksymalnej liczby tokenów.
Umieszczanie obrazów: Automatycznie wstawia zastępniki obrazów w tekście na podstawie długości artykułu.
Interfejs wiersza poleceń: Oferuje różne argumenty wiersza poleceń do personalizacji.
Zarządzanie konfiguracją: Zapisuje ustawienia w pliku JSON i obsługuje resetowanie do wartości domyślnych.
Zarządzanie kluczem API: Bezpiecznie obsługuje klucz API za pomocą pliku .env.

Wymagania:
Python 3.7 lub wyższy
Biblioteka openai (np. openai==0.27.0)
Biblioteka python-dotenv (np. python-dotenv==0.21.0)

Instalacja:

Sklonuj repozytorium, wykonując następujące polecenia w terminalu:
Przejdź do katalogu, w którym chcesz sklonować repozytorium, a następnie wykonaj:

git clone https://github.com/rogal665/article_html_converter.git
cd article_html_converter

Zainstaluj wymagane zależności, uruchamiając:
pip install -r requirements.txt

Zależności:

Plik requirements.txt zawiera konkretne wersje wymaganych pakietów, aby zapewnić kompatybilność:
openai==0.27.0
python-dotenv==0.21.0

Konfiguracja:

Ustaw swój klucz OpenAI API:
Aplikacja poprosi o wprowadzenie klucza OpenAI API przy pierwszym uruchomieniu.

Alternatywnie, utwórz plik .env w katalogu projektu i dodaj swój klucz API w następujący sposób:
OPENAI_API_KEY=twoj-klucz-api
Ważne: Zachowaj bezpieczeństwo swojego klucza OpenAI API i nie udostępniaj go publicznie.

Użycie:
Aby przetworzyć artykuł, uruchom skrypt main.py:
python main.py

Domyślnie skrypt odczytuje artykuł z pliku artykul.txt i zapisuje wyjściowy HTML do artykul.html.

Argumenty wiersza poleceń
--set_model MODEL_NAME: Ustaw model OpenAI (np. gpt-3.5-turbo) i zapisz go.
--set_temperature TEMPERATURE: Ustaw parametr temperatury i zapisz go.
--set_max_tokens MAX_TOKENS: Ustaw parametr max_tokens i zapisz go.
--reset_config: Zresetuj konfigurację do wartości domyślnych.
--reset_api_key: Usuń zapisany klucz API.
--input_file INPUT_FILE: Określ inny plik wejściowy.
--output_file OUTPUT_FILE: Określ inny plik wyjściowy.
Przykłady
Aby ustawić model OpenAI na GPT-4, uruchom:

bash
Skopiuj kod
python main.py --set_model gpt-4
Aby przetworzyć konkretny artykuł i plik wyjściowy, uruchom:

bash
Skopiuj kod
python main.py --input_file moj_artykul.txt --output_file moje_wyjscie.html
Aby zresetować konfigurację do wartości domyślnych, uruchom:

bash
Skopiuj kod
python main.py --reset_config
Konfiguracja
Ustawienia konfiguracyjne są zapisywane w pliku config.json. Możesz edytować ten plik ręcznie lub użyć argumentów wiersza poleceń, aby zaktualizować ustawienia.

Domyślna konfiguracja to:

Model: gpt-3.5-turbo
Temperatura: 0.7
Max Tokens: 2048
Logowanie
Logi są zapisywane w pliku app.log i wyświetlane w konsoli. Logowanie obejmuje komunikaty informacyjne (np. podczas odczytu plików, wysyłania żądań) oraz komunikaty o błędach (np. błędy API, brak pliku).

Obsługa błędów
OpenAIError: Przechwytuje i loguje błędy związane z OpenAI API.
Nieznane wyjątki: Przechwytuje i loguje wszelkie inne nieoczekiwane błędy.
Testy i Walidacja
Aplikacja została przetestowana z różnymi artykułami, aby upewnić się, że wygenerowany kod HTML zawsze spełnia określone wytyczne. Kod jest ustrukturyzowany i zachowuje integralność oryginalnej treści artykułu.

Uwagi
Upewnij się, że masz stabilne połączenie internetowe podczas uruchamiania skryptu.
Skrypt nie zawiera żadnego kodu CSS ani JavaScript; generuje tylko zawartość sekcji <body> w HTML.
Jak odesłać zadanie?
Proszę dołączyć cały kod aplikacji, przykładowy artykuł oraz wygenerowany plik artykul.html do repozytorium. Upewnij się, że Twoje repozytorium jest dostępne i udostępnij link zgodnie z instrukcjami rekrutera.

Licencja
Ten projekt jest licencjonowany na warunkach licencji MIT. Zobacz plik LICENSE po więcej szczegółów.

---

# Article to HTML Converter Using OpenAI API

...

Article to HTML Converter Using OpenAI API
This is a simple Python application that reads a text article and converts it into well-structured HTML code using the OpenAI API. The generated HTML includes appropriate headings, paragraphs, and strategically placed image placeholders to enhance understanding and visual appeal.

Features
OpenAI Integration: Connects to the OpenAI API to process text and generate HTML.
Customizable Configuration: Allows setting the OpenAI model, temperature, and max tokens.
Image Placement: Automatically inserts image placeholders within the text based on the article length.
Command-Line Interface: Offers various command-line arguments for customization.
Configuration Management: Saves settings to a JSON file and supports resetting to default values.
API Key Management: Handles the API key securely using a .env file.
Requirements
Python 3.7 or higher
openai library (e.g., openai==0.27.0)
python-dotenv library (e.g., python-dotenv==0.21.0)
Installation
Clone the repository by running the following commands in your terminal:

Navigate to the directory where you want to clone the repository, then execute:

bash
Skopiuj kod
git clone https://github.com/yourusername/article-html-converter.git
cd article-html-converter
Note: Replace https://github.com/yourusername/article-html-converter.git with the actual URL of your repository.

Install the required dependencies by running:

bash
Skopiuj kod
pip install -r requirements.txt
Dependencies:

The requirements.txt file contains specific versions of the required packages to ensure compatibility:

makefile
Skopiuj kod
openai==0.27.0
python-dotenv==0.21.0
Configuration
Set up your OpenAI API key:

The application will prompt you to enter your OpenAI API key on the first run.

Alternatively, create a .env file in the project directory and add your API key as follows:

makefile
Skopiuj kod
OPENAI_API_KEY=your-api-key
Important: Keep your OpenAI API key secure and do not share it publicly.

Usage
To process an article, run the main.py script:

bash
Skopiuj kod
python main.py
By default, the script reads the article from artykul.txt and writes the output HTML to artykul.html.

Command-Line Arguments
--set_model MODEL_NAME: Set the OpenAI model (e.g., gpt-3.5-turbo) and save it.
--set_temperature TEMPERATURE: Set the temperature parameter and save it.
--set_max_tokens MAX_TOKENS: Set the max_tokens parameter and save it.
--reset_config: Reset configuration to default values.
--reset_api_key: Remove the saved API key.
--input_file INPUT_FILE: Specify a different input file.
--output_file OUTPUT_FILE: Specify a different output file.
Examples
To set the OpenAI model to GPT-4, run:

bash
Skopiuj kod
python main.py --set_model gpt-4
To process a specific article and output file, run:

bash
Skopiuj kod
python main.py --input_file my_article.txt --output_file my_output.html
To reset the configuration to default values, run:

bash
Skopiuj kod
python main.py --reset_config
Configuration Details
Configuration settings are saved in the config.json file. You can edit this file manually or use command-line arguments to update settings.

The default configuration is:

Model: gpt-3.5-turbo
Temperature: 0.7
Max Tokens: 2048
Logging
Logs are saved in the app.log file and displayed in the console. Logging includes informational messages (e.g., when reading files, sending requests) and error messages (e.g., API errors, file not found).

Error Handling
OpenAIError: Catches and logs errors related to the OpenAI API.
Unknown Exceptions: Catches and logs any other unexpected errors.
Testing and Validation
The application has been tested with various articles to ensure that the generated HTML code always meets the specified guidelines. The code is structured and maintains the integrity of the original article content.

Notes
Ensure you have a stable internet connection when running the script.
The script does not include any CSS or JavaScript code; it generates only the content for the <body> section in HTML.
How to Submit the Assignment
Please include all the application code, the sample article, and the generated artykul.html file in the repository. Make sure your repository is accessible and share the link according to the recruiter's instructions.

License
This project is licensed under the terms of the MIT License. See the LICENSE file for details.