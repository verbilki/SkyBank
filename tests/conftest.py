import json
from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def get_df() -> pd.DataFrame:
    """
    A fixture that returns a pandas DataFrame with columns matching the structure of the DataFrame returned by the
    `read_excel2dataframe` function.

    The DataFrame contains three transactions with the following columns:
        'Дата операции', 'Дата платежа', 'Номер карты', 'Статус', 'Сумма операции',
        'Валюта операции', 'Сумма платежа', 'Валюта платежа', 'Кэшбэк', 'Категория', 'MCC',
        'Описание', 'Бонусы (включая кэшбэк)', 'Округление на инвесткопилку', 'Сумма операции с округлением'.
    """
    data = {
        "Дата операции": ["01.12.2021 12:35:05", "30.11.2021 18:19:28", "31.01.2018 20:09:33"],
        "Дата платежа": ["01.12.2021", "30.11.2021", "31.01.2018"],
        "Номер карты": ["*7197", "*4556", "*4556"],
        "Статус": ["OK", "FAILED", "OK"],
        "Сумма операции": [-99.00, -55.00, -1212.80],
        "Валюта операции": ["RUB", "RUB", "RUB"],
        "Сумма платежа": [-99.00, -55.00, -1212.80],
        "Валюта платежа": ["RUB", "RUB", "RUB"],
        "Кэшбэк": [np.nan, np.nan, 12],
        "Категория": ["Фастфуд", np.nan, "Ж/д билеты"],
        "MCC": ["5814", np.nan, "4112"],
        "Описание": ["IP Yakubovskaya M.V.", "Перевод на карту", "РЖД"],
        "Бонусы (включая кэшбэк)": [1.00, 0.00, 12.00],
        "Округление на инвесткопилку": [0.00, 0.00, 0.00],
        "Сумма операции с округлением": [99.00, 55.00, 1212.80],
    }
    return pd.DataFrame(data)


@pytest.fixture
def dec_df() -> pd.DataFrame:
    """
    Fixture for a DataFrame containing the transactions data for December.

    The DataFrame contains the following columns: "Дата операции", "Дата платежа", "Номер карты", "Статус",
    "Сумма операции", "Валюта операции", "Сумма платежа", "Валюта платежа", "Кэшбэк", "Категория", "MCC",
    "Описание", "Бонусы (включая кэшбэк)", "Округление на инвесткопилку", "Сумма операции с округлением".

    This fixture is used to test the `spending_by_category` function.
    """
    data = {
        "Дата операции": ["01.12.2021 12:35:05"],
        "Дата платежа": ["01.12.2021"],
        "Номер карты": ["*7197"],
        "Статус": ["OK"],
        "Сумма операции": [-99.00],
        "Валюта операции": ["RUB"],
        "Сумма платежа": [-99.00],
        "Валюта платежа": ["RUB"],
        "Кэшбэк": [np.nan],
        "Категория": ["Фастфуд"],
        "MCC": ["5814"],
        "Описание": ["IP Yakubovskaya M.V."],
        "Бонусы (включая кэшбэк)": [1.00],
        "Округление на инвесткопилку": [0.00],
        "Сумма операции с округлением": [99.00],
    }
    return pd.DataFrame(data)


@pytest.fixture
def get_empty_df() -> pd.DataFrame:
    """
    This function returns an empty DataFrame with columns matching the structure of the DataFrame returned by the
    `read_excel2dataframe` function.

    Returns:
    pd.DataFrame: An empty DataFrame with columns:
        'Дата операции', 'Дата платежа', 'Номер карты', 'Статус', 'Сумма операции',
        'Валюта операции', 'Сумма платежа', 'Валюта платежа', 'Кэшбэк', 'Категория', 'MCC', 'Описание',
        'Бонусы (включая кэшбэк)', 'Округление на инвесткопилку', 'Сумма операции с округлением'.
    """
    data = {
        "Дата операции": [np.nan],
        "Дата платежа": [np.nan],
        "Номер карты": [np.nan],
        "Статус": [np.nan],
        "Сумма операции": [np.nan],
        "Валюта операции": [np.nan],
        "Сумма платежа": [np.nan],
        "Валюта платежа": [np.nan],
        "Кэшбэк": [np.nan],
        "Категория": [np.nan],
        "MCC": [np.nan],
        "Описание": [np.nan],
        "Бонусы (включая кэшбэк)": [np.nan],
        "Округление на инвесткопилку": [np.nan],
        "Сумма операции с округлением": [np.nan],
    }
    return pd.DataFrame(data)


