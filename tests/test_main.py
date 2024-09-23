from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.main import get_user_date


@patch("builtins.input", return_value="15.09.23")
def test_get_user_date_success(mock_input: MagicMock):
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 9, 15)
        result = get_user_date()
        assert result == datetime(2023, 9, 15)


@patch("builtins.input", return_value="01.05.32")
def test_get_user_date_failure(mock_input: MagicMock):
    with patch("datetime.datetime"):
        mock_input.side_effect = Exception("Искусственно сгенерированное исключение с помощью объекта Mock.")
        with pytest.raises(Exception) as excinfo:
            get_user_date()
        assert str(excinfo.value) == "Искусственно сгенерированное исключение с помощью объекта Mock."


# def test_get_user_date_input_validation(capsys: pytest.CaptureFixture):
#     with patch("builtins.input", return_value=" invalid input "):
#         get_user_date()
#         captured = capsys.readouterr()
#         assert "Invalid input" in captured.out
