import json
import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd

from src.utils import get_basename

logger = logging.getLogger(get_basename(__file__))
logger.setLevel(logging.INFO)
prj_root = os.path.dirname(os.path.dirname(__file__))
log_file_path = os.path.join(prj_root, "logs", get_basename(__file__) + ".log")
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transactions_list(df: pd.DataFrame) -> list[dict[str, str | float]]:
    logger.info("Преобразование DataFrame в список словарей транзакций.")
    transactions = df.to_dict(orient="records")
    logger.info(
        "Начало преобразования поля 'Дата операции' в словаре"
        " из формата 'dd.mm.yyyy hh:mm:ss' в формат 'yyyy-mm-dd'."
    )
    try:
        return [
            {
                "Дата операции": datetime.strftime(
                    datetime.strptime(transaction.get("Дата операции", "1900-01-01 00:00:00"), "%d.%m.%Y %H:%M:%S"),
                    "%Y-%m-%d",
                ),
                "Сумма операции": transaction.get("Сумма операции", 0.0),
            }
            for transaction in transactions
        ]
    except Exception as ex:
        logger.error(ex)
        return []


def filter_by_year_month(year_month: str, transactions_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    This function filters a list of transactions based on a given year-month.

    Parameters:
    year_month (str): A string representing the year and month in the format 'YYYY-MM'.
    transactions_list (list[dict[str, Any]]): A list of dictionaries, where each dictionary represents a transaction.
        The dictionary should contain a key 'Дата операции' with a string value representing the transaction date.

    Returns:
    list[dict[str, Any]]: A list of dictionaries representing the transactions that match the given year-month.
        If the input year_month does not match the format 'YYYY-MM', an empty list is returned.
    """
    try:
        logger.info(f"Проверка на соответствие входного параметра {year_month} формату YYYY-MM.")
        datetime.strptime(year_month, "%Y-%m")

    except ValueError as ex:
        logger.error(ex)
        print(f"Дата {year_month} не соответствует формату YYYY-MM.")
        return []
    else:
        logger.info("Возврат списка транзакций по заданному году-месяцу.")
        return [
            transaction
            for transaction in transactions_list
            if transaction.get("Дата операции", "1900-01-01 00:00:00")[:7] == year_month
        ]


def round_to_limit(amount: float, rounding_limit: int) -> float:
    logger.info(
        f"Попытка расчёта дополнения для суммы {amount} до ближайшего значения,"
        f" кратного заданному округлению {rounding_limit}."
    )

    if rounding_limit not in [10, 50, 100]:
        logger.warning(f"Лимит округления: {rounding_limit} не соответствует допустимому списку: 10, 50, 100.")
        print(f"Лимит округления {rounding_limit} не соответствует допустимому списку: 10, 50, 100.")
        return 0.0

    addition_nearest_rounding = (
        rounding_limit - round(abs(amount) % rounding_limit, 2) if abs(amount) % rounding_limit != 0 else 0.0
    )
    logger.info(
        f"Для суммы {amount} дополением до ближайшего значения,"
        f" кратного {rounding_limit}, является {addition_nearest_rounding}."
    )
    return addition_nearest_rounding


def investment_bank(report_dt: datetime, transactions: list[dict[str, Any]], limit: int) -> str:
    year_month = report_dt.strftime("%Y-%m")
    filtered_transactions = filter_by_year_month(year_month, transactions)
    result = {}

    if filtered_transactions:
        amounts = [transaction.get("Сумма операции", 0.0) for transaction in filtered_transactions]
        result = {
            "month": year_month,
            "investment_amount": sum(round_to_limit(float(amount), limit) for amount in amounts),
        }
    return json.dumps(result, indent=4)
