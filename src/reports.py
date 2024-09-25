import io
import json
import logging
import os
from datetime import datetime
from functools import wraps
from typing import Callable, Optional

import pandas as pd

log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "reports.log")

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path, mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def write_to_file(file_name: str = "", mode: str = "w") -> Callable[[Callable], Callable]:
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

    def my_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> None:
            result: str = func(*args, **kwargs)
            if result == "[]" or result is None:
                return
            try:
                report_full_path = os.path.join(data_path, file_name)
                _, file_extension = os.path.splitext(file_name)

                if file_extension == ".json":
                    with open(report_full_path, mode, encoding="utf-8") as output_file:
                        json.dump(json.loads(result), output_file, ensure_ascii=False, indent=4)

                elif file_extension == ".csv":
                    pd.read_json(io.StringIO(result)).to_csv(report_full_path, index=False)

                else:
                    pd.read_json(io.StringIO(result)).to_excel(report_full_path, index=False)

            except Exception as e:
                logger.error(f"Произошёл сбой при записи в файл: {e}")
            else:
                print(f"Отчет по тратам сформирован в файле data/{file_name}.")
                logger.info(f"Отчет по тратам сформирован в файле data/{file_name}.")

        return wrapper

    return my_decorator


def spending_by_category(transactions: pd.DataFrame, category: str, report_max_dt: Optional[datetime] = None) -> str:
    if report_max_dt is None:
        date_to = transactions["Дата операции"].max()
    else:
        date_to = report_max_dt

    logger.info(f"Определена верхняя граница {date_to.strftime('%d.%m.%y')} диапазона расчётного периода.")
    date_from = (date_to - pd.DateOffset(months=3)).replace(hour=0, minute=0, second=0, microsecond=0)
    logger.info(f"Определена нижняя граница {date_from.strftime('%d.%m.%y')} диапазона расчётного периода.")

    transactions["Дата"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    filtered_df = transactions[(transactions["Дата"] >= date_from) & (transactions["Дата"] <= date_to)]
    logger.info("Фильтрация по заданной категории и преобразование результата из DataFrame в словарь.")
    filtered_by_category: dict = (
        filtered_df[filtered_df["Категория"] == category].iloc[:, :-1].to_dict(orient="records")
    )

    try:
        if not len(filtered_by_category):
            print("В выбранной категории нет трат за последние 3 месяца.")
            return "[]"
        else:
            logger.info("Сериализация конечного словаря в JSON.")
            return json.dumps(filtered_by_category, ensure_ascii=False, indent=4)

    except Exception as ex:
        logger.error(ex)
