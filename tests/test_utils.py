import tempfile
from datetime import datetime
from typing import Any
from unittest import mock
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import requests

from src.utils import (calculate_cashback, get_currencies, get_data_from_user, get_data_via_api_currencies,
                       get_data_via_api_stocks, get_exchange_rates, get_stock_prices, get_stocks, get_top_transactions,
                       process_cards_info, read_excel2dataframe, say_hello, sort_by_amount)


def test_calculate_cashback(monthly_operations: dict[str, float], cashback: int) -> None:
    """
    Test the calculate_cashback function.

    This function tests the calculate_cashback function by comparing the result of the function
    with the expected cashback value.

    Parameters:
    - monthly_operations (dict[str, float]): A dictionary representing the monthly operations.
      The keys are account names, and the values are the corresponding operation amounts.
    - cashback (int): The expected cashback value.

    Returns:
    - None: The function asserts the result of calculate_cashback with the expected cashback value.
    """
    assert calculate_cashback(monthly_operations) == cashback


def test_calculate_cashback_zero_expenses() -> None:
    """
    Test the calculate_cashback function with zero expenses.

    This function tests the calculate_cashback function by providing a dictionary with a single account
    and zero expenses. It checks that the function returns a dictionary with the account name as the key
    and a list containing two zeros as the value.

    Parameters:
    - monthly_operations (dict[str, float]): A dictionary representing the monthly operations.
      The keys are account names, and the values are the corresponding operation amounts.
      In this case, the dictionary contains a single account with the key "NaN" and a value of 0.0.

    Returns:
    - None: The function asserts the result of calculate_cashback with the expected dictionary.
    """
    assert calculate_cashback({"nan": 0.0}) == {"nan": [0.0, 0.0]}


def test_process_cards_info(cashback: dict[str, Any]) -> None:
    """
    Test the process_cards_info function.

    This function tests the process_cards_info function by comparing the result of the function
    with the expected output. The expected output is a list of dictionaries, where each dictionary
    represents a card's information.

    Parameters:
    - cashback (dict[str, Any]): A dictionary containing the cashback information for each card.
                                The keys are account names, and the values are lists containing
                                the total spent and cashback amounts.

    Returns:
    - None: The function asserts the result of process_cards_info with the expected output.
    """
    assert process_cards_info(cashback)[:3] == [
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
    ]


def test_sort_by_amount(get_df: pd.DataFrame) -> None:
    """
    Test the function `sort_by_amount` to sort the transactions data by the amount.

    This function tests the `sort_by_amount` function by comparing the first transaction
    in the sorted list with an expected transaction dictionary. The expected dictionary
    contains the expected values for each transaction attribute.

    Parameters:
    get_df: A DataFrame containing the transactions data. The DataFrame is expected to have
            the following columns: "Дата операции", "Дата платежа", "Номер карты", "Статус",
            "Сумма операции", "Валюта операции", "Сумма платежа", "Валюта платежа",
            "Кэшбэк", "Категория", "MCC", "Описание", "Бонусы (включая кэшбэк)",
            "Округление на инвесткопилку", "Сумма операции с округлением", "Sum_without_sign".

    Returns:
    None: The function asserts the result of the `sort_by_amount` function.
    """
    assert sort_by_amount(get_df)[0] == {
        "Дата операции": "31.01.2018 20:09:33",
        "Дата платежа": "31.01.2018",
        "Номер карты": "*4556",
        "Статус": "OK",
        "Сумма операции": -1212.8,
        "Валюта операции": "RUB",
        "Сумма платежа": -1212.8,
        "Валюта платежа": "RUB",
        "Кэшбэк": 12.0,
        "Категория": "Ж/д билеты",
        "MCC": "4112",
        "Описание": "РЖД",
        "Бонусы (включая кэшбэк)": 12.0,
        "Округление на инвесткопилку": 0.0,
        "Сумма операции с округлением": 1212.8,
        "Sum_without_sign": 1212.8,
    }


