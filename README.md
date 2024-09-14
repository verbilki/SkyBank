## Приложение 'Анализ банковских транзакций'

Этот проект представляет собой курсовую работу по Блоку 3 курса по Python на платформе SkyPro
ученика Олега Жадана (поток Prof 40.0).

## Инструкция по установке

SSH-ссылка для клонирования проекта с Github:

```
git@github.com:verbilki/SkyBank.git
```

Найти в корне проекта файл .env_template, скопировать его в .env и заполнить конфиденциальными данными
(например, для ключа API_KEY ввести токен подключения к API конвертации валют ).

1. Создать в PyCharm виртуальное окружение

### Для Windows

```commandline
python -m venv venv
```

### Для Linux, macOS

```bash
python3 -m venv venv
```

2. Активировать виртуальное окружение
   Следующую команду следует запускать из корня проекта:

### Для Windows

```commandline
venv\Scripts\activate
```

### Для Linux, macOS

```bash
source ./venv/bin/activate
```

3. Установить Poetry.

```bash
poetry install
```

4. Установить линтер flake8, анализатор статического кода mypy, форматтеры (black, isort)
на основании файла конфигурации pyproject.toml.

Пример настройки flake8, black, isort и mypy в файле pyproject.toml:

```
[tool.poetry.dependencies]
   python = "^3.8"
   flake8 = "^3.8.4"
   black = "^20.8b1"
   isort = "^5.6.4"
   mypy = "^0.790"
```

5. Установить в терминале дополнительные пакеты:

```bash
poetry add requests  
poetry add python-dotenv

pip install pandas
pip install pandas-stubs
pip install openpyxl
```

6. Запуск приложения
Для запуска приложения необходимо запустить на исполнение модуль src/main.py, состоящий из единственной функции main().

7. Функциональные модули

