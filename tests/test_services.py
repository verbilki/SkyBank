import json
from datetime import date, datetime
from typing import Any

import pandas as pd
import pytest
from pandas import DataFrame

from src.services import filter_by_year_month, get_transactions_list, investment_bank, round_to_limit


def test_get_transactions_list(get_df: DataFrame) -> None:
    """
    This function tests the get_transactions_list function.

    Parameters:
    get_df (DataFrame): A pandas DataFrame containing transaction data. The DataFrame should have at least two columns:
                        'Дата операции' (date of the transaction) and 'Сумма операции' (amount of the transaction).

    Returns:
    None: The function asserts the output of the get_transactions_list function against expected values.
    """
    assert get_transactions_list(get_df)[:2] == [
        {"Дата операции": "2021-12-01", "Сумма операции": -99.00},
        {"Дата операции": "2021-11-30", "Сумма операции": -55.00},
    ]


def test_get_transactions_list_empty_df(get_empty_df: pd.DataFrame) -> None:
    """
    This function tests the get_transactions_list function with an empty DataFrame.

    Parameters:
    get_empty_df (DataFrame): An empty pandas DataFrame.

    Returns:
    None: The function asserts the output of the get_transactions_list function against expected values.
    """
    assert get_transactions_list(get_empty_df) == []


def test_filter_by_year_month(transactions_list: list[dict[str, Any]]) -> None:
    """
    This function tests the filter_by_year_month function.

    Parameters:
    transactions_list (list[dict[str, Any]]): A list of dictionaries representing transactions.
        Each dictionary should have 'Дата операции' (date of the transaction)
        and 'Сумма операции' (amount of the transaction).

    Returns:
    None: The function asserts the output of the filter_by_year_month function against expected values.
    """
    assert filter_by_year_month("2021-12", transactions_list) == transactions_list[:2]
    assert filter_by_year_month("2021-11", transactions_list) == transactions_list[2:]


@pytest.mark.parametrize("date", ["2021-12-11", "11-12-2021", "2021.12", "12-2021"])
def test_filter_by_year_month_wrong_date(
    date: str, transactions_list: list[dict[str, Any]], capsys: pytest.CaptureFixture
) -> None:
    """
    Test the filter_by_year_month function with incorrect date format.

    Parameters:
    date (str): The date to filter transactions by. The date should be in the format 'YYYY-MM'.

    transactions_list (list[dict[str, Any]]): A list of dictionaries representing transactions.

    capsys (pytest.CaptureFixture[str]): A fixture that captures stdout and stderr during test execution.

    Returns:
    None: The function asserts the output of the filter_by_year_month function against expected values
     and checks the captured output for the expected error message.
    """
    assert filter_by_year_month(date, transactions_list) == []
    captured = capsys.readouterr()
    assert captured.out == f"Дата {date} не соответствует формату YYYY-MM.\n"


def test_filter_by_year_month_empty_list() -> None:
    """
    This function tests the filter_by_year_month function with an empty list of transactions.

    Parameters:
    year_month (str): The year and month for which transactions need to be filtered.
                      The format should be 'YYYY-MM'.
    transactions_list (list[dict[str, Any]]): A list of dictionaries representing transactions.
                                             Each dictionary should have 'Дата операции' (date of the transaction)
                                             and 'Сумма операции' (amount of the transaction).

    Returns:
    None: The function asserts that when an empty list of transactions is passed to the
          filter_by_year_month function, it returns an empty list as well.
    """
    assert filter_by_year_month("2021-12", []) == []


