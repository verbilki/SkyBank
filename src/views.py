import json
import os
from datetime import datetime

import pandas as pd

from src.utils import (calculate_cashback, filter_by_date, get_data_from_user, get_exchange_rates, get_stock_prices,
                       get_top_transactions, get_total_expenses, process_cards_info, say_hello, sort_by_amount)


def generate_json_response(report_datetime: datetime, df: pd.DataFrame) -> str:
    prj_root = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(prj_root, "user_settings.json")) as settings_file:
        try:
            user_settings = json.load(settings_file)

        except json.JSONDecodeError:
            print(
                "Для корректной работы приложения введите коды валют и тикеры акций компаний S&P 500,"
                " которые будут отображаться на главной странице приложения."
            )

            currencies = input("Введите коды валют (разделитель - запятая или пробел): ")
            stocks = input("Введите тикеры акций компаний S&P 500 (разделитель - запятая или пробел): ")

            check_input = get_data_from_user(currencies, stocks)

            while check_input:
                print(check_input)
                currencies = input("\nВведите коды валют (разделитель - запятая или пробел): ")
                stocks = input("Введите тикеры акций компаний S&P 500 (разделитель - запятая или пробел): ")
                check_input = get_data_from_user(currencies, stocks)

    df_filtered = filter_by_date(report_datetime, df)
    current_month_expenses = calculate_cashback(get_total_expenses(df_filtered))

    result_dict = {
        "greeting": say_hello(report_datetime),
        "cards": process_cards_info(current_month_expenses),
        "top_transactions": get_top_transactions(sort_by_amount(df_filtered)),
        "currency_rates": get_exchange_rates(user_settings.get("user_currencies")),
        "stock_prices": get_stock_prices(user_settings.get("user_stocks")),
    }

    return json.dumps(result_dict, ensure_ascii=False, indent=4)