def test_get_top_transactions(get_df):
    """
    Test the function `get_top_transactions` to retrieve the top five transactions.

    Parameters:
    get_df: A DataFrame containing the transactions data.

    Returns:
    None: The function asserts the result of the `get_top_transactions` function.
    """
    transactions_list = sort_by_amount(get_df)
    assert get_top_transactions(transactions_list)[:2] == [
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
    ]


def test_process_cards_info_empty_data() -> None:
    """
    Tests the function `process_cards_info` for empty data.

    This function tests the `process_cards_info` function by passing an empty dictionary.
    It verifies that the function returns an empty list.

    Parameters: None

    Returns: None: The function asserts the result.
    """
    assert process_cards_info({"NaN": [0.0, 0.0]}) == []


@patch("src.utils.logger")
def test_valid_hour_morning(mock_logger: MagicMock) -> None:
    """
    Test the function `say_hello` for a morning hour.

    This function tests the `say_hello` function by setting the current time to 7:00.
    It verifies that the function returns the correct greeting message "Доброе утро!"
    and logs the appropriate information using the `mock_logger`.

    Parameters:
    - mock_logger (MagicMock): A mock object for the logger.
                        This is used to verify that the function logs the correct information.

    Returns: None: The function asserts the result and logs the information.
    """
    assert say_hello(datetime(2022, 1, 1, 7, 0, 0)) == "Доброе утро!"
    mock_logger.info.assert_called_with("Час 7 является допустимой величиной.")


@patch("src.utils.logger")
def test_valid_hour_afternoon(mock_logger: MagicMock) -> None:
    """
    Test the function `say_hello` for an afternoon hour.

    This function tests the `say_hello` function by setting the current time to 15:00.
    It verifies that the function returns the correct greeting message "Доброго дня!"
    and logs the appropriate information using the `mock_logger`.

    Parameters:
    - mock_logger (MagicMock): A mock object for the logger.

    Returns:
    - None: The function asserts the result and logs the information.
    """
    assert say_hello(datetime(2022, 1, 1, 15, 0, 0)) == "Добрый день!"
    mock_logger.info.assert_called_with("Час 15 является допустимой величиной.")


@patch("src.utils.logger")
def test_valid_hour_evening(mock_logger: MagicMock) -> None:
    """
    Test the function `say_hello` for an evening hour.

    This function tests the `say_hello` function by setting the current time to 20:00.
    It verifies that the function returns the correct greeting message "Добрый вечер!"
    and logs the appropriate information using the `mock_logger`.

    Parameters:
    - mock_logger (MagicMock): A mock object for the logger.
            This is used to verify that the function logs the correct information.

    Returns:
    - None: The function asserts the result and logs the information.
    """
    assert say_hello(datetime(2022, 1, 1, 20, 0, 0)) == "Добрый вечер!"
    mock_logger.info.assert_called_with("Час 20 является допустимой величиной.")


@patch("src.utils.logger")
def test_valid_hour_night(mock_logger: MagicMock) -> None:
    """
    Test the function `say_hello` for a night hour.

    This function tests the `say_hello` function by setting the current time to 23:00.
    It verifies that the function returns the correct greeting message "Доброй ночи!"
    and logs the appropriate information using the `mock_logger`.

    Parameters:
    - mock_logger (MagicMock): A mock object for the logger.

    Returns:
    - None: The function asserts the result and logs the information.
    """
    assert say_hello(datetime(2022, 1, 1, 23, 0, 0)) == "Доброй ночи!"
    mock_logger.info.assert_called_with("Час 23 является допустимой величиной.")