@pytest.fixture
def monthly_operations() -> dict[str, float]:
    """
    Fixture providing a dictionary of monthly operations.

    The dictionary contains the account numbers as keys and the corresponding
    monthly operation amounts as values.

    Returns: dict[str, float]: A dictionary of account numbers and monthly operation amounts.
    """
    return {
        "1112": 46207.08,
        "4556": 533948.75,
        "5091": 14918.16,
        "5441": 470854.8,
        "5507": 84000.0,
        "6002": 69200.0,
        "7197": 2417014.58,
        "nan": 552941.14,
    }


@pytest.fixture
def cashback() -> dict[str, list]:
    """
    Fixture providing a dictionary of account numbers and their corresponding cashback values.

    The dictionary contains the account numbers as keys and the corresponding
    cashback values as values. The cashback values are lists containing the
    total spent amount and the cashback amount.

    Returns: dict[str, list]: A dictionary of account numbers and cashback values.
    """
    return {
        "1112": [46207.08, 462.07],
        "4556": [533948.75, 5339.49],
        "5091": [14918.16, 149.18],
        "5441": [470854.8, 4708.55],
        "5507": [84000.0, 840.0],
        "6002": [69200.0, 692.0],
        "7197": [2417014.58, 24170.15],
        "nan": [552941.14, 5529.41],
    }


@pytest.fixture
def transactions_list() -> list[dict]:
    """
    This function returns a list of dictionaries, each representing a transaction.
    Each dictionary contains the transaction's date and amount.

    Parameters: None

    Returns:
    list[dict]: A list of dictionaries. Each dictionary has the following keys:
        - 'Дата операции': A string representing the transaction's date in 'YYYY-MM-DD' format.
        - 'Сумма операции': A float representing the transaction's amount.
    """
    return [
        {"Дата операции": "2021-12-31", "Сумма операции": -160.89},
        {"Дата операции": "2021-12-01", "Сумма операции": -64.0},
        {"Дата операции": "2021-11-03", "Сумма операции": -191.5},
        {"Дата операции": "2021-11-02", "Сумма операции": -60.0},
        {"Дата операции": "2021-11-30", "Сумма операции": -103.0},
        {"Дата операции": "2021-11-30", "Сумма операции": -41.0},
        {"Дата операции": "2021-11-29", "Сумма операции": 500.0},
    ]


