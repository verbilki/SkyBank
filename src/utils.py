import json
import logging
import os
from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv


def get_basename(file_path: str = __file__) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]


logger = logging.getLogger(get_basename(__file__))
logger.setLevel(logging.INFO)

prj_root = os.path.dirname(os.path.dirname(__file__))
log_file_path = os.path.join(prj_root, "logs", get_basename(__file__) + ".log")
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_excel2dataframe(excel_file_path: str = "") -> pd.DataFrame | None:
    """
    This function reads an Excel file specified by the `excel_file_path` argument and returns a pandas DataFrame.
    If the file path is empty or the file is not a valid Excel file, the function returns None.

    Parameters:
    excel_file_path (str): The path to the Excel file to be read. If not provided, an empty string is used.

    Returns:
    pd.DataFrame | None: A pandas DataFrame containing the data from the Excel file
                        if the file is valid and readable.
        If the file is not found or is not a valid Excel file, the function returns None.
    """
    # if excel_file_path == "" or not is_valid_excel(excel_file_path):
    #     return None
    try:
        logger.info(f"Перед чтением Excel-файла {excel_file_path}.")
        df = pd.read_excel(excel_file_path)
        logger.info("Чтение Excel-файла прошло успешно.")
        return df

    except FileNotFoundError as ex:
        logger.error(ex)
        print(f"Файл {excel_file_path} не найден.")
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