@patch("src.utils.logger")
def test_invalid_hour(mock_logger: MagicMock) -> None:
    """
    Test the function `say_hello` for an invalid hour.

    This function tests the `say_hello` function by setting the current time to 24,
    which is an invalid hour. It verifies that the function logs a warning message
    and returns a specific error message.

    Parameters:
    - self (unittest.TestCase): The test case instance.
    - mock_logger (MagicMock): A mock object for the logger.

    Returns:
    - None: The function asserts the result and logs the warning message.
    """
    with pytest.raises(ValueError) as ex:
        say_hello(datetime(2022, 1, 1, 24, 0, 0))
    assert ex.value.args[0] == "hour must be in 0..23"


@patch("src.utils.json.load")
@patch("src.utils.open")
def test_get_currencies(mock_open: MagicMock, mock_json_load: MagicMock, currencies: list[str]) -> None:
    """
    Test the get_currencies function.

    This function tests the get_currencies function by mocking the open and json.load functions.
    It asserts that the function returns the expected list of currencies and verifies
    that the open function is called once with the correct arguments.

    Parameters:
    mock_open (MagicMock): A mock object for the open function.
    mock_json_load (MagicMock): A mock object for the json.load function.
    currencies (list[str]): A list of currencies to be returned by the mock json.load function.

    Returns:
    None
    """
    mock_json_load.return_value = currencies
    assert get_currencies("currencies.json") == ["USD", "EUR", "CNY", "JPY", "KZT"]
    mock_open.assert_called_once_with("currencies.json", "r", encoding="utf-8")


def test_get_currencies_no_such_file(capsys: pytest.CaptureFixture) -> None:
    """
    Test the get_currencies function when the file does not exist.

    Parameters:
    capsys (pytest.CaptureFixture): A fixture for capturing stdout and stderr.

    Returns:
    None

    This function asserts that the get_currencies function returns an empty list when
    the specified file does not exist. It also asserts that the appropriate error message
    is printed to stdout.
    """
    file_name = "no_such_file.json"
    assert get_currencies(file_name) == []
    captured = capsys.readouterr()
    assert captured.out == f"Файл {file_name} с кодами валют не найден.\n"


def test_get_currencies_json_decode_error() -> None:
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as tmp_file:
        data = """{
            "symbol": "KZT",
            "name": {"Kazakhstani Tenge"},
            "symbol_native": "тңг.",
            "decimal_digits": 2,
            "rounding": 0,
            "code": "KZT",
            "name_plural": "Kazakhstani tenges"
        }"""
        tmp_file.write(data)
        file_path = tmp_file.name
    assert get_currencies(file_path) == []


@patch("src.utils.json.load")
@patch("src.utils.open")
def test_get_stocks(mock_open: MagicMock, mock_json_load: MagicMock, stocks: list[str]) -> None:
    mock_json_load.return_value = stocks
    assert get_stocks("stocks.json") == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    mock_open.assert_called_once_with("stocks.json", "r", encoding="utf-8")


def test_get_stocks_no_such_file(capsys: pytest.CaptureFixture) -> None:
    """
    Test the get_stocks function when the file does not exist.

    Parameters:
    capsys (pytest.CaptureFixture): A fixture for capturing stdout and stderr.

    Returns:
    None

    This function asserts that the get_stocks function returns an empty list when
    the specified file does not exist. It also asserts that the appropriate error message
    is printed to stdout.
    """
    file_name = "no_such_file.json"
    assert get_stocks(file_name) == []
    captured = capsys.readouterr()
    assert captured.out == f"Файл {file_name} не найден.\n"


