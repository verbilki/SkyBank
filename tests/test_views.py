from datetime import datetime
from unittest.mock import MagicMock, patch

from pandas import DataFrame

from src.views import generate_json_response


@patch("os.path.dirname", return_value="/mock/path")
@patch("os.path.join", side_effect=lambda *args: "/".join(args))
@patch("src.views.get_stock_prices")
@patch("src.views.get_exchange_rates")
@patch("src.views.get_top_transactions")
@patch("src.views.process_cards_info")
@patch("src.views.json.load")
@patch("src.views.open")
def test_generate_json_response(
    mock_open: MagicMock,
    mock_json: MagicMock,
    mock_process_cards_info: MagicMock,
    mock_get_top_transactions: MagicMock,
    mock_get_get_exchange_rates: MagicMock,
    mock_get_stock_prices: MagicMock,
    mock_join: MagicMock,
    mock_dirname: MagicMock,
    json_response: str,
    get_df: DataFrame,
) -> None:
    mock_json.return_value = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN"]}

    mock_process_cards_info.return_value = [
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
    mock_get_top_transactions.return_value = [
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
    mock_get_get_exchange_rates.return_value = [
        {"currency": "USD", "rate": 87.99},
        {"currency": "EUR", "rate": 95.18},
    ]
    mock_get_stock_prices.return_value = [
        {"stock": "AAPL", "price": 216.24},
        {"stock": "AMZN", "price": 166.94},
    ]
    assert generate_json_response(datetime(2022, 3, 8, 15, 45, 0), get_df) == json_response
    mock_open.assert_called_once_with("/mock/path/user_settings.json")