def is_valid_excel(file_path: str) -> bool:
    """
    Check if the given file path points to a valid Excel file.

    The function checks if the file extension is either '.xlsx' or '.xls' and
    attempts to load the file using the appropriate library (openpyxl for '.xlsx' and xlrd for '.xls').
    If the file is successfully loaded, the function returns True. Otherwise, it returns False.

    Parameters:
    file_path (str): The path to the file to be checked.

    Returns:
    bool: True if the file is a valid Excel file, False otherwise.
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() not in [".xlsx", ".xls"]:
        return False

    try:
        if file_extension.lower() == ".xlsx":
            from openpyxl import load_workbook

            load_workbook(file_path)
        # elif file_extension.lower() == '.xls':
        #     import xlrd
        #     xlrd.open_workbook(file_path)
        return True
    except Exception:
        return False


def filter_by_date(filter_to_dt: datetime, df: pd.DataFrame) -> pd.DataFrame:
    """
    This function filters a pandas DataFrame based on a given date range.

    Parameters:
    filter_to_dt (datetime): The end date of the range. The function will include transactions with dates
        up to and including this date.
    df (pd.DataFrame): The pandas DataFrame to be filtered. It should contain a column named 'Дата операции'
        with datetime values.

    Returns:
    pd.DataFrame: A filtered pandas DataFrame containing only the rows that fall within the specified date range.
        If the input DataFrame does not contain the required column or if any errors occur
        during the filtering process, the function will return None.
    """
    logger.info("Определение даты начала и конца интервала фильтрации DataFrame.")
    from_dt = filter_to_dt.replace(day=1)

    logger.info("Создание в исходном DataFrame временного столбца 'date' типа datetime для сортировки.")
    df["date"] = df["Дата операции"].map(lambda x: datetime.strptime(str(x), "%d.%m.%Y %H:%M:%S"))
    logger.info(
        f"Отбор транзакций в диапазоне от {datetime.strftime(from_dt, '%d.%m.%y')}"
        f" до {datetime.strftime(filter_to_dt, '%d.%m.%y')}"
    )
    filtered_df = df[(df["date"] >= from_dt) & (df["date"] <= filter_to_dt)]
    return filtered_df.iloc[:, :-1]


def calculate_cashback(operations_dict: dict[str, float]) -> dict[str, Any]:
    """
    Calculates cashback for each transaction in the given dictionary.

    The function iterates over the provided dictionary of transactions, where the keys are transaction IDs
    and the values are the transaction amounts. For each transaction, it calculates the cashback as a percentage
    of the transaction amount (1% in this case) and appends it to the list of values
    associated with the transaction ID.

    Parameters:
    operations_dict (dict[str, float]): A dictionary containing transaction IDs as keys
    and transaction amounts as values.

    Returns:
    dict[str, float]: The same dictionary as the input, but with the cashback added to the list of values
    for each transaction ID.
    """
    logger.info("Перед вычислением кэшбэка по транзакциям.")
    for key, value in operations_dict.items():
        cash_back = round(value / 100, 2)
        if isinstance(value, float):
            operations_dict[key] = [value]
            operations_dict[key].append(cash_back)
        # operations_dict[key] = [value, round(value / 100, 2)]

    logger.info("В словарь транзакций добавлен кэшбэк.")
    return operations_dict


def get_total_expenses(df: pd.DataFrame) -> dict[str, float]:
    """
    Calculates total expenses for each card number in the given DataFrame.

    The function formats card numbers by removing asterisks, groups the data by card number,
    calculates the sum of transaction amounts for each group, and maps the sum to a positive value if it is negative.
    Finally, it returns a dictionary where the keys are the formatted card numbers
     and the values are the total expenses.

    Parameters:
    df (pd.DataFrame): A pandas DataFrame containing transaction data.

    Returns:
    dict[str, float]: A dictionary where the keys are the formatted card numbers
                      and the values are the total expenses.
    """
    df_copy = df.loc[::]
    logger.info("Форматирование номеров карт (удаление астерисков).")
    df_copy["Card_number_fmt"] = df_copy["Номер карты"].map(lambda x: str(x).replace("*", ""))
    logger.info("Определение общей суммы расходов по каждой карте.")
    grouped_data = df_copy.groupby("Card_number_fmt")["Сумма платежа"].sum().map(lambda x: -x if x < 0 else x)
    logger.info("Возврат словаря с общими суммами расходов по каждой карте.")
    return grouped_data.to_dict()


def say_hello(user_datetime: datetime = datetime.now()) -> str:
    """
    This function generates a greeting message based on the hour of the given datetime.

    Parameters:
    user_datetime (datetime): The datetime object representing the current time.

    Returns:
    str: A greeting message. The message can be one of the following:
        - "Доброе утро!" if the hour is between 5 and 12 (inclusive).
        - "Добрый день!" if the hour is between 12 and 18 (inclusive).
        - "Добрый вечер!" if the hour is between 18 and 22 (inclusive).
        - "Доброй ночи!" if the hour is between 22 and 5 (inclusive).
        - "Час {hour} является недопустимой величиной." if the hour is outside the valid range (0-23).
    """
    try:
        hour = user_datetime.hour

        if 5 <= hour < 12:
            hello_str = "Доброе утро!"
        elif 12 <= hour < 18:
            hello_str = "Добрый день!"
        elif 18 <= hour < 22:
            hello_str = "Добрый вечер!"
        else:
            hello_str = "Доброй ночи!"

        logger.info(f"Час {hour} является допустимой величиной.")

    except ValueError as ex:
        logger.error(ex.message)
        hello_str = "Недопустимый час."
    finally:
        return hello_str


def process_cards_info(transactions_dict: dict[str, Any]) -> list[dict]:
    """
    Processes a dictionary of transactions to extract and format card information.

    The function filters out transactions with invalid card numbers (represented by 'NaN')
    and returns a list of dictionaries, each containing the last digits of the card,
    the total amount spent, and the cashback for that card.

    Parameters:
    transactions_dict (dict[str, Any]): A dictionary where the keys are card numbers (as strings)
        and the values are lists containing the total amount spent and the cashback.

    Returns:
    list[dict]: A list of dictionaries. Each dictionary has the following keys:
        'last_digits' (str): The last digits of the card number.
        'total_spent' (float): The total amount spent by the card.
        'cashback' (float): The cashback received for the card.
    """
    logger.info("Фильтрация транзакций с корректными номерами карт.")
    cards = [key for key in transactions_dict.keys() if key != "NaN"]
    logger.info("Возврат в вызывающую функцию списка транзакций с корректными номерами карт.")
    return [
        {
            "last_digits": card,
            "total_spent": round(transactions_dict.get(card)[0], 2),
            "cashback": transactions_dict.get(card)[1],
        }
        for card in cards
    ]


def sort_by_amount(df: pd.DataFrame) -> list[dict]:
    """
    Sorts the given DataFrame by the 'Сумма операции' column in descending order.
    Negative transaction amounts are replaced with positive values.

    Parameters:
    df (pd.DataFrame): The DataFrame to be sorted. It should contain a column named 'Сумма операции'.

    Returns:
    list[dict]: A list of dictionaries representing the sorted DataFrame.
    Each dictionary corresponds to a row in the DataFrame.
    """
    df_copy = df.loc[::]
    logger.info("Создание копии исходного DataFrame, где отрицательные суммы транзакций заменены на положительные.")
    df_copy["Sum_without_sign"] = df_copy["Сумма операции"].map(lambda x: -x if x < 0 else x)
    logger.info("Сортировка транзакций по сумме платежа в порядке убывания.")
    sorted_by_expenses_desc = df_copy.sort_values(by="Sum_without_sign", ascending=False)
    logger.info("Возврат результата сортировка в порядке убывания сумм в вызывающую функцию в виде словаря.")
    return sorted_by_expenses_desc.to_dict(orient="records")


def get_top_transactions(transactions_list: list[dict], top: int = 5) -> list[dict]:
    """
    This function retrieves the top N transactions from a list of transactions based on the payment amount.

    Parameters:
    transactions_list (list[dict]): A list of dictionaries, where each dictionary represents a transaction.
        Each transaction dictionary should contain the following keys:
        'Дата платежа', 'Сумма платежа', 'Категория', 'Описание'.

    Returns:
    list[dict]: A list of dictionaries representing the top five transactions.
        Each dictionary contains the 'Дата платежа', 'Сумма платежа', 'Категория', and 'Описание' of the transaction.
        If the input list contains less than five transactions, the function will return all available transactions.
    """
    logger.info(f"В процессе создания списка Top-{top} транзакций по сумме платежа.")
    # df.nlargest(top, 'Сумма платежа')
    return [
        {
            "date": transaction.get("Дата платежа"),
            "amount": transaction.get("Сумма платежа", 0.0),
            "category": transaction.get("Категория", "Unknown"),
            "description": transaction.get("Описание", "описание отсутствует"),
        }
        for transaction in transactions_list[:top]
    ]


def get_currencies(currencies_file: str) -> list:
    try:
        logger.info(f"Попытка открытия файла с кодами валют {currencies_file}.")
        with open(currencies_file, "r", encoding="utf-8") as cf:
            try:
                logger.info(f"Попытка десериализации файла с кодами валют {currencies_file}.")
                currencies = json.load(cf)
                logger.info("Десериализация прошла успешно.")
                return [currency.get("code") for currency in currencies]

            except json.JSONDecodeError as ex:
                logger.error(ex)
                return []

    except FileNotFoundError as ex:
        logger.error(ex)
        print(f"Файл {currencies_file} с кодами валют не найден.")
        return []


def get_stocks(stocks_file: str) -> list:
    """
    This function retrieves a list of stock ticker symbols from a JSON file.

    Parameters:
    stocks_file (str): The path to the JSON file containing the list of stocks.

    Returns:
    list: A list of stock ticker symbols. If the file is not found or the data cannot be deserialized,
          an empty list is returned.
    """
    try:
        logger.info(f"Попытка открыть JSON-файл с тикерами биржевых тикеров {stocks_file}.")
        with open(stocks_file, "r", encoding="utf-8") as sf:
            try:
                logger.info("Попытка десериализации JSON-файла с тикерами биржевых активов.")
                companies = json.load(sf)
                logger.info("Десериализация файла с тикерами биржевых активов прошла успешно.")
                return [company.get("tickerSymbol") for company in companies]

            except json.JSONDecodeError as ex:
                logger.error(ex)
                return []
    except FileNotFoundError as ex:
        logger.error(ex)
        print(f"Файл {stocks_file} не найден.")
        return []


def get_data_from_user(user_currencies: str, user_stocks: str) -> None | str:
    """
    This function processes user input and stores it in a JSON file.

    Parameters:
    user_currencies (str): A string containing comma-separated currency codes.
    user_stocks (str): A string containing comma-separated stock ticker symbols.

    Returns:
    None | str: If the user input is invalid (i.e., contains codes or symbols that are not in the predefined lists),
        the function returns an error message. Otherwise, it returns None.

    """
    logger.info("Перед началом чтения кодов валют и биржевых тикеров из пользовательского JSON-файла.")
    prj_root = os.path.dirname(os.path.dirname(__file__))
    codes = get_currencies(os.path.join(prj_root, "data", "currencies.json"))
    symbols = get_stocks(os.path.join(prj_root, "data", "sandp500.json"))

    if not codes or not symbols:
        logger.warning(
            "Сбой при попытке получения из JSON-файла "
            f"{'кодов валют и биржевых тикеров'
                if not codes and not symbols else 'кодов валют ' if not codes else 'биржевых тикеров'}"
        )

    logger.info("Перед обработкой пользовательских настроек в JSON-файле.")
    user_currencies = user_currencies.upper().replace(",", " ").replace("  ", " ").split()
    user_stocks = user_stocks.upper().replace(",", " ").replace("  ", " ").split()

    logger.info("Проверка на валидность пользовательских настроек в JSON-файле.")

    if any(currency not in codes for currency in user_currencies) or any(
        stock not in symbols for stock in user_stocks
    ):
        logger.warning(
            f"{'Currencies and stocks'
                if any(currency not in codes for currency in user_currencies)
                and any(stock not in symbols for stock in user_stocks) else 'Currencies'
                if any(currency not in codes for currency in user_currencies) else 'Stocks'} are invalid"
        )
        return "Проверьте правильность введенных данных."

    logger.info("Writing user settings into file.")
    with open(os.path.join(prj_root, "user_settings.json"), "w", encoding="utf-8") as of:
        user_settings = {"user_currencies": user_currencies, "user_stocks": user_stocks}
        json.dump(user_settings, of)


def get_data_via_api_currencies(currencies: list[str]) -> tuple:
    """
    This function requests the current exchange rates of the given currencies from the external API.

    Parameters:
    currencies (list[str]): A list of currency codes.

    Returns:
    tuple: A tuple containing a boolean indicating success or failure, and either a list of exchange rates
           or an error message. If the request is successful, the boolean is True and the list contains the
           exchange rates of the given currencies, rounded to 2 decimal places. If the request fails, the
           boolean is False and the string contains the error message.

    """
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    logger.info("Инициализация получения обменных курсов валют из API ЦБ РФ.")

    try:
        response = requests.get(url)

        if response.status_code == 200:
            logger.info("Получены текущие обменные курсы валют.")
            currencies_data = response.json()["Valute"]
            currencies_rates = [currencies_data.get(currency, {}).get("Value") for currency in currencies]
            logger.info(f"Выбраны обменные курсы для пользовательских валют: {currencies}.")
            return True, list(map(lambda x: round(x, 2), currencies_rates))

        logger.warning(f"Получение обменных курсов валют завершилось ошибкой. Причина: {response.reason}")
        return False, str(response.reason)

    except requests.exceptions.RequestException as ex:
        logger.error(ex)
        return False, str(ex)


def get_data_via_api_stocks(stocks: list[str]) -> tuple:
    """
    This function requests the current prices of the given stocks from the external API.

    Parameters:
    stocks (list[str]): A list of stock ticker symbols.

    Returns:
    tuple: A tuple containing a boolean indicating the success of the operation and a list of float prices.
    If the operation is successful, the boolean is True and the list contains the current prices of the given stocks.
    If the operation fails, the boolean is False and the list contains the reason of the failure.
    """
    load_dotenv()

    url = f"{os.getenv("FMP_STOCKS_URL")}list?apikey={os.getenv("FMP_API_KEY")}"

    logger.info("Перед получением из API значений котировок биржевых активов.")
    try:
        response = requests.get(url)
        status_code = response.status_code

        if status_code == 200:
            logger.info("Получен массив данных по котировкам биржевых активов.")
            stocks_data = response.json()
            stocks_prices = [
                i.get("price", 0.0) for i in stocks_data for stock in stocks if i.get("symbol", "000") == stock
            ]
            logger.info(
                "В вызывающую функцию передаётся массив текущих котировок" f" пользовательских тикеров: {stocks}."
            )
            return True, stocks_prices

        logger.warning(f"Получение котировок биржевых активов завершилось ошибкой. Причина: {response.reason}")
        return False, str(response.reason)

    except requests.exceptions.RequestException as ex:
        logger.error(ex)
        return False, str(ex)


def get_exchange_rates(currencies: list[str]) -> list[dict]:
    logger.info("Перед получением из API обменных курсов пользовательских валют.")
    status, rates = get_data_via_api_currencies(currencies)
    if status:
        logger.info("Получены обменные курсы пользовательских валют. Возврат в виде списка словарей.")
        return [{"currency": currencies[i], "rate": rates[i]} for i in range(len(currencies))]


def get_stock_prices(stocks: list[str]) -> list[dict]:
    """
    Retrieves the current prices of the given stocks from an external API.

    Parameters:
    stocks (list[str]): A list of stock ticker symbols.

    Returns:
    list[dict]: A list of dictionaries. Each dictionary contains the stock ticker symbol and its current price.
                If the operation fails, an empty list is returned.

    Note:
    This function uses the `get_data_via_api_stocks` function to retrieve the stock prices.
    The `logger` object is used for logging purposes.
    """
    logger.info("Попытка получения котировок биржевых активов из API по списку тикеров.")
    status, prices = get_data_via_api_stocks(stocks)
    if status:
        logger.info(
            "Получены актуальные котировки биржевых активов по заданным тикерам. Возврат в виде списка словарей."
        )
        return [{"stock": stocks[i], "price": prices[i]} for i in range(len(stocks))]
    else:
        return []


if __name__ == "__main__":
    pass