def test_get_stocks_json_decode_error() -> None:
    """
    Test the get_stocks function when the JSON data in the file is not properly formatted.
    Parameters: None
    Returns:  None

    This function creates a temporary file, writes improperly formatted JSON data to it,
    and then calls the get_stocks function with the file path. It asserts that the function
    returns an empty list, indicating that the JSON data could not be decoded.
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as tmp_file:
        data = "company: Apple Inc, tickerSymbol: AAPL"
        tmp_file.write(data)
        file_path = tmp_file.name
    assert get_stocks(file_path) == []


@pytest.mark.parametrize(
    "input_currencies, input_stocks, user_currencies, user_stocks",
    [
        ("USD,eur CNy, JPY", "aapl,GOOGL tSLA, AMZN", ["USD", "EUR", "CNY", "JPY"], ["AAPL", "GOOGL", "TSLA", "AMZN"]),
        ("KZt", "aapl,GOOGL tSLA, AMZN", ["KZT"], ["AAPL", "GOOGL", "TSLA", "AMZN"]),
        ("eur CNy", "msft ", ["EUR", "CNY"], ["MSFT"]),
    ],
)
@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.utils.json.dump")
@patch("src.utils.open")
@patch("src.utils.get_stocks")
@patch("src.utils.get_currencies")
def test_get_data_from_user(
    mock_get_currencies: MagicMock,
    mock_get_stocks: MagicMock,
    mock_open: MagicMock,
    mock_json_dump: MagicMock,
    mock_join: MagicMock,
    mock_dirname: MagicMock,
    input_currencies: str,
    input_stocks: str,
    user_currencies: str,
    user_stocks: str,
) -> None:
    """
    This function tests the get_data_from_user function from the src.utils module.

    Parameters:
    mock_get_currencies (MagicMock): A mock object used to replace the get_currencies function.
    mock_get_stocks (MagicMock): A mock object used to replace the get_stocks function.
    mock_open (MagicMock): A mock object used to replace the open function.
    mock_json_dump (MagicMock): A mock object used to replace the json.dump function.
    mock_join (MagicMock): A mock object used to replace the os.path.join function.
    mock_dirname (MagicMock): A mock object used to replace the os.path.dirname function.
    input_currencies (str): A string representing the input currencies.
    input_stocks (str): A string representing the input stocks.
    user_currencies (list): A list representing the expected user currencies.
    user_stocks (list): A list representing the expected user stocks.

    Returns:
    None. This function is used for testing purposes and does not return any value.
    """
    mock_get_currencies.return_value = ["USD", "EUR", "CNY", "JPY", "KZT"]
    mock_get_stocks.return_value = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    get_data_from_user(input_currencies, input_stocks)
    mock_open.assert_called_once_with("/mock/path/user_settings.json", "w", encoding="utf-8")
    mock_json_dump.assert_called_with(
        {"user_currencies": user_currencies, "user_stocks": user_stocks}, mock_open().__enter__()
    )


@patch("src.utils.get_stocks")
@patch("src.utils.get_currencies")
def test_get_data_from_user_logger_messages(
    mock_get_currencies: MagicMock, mock_get_stocks: MagicMock, caplog: pytest.LogCaptureFixture
) -> None:
    """
    Test the get_data_from_user function's logging messages.

    Parameters:
    mock_get_currencies (MagicMock): A mock object used to replace the get_currencies function.
    mock_get_stocks (MagicMock): A mock object used to replace the get_stocks function.
    caplog (pytest.LogCaptureFixture): A fixture used to capture logging messages.

    Returns: None

    This function sets the return values of the mock_get_currencies and mock_get_stocks objects to empty lists.
    It then calls the get_data_from_user function with sample input values.
    Finally, it asserts that the "Перед началом чтения кодов валют и биржевых тикеров
    из пользовательского JSON-файла." message is present in the captured logging messages.
    """
    mock_get_currencies.return_value = []
    mock_get_stocks.return_value = []
    get_data_from_user("USD,eur CNy, JPY", "aapl,GOOGL tSLA, AMZN")
    assert "Перед началом чтения кодов валют и биржевых тикеров из пользовательского JSON-файла." in caplog.messages


@pytest.mark.parametrize(
    "input_currencies, input_stocks",
    [
        ("wrong_currency", "aapl,GOOGL tSLA, AMZN"),
        ("USD,eur CNy, JPY", "wrong_symbol"),
        ("byr", "tmos, MCX"),
    ],
)
@patch("src.utils.get_stocks")
@patch("src.utils.get_currencies")
def test_get_data_from_user_wrong_data(
    mock_get_currencies: MagicMock, mock_get_stocks: MagicMock, input_currencies: str, input_stocks: str
) -> None:
    """
    Test the get_data_from_user function when the input data is incorrect.

    Parameters:
    mock_get_currencies (MagicMock): A mock object used to replace the get_currencies function.
    mock_get_stocks (MagicMock): A mock object used to replace the get_stocks function.
    input_currencies (str): A string representing the input currencies.
    input_stocks (str): A string representing the input stocks.

    Returns:
    str: A message indicating that the input data is incorrect.

    This function sets the return values of the mock_get_currencies and mock_get_stocks objects to predefined lists.
    It then calls the get_data_from_user function with the input_currencies and input_stocks parameters.
    Finally, it asserts that the function returns the expected error message.
    """
    mock_get_currencies.return_value = ["USD", "EUR", "CNY", "JPY", "KZT"]
    mock_get_stocks.return_value = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    assert get_data_from_user(input_currencies, input_stocks) == "Проверьте правильность введенных данных."


@patch("src.utils.requests.get")
def test_get_data_via_api_currencies(mock_get: MagicMock, api_response_currencies: dict) -> None:
    """
    This function tests the get_data_via_api_currencies function from the src.utils module.

    Parameters:
    mock_get (MagicMock): A mock object used to replace the requests.get function.
    api_response_currencies (dict): A dictionary representing the API response for currencies.

    Returns:
    tuple: A tuple containing a boolean indicating the success of the API request and a list of currency rates.

    The function sets the status code and JSON response of the mock_get object to simulate a successful API request.
    It then calls the get_data_via_api_currencies function with a list of currencies.
    Finally, it asserts that the function returns the expected result (True, [87.99, 95.18, 11.89, 59.64, 18.44]).
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = api_response_currencies
    result = get_data_via_api_currencies(["USD", "EUR", "CNY", "JPY", "KZT"])
    assert result == (True, [87.99, 95.18, 11.89, 59.64, 18.44])