@pytest.mark.parametrize(
    "amount, limit, expected",
    [
        (-160.67, 10, 9.33),
        (-150.89, 50, 49.11),
        (-32.0, 10, 8.0),
        (-11.0, 100, 89.0),
        (-89.0, 10, 1.0),
        (-122.0, 50, 28.0),
        (-144.0, 100, 56.0),
        (600.0, 10, 0.0),
        (600.0, 50, 0.0),
        (600.0, 100, 0.0),
    ],
)
def test_round_to_limit(amount: float, limit: int, expected: float) -> None:
    """
    Test the round_to_limit function with various input data.

    The function rounds the given amount to the nearest hundredth, but only if the absolute value of the amount
    exceeds the specified limit. If the absolute value of the amount is less than or equal to the limit, the function
    returns the amount as is.

    Parameters:
    amount (float): The amount to be rounded.
    limit (int): The limit value. The absolute value of the amount must exceed this limit for rounding to occur.
    expected (float): The expected result of the round_to_limit function.

    Returns:
    None: The function asserts the output of the round_to_limit function against the expected result.
    """
    assert round_to_limit(amount, limit) == expected


def test_round_to_limit_incorrect_limit(capsys: pytest.CaptureFixture) -> None:
    """
    Test the round_to_limit function when the provided limit is not in the valid list.

    This function asserts that the round_to_limit function returns 0.0 when an invalid limit is provided.
    It also checks that the function prints an error message to the console when an invalid limit is used.

    Parameters:
    capsys (pytest.CaptureFixture): A fixture that captures stdout and stderr during test execution.

    Returns:
    None: The function asserts the output of the round_to_limit function and checks the captured output.
    """
    assert round_to_limit(500.0, 45) == 0.0
    captured = capsys.readouterr()
    assert captured.out == "Лимит округления 45 не соответствует допустимому списку: 10, 50, 100.\n"


@pytest.mark.parametrize(
    "report_date, limit, expected",
    [
        (date(2021, 12, 1), 10, 15.11),
        (date(2021, 12, 1), 50, 75.11),
        (date(2021, 12, 1), 100, 75.11),
        (date(2021, 11, 1), 10, 24.5),
        (date(2021, 11, 1), 50, 104.5),
        (date(2021, 11, 1), 100, 204.5),
    ],
)
def test_investment_bank(
    report_date: date, limit: int, expected: float, transactions_list: list[dict[str, Any]]
) -> None:
    """
    This function tests the investment_bank function.

    Parameters:
    report_date (date): The date for which the investment amount needs to be calculated.
    limit (int): The limit value. The absolute value of the transaction amount must exceed this limit
        for rounding to occur.
    expected (float): The expected result of the investment_bank function.
        It represents the calculated investment amount for the given report_date and limit.

    transactions_list (list[dict[str, Any]]): A list of dictionaries representing transactions.
        Each dictionary should have 'Дата операции' (date of the transaction)
        and 'Сумма операции' (amount of the transaction).

    Returns:
    None: The function asserts the output of the investment_bank function against the expected result.
    """
    assert investment_bank(report_date, transactions_list, limit) == json.dumps(
        {"month": datetime.strftime(report_date, "%Y-%m"), "investment_amount": expected}, indent=4
    )


@pytest.mark.parametrize(
    "limit, expected",
    [
        (10, "{}"),
        (50, "{}"),
        (100, "{}"),
    ],
)
def test_investment_bank_no_transactions(transactions_list: list[dict[str, Any]], limit: int, expected: str) -> None:
    """
    Test the investment_bank function when there are no transactions for the specified year and month.

    Parameters:
    transactions_list (list[dict[str, Any]]): A list of dictionaries representing transactions.
        Each dictionary should have 'Дата операции' (date of the transaction)
        and 'Сумма операции' (amount of the transaction).
    limit (int): The limit value. The absolute value of the transaction amount must exceed this limit
        for rounding to occur.
    expected (Any): The expected result of the investment_bank function.
        If there are no transactions for the specified year and month, the function should return None.

    Returns:
    None: The function asserts the output of the investment_bank function against the expected result.
    """
    assert investment_bank(date(2021, 10, 1), transactions_list, limit) == expected


def test_investment_bank_wrong_limit(transactions_list: list[dict], capsys: pytest.CaptureFixture) -> None:
    assert investment_bank(date(2021, 11, 1), transactions_list, 25) == json.dumps(
        {"month": "2021-11", "investment_amount": 0.0}, indent=4
    )
    captured = capsys.readouterr()
    assert "Лимит округления 25 не соответствует допустимому списку: 10, 50, 100.\n" in captured.out