* [Папка src](#папка-src)
    + [Головной модуль main.py](#модуль-main-py)
    + [Модуль utils.py](#модуль-utils-py)
        - [Функция read_transactions_from_json](#read_transactions_from_json)
        - [Функция get_transaction_amount](#get_transaction_amount)
    + [Модуль masks.py](#модуль-masks-py)
    + [Модуль external_api.py](#модуль-external_api-py)
        - [Функция get_exchange_rate](#функция-get_exchange_rate)
    + [Модуль read_from_file.py](#модуль-read_from_file-py)
        - [Функция test_read_transactions_from_csv](#функция-test_read_transactions_from_csv)
        - [Функция test_read_transactions_from_excel](#функция-test_read_transactions_from_excel)
   + [Модуль widget.py](#модуль-widget-py)

* [папка tests](#tests)
    + [Модуль глобальных фикстур conftest.py](#conftestpy)
    + [Модуль tests/test_masks.py](#модуль-tests-test_masks-py)
    + [Модуль tests/test_read_from_file.py](#модуль-tests-read_from_file-py)
    + [Модуль tests/test_widget.py](#модуль-tests-test_widget-py)

## Папка src

### Модуль utils.py

#### Функция read_transactions_from_json

Назначение: Reads transactions from a JSON file specified by the `json_file_path` argument.

Args:
json_file_path (str)`: The path to the JSON file containing transactions.

Returns:
list[dict]`: A list of dictionaries representing transactions.
Each dictionary contains keys for the transaction's ID, state, date,
operation amount, description, from account, and to account.
Returns an empty list if the file cannot be opened or if the
deserialized data is not a list.

Raises: `json.JSONDecodeError`

#### функция get_transaction_amount

Назначение: получить объём заданной транзакции в рублях с учётом возможной конвертации валюты.
Args: transaction (dict[str, Any]): A dictionary representing a transaction.

Returns:
  float: The amount of the transaction. If the transaction is in USD, an exchange rate is
  requested from the external API.

### Модуль external_api.py

#### Функция get_exchange_rate

Назначение: получить текущий обменный курс иностранной валюты к рублю из внешнего API.
Args: None
Returns: `float`: The exchange rate.

### Модуль masks.py

- `get_mask_card_number(card_number: str) -> str`:
  This function takes a bank card number as input and returns a masked version of it.
  The masked card number will have the first 6 digits, followed by "******", and the last 4 digits visible.
  If the input card number is empty, an empty string is returned. The function also logs relevant information
  using the provided logger.

  If the card number contains non-digit characters, a `ValueError` is raised with a message indicating
  that the card number should only contain digits. If the card number has a length other than 16,
  a `ValueError` is raised with a message indicating that the card number should be 16 digits long.

  The function uses the `dotenv` library to load environment variables from a `.env` file.
  The `BANK_CARD_LAST_VISIBLE_DIGITS` environment variable is used to determine the number of visible digits
  at the end of the masked card number. If the variable is not set, the default value is 4.

- `get_mask_account(account_number: str) -> str`:
  This function takes a bank account number as input and returns a masked version of it.
  The masked account number will have the first 2 characters visible, followed by "**", 
  and the last 4 digits visible. If the input account number is empty, an empty string is returned.
  The function also logs relevant information using the provided logger.

  If the account number contains non-digit characters, a `ValueError` is raised with a message
  indicating that the account number should only contain digits. If the account number has a length
  other than 20, a `ValueError` is raised with a message indicating that the account number should be 20 digits long.

  The function uses the `dotenv` library to load environment variables from a `.env` file.
  The `BANK_CARD_LAST_VISIBLE_DIGITS` environment variable is used to determine the number of visible digits
  at the end of the masked account number. If the variable is not set, the default value is 4.

### read_transactions_from_csv(file_path: str) -> list[dict[str, Any]]

Reads transactions from a CSV file specified by the `file_path` argument.

#### Arguments

- `file_path` (str): The path to the CSV file containing transactions. The file should be semicolon-separated.

#### Returns

- list[dict[str, Any]]: A list of dictionaries representing transactions.
  Each dictionary contains keys for the transaction's ID, state, date, operation amount, description,
  from account, and to account. Returns an empty list if the file cannot be opened
  or if the deserialized data is not a list.

#### Note

Any keys with a value of 0 are removed from the final dictionary.


### read_transactions_from_excel(file_path: str) -> list[dict[str, Any]]

Reads transactions from an Excel file specified by the `file_path` argument.

#### Arguments

- `file_path` (str): The path to the Excel file containing transactions.
  The file should be in a format compatible with pandas' read_excel function.

#### Returns

- list[dict[str, Any]]: A list of dictionaries representing transactions.
  Each dictionary contains keys for the transaction's ID, state, date, operation amount, description, 
  from account, and to account. Returns an empty list if the file cannot be opened
  or if the deserialized data is not a list.

#### Note

Any keys with a value of 0 are removed from the final dictionary.

### Модуль widget.py
================

#### Функция mask_account_card
Description: The mask_account_card function takes a card or account number as input
             and returns a masked version of the number.

Parameters: card_or_acc_number (str): The card or account number to be masked.
Returns: str: The masked card or account number.

Example:
```
masked_number = mask_account_card("Visa Platinum 7000792289606361")
print(masked_number)  # Output: "Visa Platinum 7000 79** **** 6361"
```

#### Функция format_str_date
Description: The format_str_date function takes a date string as input and returns a formatted date string.

Parameters: date_string (str): The date string to be formatted.
Returns: str: The formatted date string.
Example:
```
formatted_date = format_str_date("2023-01-01T12:34:56.789012")
print(formatted_date)  # Output: "2023-01-01 12:34:56.789012"
```
Note: The format_str_date function is not fully implemented in the provided code snippet, 
so the example output is hypothetical.

Usage: To use the functions in the widget module, simply import the module and call the desired function:

```
from src.widget import mask_account_card, format_str_date

masked_number = mask_account_card("Visa Platinum 7000792289606361")
formatted_date = format_str_date("2023-01-01T12:34:56.789012")
```

### Модуль tests/test_utils.py 

Тесты для функций модуля src/utils.py.

### Модуль tests/test_external_api.py

Тесты для функций модуля src/external_api.py.

### Модуль tests/test_masks.py

- `test_get_mask_card_number_empty_input()`:
  This test function checks if the `get_mask_card_number` function returns an empty string when given an empty input.

- `test_get_mask_card_number_non_digit_characters()`:
  This test function checks if the `get_mask_card_number` function raises a `ValueError`
  when given a card number containing non-digit characters.

- `test_get_mask_card_number_incorrect_length()`:
  This test function checks if the `get_mask_card_number` function raises a `ValueError`
  when given a card number with an incorrect length.

- `test_get_mask_card_number_correct_input()`:
  This test function checks if the `get_mask_card_number` function returns the expected masked card number
  when given a valid card number.

- `test_get_mask_account_empty_input()`:
  This test function checks if the `get_mask_account` function returns an empty string when given an empty input.

- `test_get_mask_account_non_digit_characters()`:
  This test function checks if the `get_mask_account` function raises a `ValueError` 
  when given an account number containing non-digit characters.

- `test_get_mask_account_incorrect_length()`:
  This test function checks if the `get_mask_account` function raises a `ValueError` 
  when given an account number with an incorrect length.

- `test_get_mask_account_correct_input()`:
  This test function checks if the `get_mask_account` function returns the expected masked account number
  when given a valid account number.


### Модуль tests/test_read_from_file.py

This module contains unit tests for functions in the src/read_from_file module.

#### Функция test_read_transactions_from_csv

Description: This function tests the read_transactions_from_csv function by mocking the pd.read_csv function.
It asserts that the function returns the expected list of transactions when given an existing CSV file.

Parameters:
mock_read_csv (MagicMock): A mock object for pd.read_csv function.
get_df (pd.DataFrame): A pandas DataFrame containing the expected transactions.

Returns: None. The function asserts the behavior of read_transactions_from_csv function.

#### Функция test_read_transactions_from_excel

Description: This function tests the read_transactions_from_excel function by mocking the pd.read_excel function.
It asserts that the function returns the expected list of transactions when given an existing Excel file.

Parameters:
mock_read_excel (MagicMock): A mock object for pd.read_excel function.
get_df (pd.DataFrame): A pandas DataFrame containing the expected transactions.

Returns: None. The function asserts the behavior of read_transactions_from_excel function.


## 7. Настройка и использование фреймворка unit-тестирования Pytest

Исходный код модулей покрыт юнит-тестами Pytest на более, чем 88%. Для запуска выполните команды:

```bash
poetry add --group dev pytest # установка pytest в виртуальное окружение приложения
pytest # запуск тестов
```

Команда для формирования HTML-отчёта в терминале:

```bash
pytest --cov=src --cov-report=html
```

В результате зтого запуска будет сформирован HTML-отчет (файл htmlcov/index.html) о покрытии тестами.

## Лицензия

[GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.html#license-text)