@patch("src.utils.requests.get")
def test_get_data_via_api_currencies_denied_request(mock_get: MagicMock) -> None:
    """
    Test the get_data_via_api_currencies function when the API request is denied.

    Parameters: mock_get (MagicMock): A mock object for the requests.get function.
    Returns: None

    This function sets the status code and reason for the mock_get object to simulate a denied request.
    It then calls the get_data_via_api_currencies function with a list of currencies.
    Finally, it asserts that the function returns the expected result (False, "Forbidden").
    """
    mock_get.return_value.status_code = 403
    mock_get.return_value.reason = "Forbidden"
    result = get_data_via_api_currencies(["USD", "EUR", "CNY", "JPY", "KZT"])
    assert result == (False, "Forbidden")


def test_get_data_via_api_currencies_request_error() -> None:
    """
    This function tests the case when a RequestException occurs during the API request for currency data.

    Parameters: None
    Returns: None

    The function uses a mock patch to replace the requests.get function with a side effect
    that raises a RequestException.
    It then calls the get_data_via_api_currencies function with a list of currencies.
    Finally, it asserts that the function returns the expected result (False, "Something went wrong").
    """
    with mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Something went wrong")):
        result = get_data_via_api_currencies(["USD", "EUR", "CNY", "JPY", "KZT"])
    assert result == (False, "Something went wrong")