@pytest.fixture
def json_response() -> str:
    """
    This function returns a JSON string representing a response from a financial service.
    The JSON string contains information about greeting, cards, top transactions, currency rates,
    and stock prices.

    Returns:
    str: A JSON string representing the response.
    """
    data = {
        "greeting": "Добрый день!",
        "cards": [
            {
                "last_digits": "1112",
                "total_spent": 46207.08,
                "cashback": 462.07,
            },
            {
                "last_digits": "4556",
                "total_spent": 533948.75,
                "cashback": 5339.49,
            },
            {
                "last_digits": "5091",
                "total_spent": 14918.16,
                "cashback": 149.18,
            },
        ],
        "top_transactions": [
            {
                "date": "31.01.2018",
                "amount": -1212.80,
                "category": "Ж/д билеты",
                "description": "РЖД",
            },
            {
                "date": "01.12.2021",
                "amount": -99.00,
                "category": "Фастфуд",
                "description": "IP Yakubovskaya M.V.",
            },
        ],
        "currency_rates": [{"currency": "USD", "rate": 87.99}, {"currency": "EUR", "rate": 95.18}],
        "stock_prices": [
            {"stock": "AAPL", "price": 216.24},
            {"stock": "AMZN", "price": 166.94},
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=4)


@pytest.fixture
def currencies() -> list[dict[str, str | int]]:
    """
    This function returns a list of dictionaries, each representing a currency with its details.

    Returns:
    list[dict[str, str | int]]: A list of dictionaries. Each dictionary contains the following keys:
        - 'symbol': A string representing the currency symbol.
        - 'name': A string representing the full name of the currency.
        - 'symbol_native': A string representing the native symbol of the currency.
        - 'decimal_digits': An integer representing the number of decimal digits in the currency.
        - 'rounding': An integer representing the rounding method of the currency.
        - 'code': A string representing the currency code.
        - 'name_plural': A string representing the plural form of the currency name.
    """
    return [
        {
            "symbol": "$",
            "name": "US Dollar",
            "symbol_native": "$",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "USD",
            "name_plural": "US dollars",
        },
        {
            "symbol": "€",
            "name": "Euro",
            "symbol_native": "€",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "EUR",
            "name_plural": "euros",
        },
        {
            "symbol": "CN¥",
            "name": "Chinese Yuan",
            "symbol_native": "CN¥",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "CNY",
            "name_plural": "Chinese yuan",
        },
        {
            "symbol": "¥",
            "name": "Japanese Yen",
            "symbol_native": "￥",
            "decimal_digits": 0,
            "rounding": 0,
            "code": "JPY",
            "name_plural": "Japanese yen",
        },
        {
            "symbol": "KZT",
            "name": "Kazakhstani Tenge",
            "symbol_native": "тңг.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "KZT",
            "name_plural": "Kazakhstani tenges",
        },
    ]


@pytest.fixture
def stocks() -> list[dict[str, str]]:
    """
    This function returns a list of dictionaries, each representing a stock with its company name and ticker symbol.

    Parameters: None

    Returns:
    list[dict[str, str]]: A list of dictionaries. Each dictionary contains the following keys:
        - 'company': A string representing the company name.
        - 'tickerSymbol': A string representing the stock's ticker symbol.
    """
    return [
        {"company": "Apple Inc", "tickerSymbol": "AAPL"},
        {"company": "Amazon.com Inc", "tickerSymbol": "AMZN"},
        {"company": "Alphabet Inc Cl A", "tickerSymbol": "GOOGL"},
        {"company": "Microsoft Corp", "tickerSymbol": "MSFT"},
        {"company": "Tesla Inc", "tickerSymbol": "TSLA"},
    ]


@pytest.fixture
def api_response_currencies() -> dict:
    return {
        "Date": "2024-08-10T11:30:00+03:00",
        "PreviousDate": "2024-08-09T11:30:00+03:00",
        "Timestamp": "2024-08-10T12:00:00+03:00",
        "Valute": {
            "USD": {
                "ID": "R01235",
                "NumCode": "840",
                "CharCode": "USD",
                "Nominal": 1,
                "Name": "Доллар США",
                "Value": 87.992,
                "Previous": 86.5621,
            },
            "EUR": {
                "ID": "R01239",
                "NumCode": "978",
                "CharCode": "EUR",
                "Nominal": 1,
                "Name": "Евро",
                "Value": 95.1844,
                "Previous": 94.1333,
            },
            "CNY": {
                "ID": "R01375",
                "NumCode": "156",
                "CharCode": "CNY",
                "Nominal": 1,
                "Name": "Китайский юань",
                "Value": 11.8911,
                "Previous": 11.8664,
            },
            "KZT": {
                "ID": "R01335",
                "NumCode": "398",
                "CharCode": "KZT",
                "Nominal": 100,
                "Name": "Казахстанских тенге",
                "Value": 18.4415,
                "Previous": 18.1998,
            },
            "JPY": {
                "ID": "R01820",
                "NumCode": "392",
                "CharCode": "JPY",
                "Nominal": 100,
                "Name": "Японских иен",
                "Value": 59.6394,
                "Previous": 59.2688,
            },
        },
    }


@pytest.fixture
def api_response_stocks() -> list[dict]:
    """
    This function returns a list of dictionaries, each representing a stock with its details.

    Returns:
    list[dict]: A list of dictionaries. Each dictionary contains the following keys:
        - 'symbol': A string representing the stock's ticker symbol.
        - 'name': A string representing the company name.
        - 'price': A float representing the current stock price.
        - 'exchange': A string representing the stock's exchange.
        - 'exchangeShortName': A string representing the short name of the stock's exchange.
        - 'type': A string representing the type of the stock (always 'stock' in this case).

    Example:
    [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 216.24,
            "exchange": "NASDAQ Global Select",
            "exchangeShortName": "NASDAQ",
            "type": "stock",
        },
        {
            "symbol": "AMZN",
            "name": "Amazon.com, Inc.",
            "price": 166.94,
            "exchange": "NASDAQ Global Select",
            "exchangeShortName": "NASDAQ",
            "type": "stock",
        },
        ...
    ]
    """
    return [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 216.24,
            "exchange": "NASDAQ Global Select",
            "exchangeShortName": "NASDAQ",
            "type": "stock",
        },
        {
            "symbol": "AMZN",
            "name": "Amazon.com, Inc.",
            "price": 166.94,
            "exchange": "NASDAQ Global Select",
            "exchangeShortName": "NASDAQ",
            "type": "stock",
        },
        {
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "price": 163.67,
            "exchange": "NASDAQ Global Select",
            "exchangeShortName": "NASDAQ",
            "type": "stock",
        },
        {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "price": 406.02,
            "exchange": "NASDAQ Global Select",
            "exchangeShortName": "NASDAQ",
            "type": "stock",
        },
        {
            "symbol": "TSLA",
            "name": "Tesla, Inc.",
            "price": 200,
            "exchange": "NASDAQ Global Select",
            "exchangeShortName": "NASDAQ",
            "type": "stock",
        },
    ]


@pytest.fixture
def mock_logger(mocker):
    """
    Create a mock for the logger.

    This function is used to replace the actual logger with a mock object during testing.
    This allows us to verify that the logger is being used correctly without actually
    performing any logging operations.

    Returns: MagicMock: A mock object that represents the logger.
    """
    logger = mocker.patch("src.utils.logger", new=MagicMock())
    return logger
