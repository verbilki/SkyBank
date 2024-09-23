import json
from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.reports import spending_by_category, write_to_file


def test_spending_by_category(get_df: pd.DataFrame, dec_df: pd.DataFrame) -> None:
    """
    This function tests the `spending_by_category` function by comparing the output with the expected result.

    Parameters:
    get_df (pd.DataFrame): A DataFrame containing the transactions data for the current month.
    dec_df (pd.DataFrame): A DataFrame containing the expected transactions data for December.

    Returns:
    None: The function asserts the equality of the output and the expected result.
    """
    assert spending_by_category(get_df, "Фастфуд", datetime(2021, 12, 1, 12, 35, 5)) == json.dumps(
        dec_df.to_dict(orient="records"), ensure_ascii=False, indent=4
    )


@patch("src.reports.pd.DataFrame.to_dict")
def test_spending_by_category_json_dumps_error(
    mock_df_to_dict: MagicMock, get_df: pd.DataFrame, caplog: pytest.LogCaptureFixture
) -> None:
    mock_df_to_dict.return_value = {
        "symbol": "KZT",
        "name": {"Kazakhstani Tenge"},
        "symbol_native": "тңг.",
        "decimal_digits": 2,
        "rounding": 0,
        "code": "KZT",
        "name_plural": "Kazakhstani tenges",
    }
    assert spending_by_category(get_df, "Фастфуд", datetime(2021, 12, 1, 12, 35, 5)) is None
    assert "Object of type set is not JSON serializable" in caplog.messages


def test_spending_by_category_no_transactions(get_df: pd.DataFrame) -> None:
    """
    Test the function `spending_by_category` when there are no transactions for the given category.

    Parameters:
    get_df (pd.DataFrame): A DataFrame containing the transactions data.

    Returns: str: The function returns an empty list as a JSON string.
    """
    assert spending_by_category(get_df, "Not existing category", datetime(2021, 12, 1, 12, 35, 5)) == "[]"


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("json.dump")
def test_write_to_json(
    mock_json_dump: MagicMock, mock_os_join: MagicMock, mock_dirname: MagicMock, mock_open_file: MagicMock
) -> None:
    """
    Test the function `write_to_file` with the `json.dump` method.

    The function `write_to_file` is used to write the output of a function to a file.
    In this test, the function `write_to_file` is used with the `json.dump` method to write
    a JSON string to a JSON file.

    The mock objects are used to mock the `open` function and the `os.path.dirname` and `os.path.join` functions.
    The mock objects are used to simulate the writing of the JSON string to a file.

    The test asserts that the `open` function is called with the correct arguments and that the `json.dump`
    method is called with the correct arguments.

    """

    @write_to_file(file_name="test.json")
    def mock_function():
        return json.dumps({"key": "value"})

    mock_os_join.return_value = "/mock/path/data/test.json"
    mock_function()

    mock_open_file.assert_called_with("/mock/path/data/test.json", "w", encoding="utf-8")
    mock_json_dump.assert_called_once_with(
        {"key": "value"}, mock_open_file().__enter__(), ensure_ascii=False, indent=4
    )


@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("pandas.DataFrame.to_csv")
def test_write_to_csv(mock_to_csv: MagicMock, mock_os_join: MagicMock, mock_dirname: MagicMock) -> None:
    """
    This function tests the `write_to_file` decorator with the `to_csv` method.

    The `write_to_file` decorator is used to write the output of a function to a file.
    In this test, the `write_to_file` decorator is used with the `to_csv` method to write
    a DataFrame to a CSV file.

    Args:
    mock_to_csv (MagicMock): A mock object for the `to_csv` method of a DataFrame.
    mock_os_join (MagicMock): A mock object for the `os.path.join` function.
    mock_dirname (MagicMock): A mock object for the `os.path.dirname` function.

    Returns:
    None: The function asserts the behavior of the `write_to_file` decorator with the `to_csv` method.
    """

    @write_to_file(file_name="test.csv")
    def mock_function() -> str:
        """
        This function is a mock function used for testing the `write_to_file` decorator.
        It returns a JSON string representing a DataFrame.

        Returns:
        str: A JSON string representing a DataFrame.
        """
        return json.dumps([{"key": "value"}])

    mock_os_join.return_value = "/mock/path/data/test.csv"
    mock_function()
    mock_to_csv.assert_called_once_with("/mock/path/data/test.csv", index=False)


@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("pandas.DataFrame.to_excel")
def test_write_to_excel(mock_to_excel: MagicMock, mock_os_join: MagicMock, mock_dirname: MagicMock) -> None:
    """
    This function tests the `write_to_file` decorator with the `to_excel` method.

    The `write_to_file` decorator is used to write the output of a function to a file.
    In this test, the `write_to_file` decorator is used with the `to_excel` method to write
    a DataFrame to an Excel file.

    Args:
    mock_to_excel (MagicMock): A mock object for the `to_excel` method of a DataFrame.
    mock_os_join (MagicMock): A mock object for the `os.path.join` function.
    mock_dirname (MagicMock): A mock object for the `os.path.dirname` function.

    Returns:
    None: The function asserts the behavior of the `write_to_file` decorator with the `to_excel` method.
    """

    @write_to_file(file_name="test.xlsx")
    def mock_function() -> str:
        return json.dumps([{"key": "value"}])

    mock_os_join.return_value = "/mock/path/data/test.xlsx"
    mock_function()

    mock_to_excel.assert_called_once_with("/mock/path/data/test.xlsx", index=False)


@patch("builtins.open", new_callable=mock_open)
def test_write_to_file_insufficient_permissions(mock_open: mock.Mock) -> None:
    """
    Test that the function `write_to_file` raises a PermissionError when given a file with insufficient permissions.

    Args:
        mock_open (mock.Mock): A mock object for the built-in open() function.
    """

    @mock.patch("src.reports.open", side_effect=PermissionError("Permission denied"))
    def test_write_to_file_insufficient_permissions(mock_open: mock.Mock) -> None:
        report_file = "test_file.json"

        @write_to_file(report_file)
        def sample_function() -> str:
            return json.dumps({"key": "value"})

        with mock.patch("src.reports.logger") as mock_logger:
            with pytest.raises(PermissionError):
                sample_function()

        mock_open.assert_called_once_with(report_file, "w", encoding="utf-8")
        mock_logger.error.assert_called_once_with("Произошёл сбой при записи в файл: Permission denied")