@patch("src.utils.requests.get")
def test_get_data_via_api_stocks(mock_get: MagicMock, api_response_stocks: dict) -> None:
    """
    This function tests the get_data_via_api_stocks function from the src.utils module.

    Parameters:
    mock_get (MagicMock): A mock object used to replace the requests.get function.
    api_response_stocks (dict): A dictionary representing the API response for stocks.

    Returns:
    tuple: A tuple containing a boolean indicating the success of the API request and a list of stock prices.

    The function sets the status code and JSON response of the mock_get object to simulate a successful API request.
    It then calls the get_data_via_api_stocks function with a list of stock symbols.
    Finally, it asserts that the function returns the expected result (True, [216.24, 166.94, 163.67, 406.02, 200]).
    """
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = api_response_stocks
    result = get_data_via_api_stocks(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
    assert result == (True, [216.24, 166.94, 163.67, 406.02, 200])


@patch("src.utils.requests.get")
def test_get_data_via_api_stocks_denied_access(mock_get: MagicMock) -> None:
    """
    This function tests the case when the API request for stock data is denied.

    Parameters:
    mock_get (MagicMock): A mock object used to replace the requests.get function.

    Returns:
    tuple: A tuple containing a boolean indicating the success of the API request
    and a string indicating the reason for the failure.

    The function sets the status code and reason for the mock_get object to simulate a denied request.
    It then calls the get_data_via_api_stocks function with a list of stock symbols.
    Finally, it asserts that the function returns the expected result (False, "Unauthorized").
    """
    mock_get.return_value.status_code = 401
    mock_get.return_value.reason = "Unauthorized"
    result = get_data_via_api_stocks(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
    assert result == (False, "Unauthorized")


def test_get_data_via_api_stocks_request_error() -> None:
    """
    This function tests the case when a RequestException occurs during the API request for stock data.

    Parameters: None

    Returns: tuple: A tuple containing a boolean indicating the success of the API request
            and a string indicating the reason for the failure.

    The function uses a mock patch to replace the requests.get function with a side effect
    that raises a RequestException.
    It then calls the get_data_via_api_stocks function with a list of stock symbols.
    Finally, it asserts that the function returns the expected result (False, "Something went wrong").
    """
    with mock.patch("requests.get", side_effect=requests.exceptions.RequestException("Something went wrong")):
        result = get_data_via_api_stocks(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
    assert result == (False, "Something went wrong")


@patch("src.utils.get_data_via_api_currencies")
def test_get_exchange_rates(mock_get_currencies: MagicMock) -> None:
    """
    This function tests the get_exchange_rates function from the src.utils module.

    Parameters:
    mock_get_currencies (MagicMock): A mock object used to replace the get_data_via_api_currencies function.

    Returns: None

    The function sets the return value of the mock_get_currencies object to simulate a successful API request.
    It then calls the get_exchange_rates function with a list of currencies.
    Finally, it asserts that the function returns the expected result (True, [87.99, 95.18, 11.89, 59.64, 18.44]).
    """
    mock_get_currencies.return_value = (True, [87.99, 95.18, 11.89, 59.64, 18.44])
    assert get_exchange_rates(["USD", "EUR", "CNY", "JPY", "KZT"])[:2] == [
        {"currency": "USD", "rate": 87.99},
        {"currency": "EUR", "rate": 95.18},
    ]


@pytest.mark.parametrize("return_status, return_result", [(False, "Forbidden"), (False, "Something went wrong")])
@patch("src.utils.get_data_via_api_currencies")
def test_get_exchange_rates_unsuccessful_operation(
    mock_get_currencies: MagicMock, return_status: bool, return_result: str
) -> None:
    """
    Test the get_exchange_rates function when the API request is unsuccessful.

    Parameters:
    mock_get_currencies (MagicMock): A mock object used to replace the get_data_via_api_currencies function.
    return_status (bool): The status of the API request. If False, the request is unsuccessful.
    return_result (str): The reason for the unsuccessful request.

    Returns:
    None: If the API request is unsuccessful, the function asserts that the return value of get_exchange_rates is None.

    The function sets the return value of the mock_get_currencies object to simulate an unsuccessful API request.
    It then calls the get_exchange_rates function with a list of currencies.
    Finally, it asserts that the function returns None when the API request is unsuccessful.
    """
    mock_get_currencies.return_value = (return_status, return_result)
    assert get_exchange_rates(["USD", "EUR", "CNY", "JPY", "KZT"]) is None


@patch("src.utils.get_data_via_api_stocks")
def test_get_stock_prices(mock_get_stocks: MagicMock) -> None:
    """
    Test the get_stock_prices function from the src.utils module.

    Parameters:
    mock_get_stocks (MagicMock): A mock object used to replace the get_data_via_api_stocks function.

    Returns: None

    The function sets the return value of the mock_get_stocks object to simulate a successful API request.
    It then calls the get_stock_prices function with a list of stock symbols.
    Finally, it asserts that the first two stock prices returned by the function match the expected values.
    """
    mock_get_stocks.return_value = (True, [216.24, 166.94, 163.67, 406.02, 200])
    assert get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])[:2] == [
        {"stock": "AAPL", "price": 216.24},
        {"stock": "AMZN", "price": 166.94},
    ]


@pytest.mark.parametrize("return_status, return_result", [(False, "Unauthorized"), (False, "Something went wrong")])
@patch("src.utils.get_data_via_api_stocks")
def test_get_stock_prices_unsuccessful_operation(
    mock_get_stocks: MagicMock, return_status: bool, return_result: str
) -> None:
    """
    Test the get_stock_prices function when the API request is unsuccessful.

    Parameters:
    mock_get_stocks (MagicMock): A mock object used to replace the get_data_via_api_stocks function.
    return_status (bool): The status of the API request. If False, the request is unsuccessful.
    return_result (str): The reason for the unsuccessful request.

    Returns:
    []: If the API request is unsuccessful, the function asserts that the return value of get_stock_prices is None.

    The function sets the return value of the mock_get_stocks object to simulate an unsuccessful API request.
    It then calls the get_stock_prices function with a list of stock symbols.
    Finally, it asserts that the function returns None when the API request is unsuccessful.
    """
    mock_get_stocks.return_value = (return_status, return_result)
    assert get_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]) == []


@patch("src.utils.pd.read_excel")
def test_get_data_from_xlsx(mock_read_excel: Any, get_df: pd.DataFrame) -> None:
    """
    This function tests the get_data_from_xlsx function from the src.external_api module.

    Parameters:
    mock_read_excel (Any): A mock object used to replace the pd.read_excel function.
    get_df (pd.DataFrame): A DataFrame object used for testing.

    Returns:
    None. This function is used for testing purposes and does not return any value.

    The function sets the return value of the mock_read_excel object to get_df.
    It then calls the get_data_from_xlsx function with the file name "existing.xlsx"
    and asserts that the returned DataFrame is equal to get_df.
    Finally, it asserts that the mock_read_excel function was called once with the file name "existing.xlsx".
    """
    mock_read_excel.return_value = get_df
    assert read_excel2dataframe("existing.xlsx").equals(get_df)
    mock_read_excel.assert_called_once_with("existing.xlsx")


def test_read_excel2dataframe_no_such_file(get_empty_df: pd.DataFrame, capsys: pytest.CaptureFixture):
    """
    This function tests the case when the specified Excel file does not exist.

    Parameters:
    get_empty_df (pd.DataFrame): A DataFrame object used for testing when the file does not exist.
    capsys (pytest.CaptureFixture): A fixture used to capture stdout and stderr during testing.

    Returns:
    None. This function is used for testing purposes and does not return any value.

    The function sets the file name to "no_such_file.xlsx".
    It then calls the get_data_from_xlsx function with the file name.
    After that, it captures the stdout using the capsys fixture.
    It asserts that the captured stdout contains the error
    message "Файл не найден. Проверьте правильность введенных данных."
    Finally, it asserts that the DataFrame returned by the get_data_from_xlsx function is equal to get_empty_df.
    """
    file_name = "no_such_file.xlsx"
    read_excel2dataframe(file_name)
    captured = capsys.readouterr()
    assert captured.out == f"Файл {file_name} не найден.\n"
    assert read_excel2dataframe(file_name).equals(get_empty_df)
