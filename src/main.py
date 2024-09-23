import os
from datetime import date, datetime

import pandas as pd

from src.reports import spending_by_category, write_to_file
from src.services import get_transactions_list, investment_bank
from src.utils import read_excel2dataframe  # get_data_from_user
from src.views import generate_json_response

prj_root = os.path.dirname(os.path.dirname(__file__))


def get_user_date() -> date:
    current_date = datetime.today()
    user_input = input(
        "Введите дату в формате DD.MM.YY или нажмите Enter для выбора текущей даты"
        f" ({current_date.strftime('%d.%m.%y')}): "
    )

    if user_input.strip() == "":
        return current_date

    else:
        try:
            user_date = datetime.strptime(user_input, "%d.%m.%y")
            return user_date
        except ValueError:
            print("Ваш ввод не соответствует требуемому формату даты DD.MM.YY.")
            return get_user_date()


def expenditures_and_reporting(transactions_df: pd.DataFrame, report_dt: datetime) -> None:
    """
    Prints a menu for selecting the report format and category of expenditures,
    generates a report by calling `spending_by_category` and writes it to a file
    using `write_to_file`.

    Parameters
    ----------
    transactions_df : pd.DataFrame
        A Pandas DataFrame containing transactions
    report_dt : datetime
        The maximum date for transactions to be included in the report

    Returns: None
    """
    report_extensions_dict = {"1": "xlsx", "2": "csv", "3": "json"}
    print(
        "\nВыберите цифру формата отчета или нажмите Enter для выгрузки в JSON:\n" "1. xlsx\n" "2. csv\n" "3. json\n"
    )

    report_extensions_choice = ""
    while report_extensions_choice not in report_extensions_dict.keys():
        report_extensions_choice = input("Ваш выбор (1, 2, 3 (default)): ")

        if report_extensions_choice.strip() == "":
            report_extensions_choice = "3"

    print("\nВыберите категорию трат:\n")
    category = ""
    while category not in transactions_df["Категория"].unique():
        print("Доступные категории:\n" f"{transactions_df["Категория"].unique()}")

        category = input("\nВведите наименование категории из списка выше: ").strip().title()
        print(f"\nВы выбрали категорию: {category}.\n")

    report_name = (
        f"spending_by_cat_{category.replace(' ', '_')}" f".{report_extensions_dict[report_extensions_choice]}"
    )
    write_to_file(report_name, "w")(spending_by_category)(transactions_df, category, report_dt)


def main():
    print("Добро пожаловать в приложение анализа банковских операций 'SkyBank' !\n")

    while True:
        print(
            "Введите цифру пункта меню:\n"
            "1. Главная страница\n"
            "2. Доходы по инвесткопилке\n"
            "3. Траты по заданной категории\n"
            "4. Выход\n"
        )

        menu_choice = input("Ваш выбор (1, 2, 3, 4): ")

        if menu_choice == "4":
            print("До свидания.")
            break

        else:
            work_dt = datetime.combine(get_user_date(), datetime.max.time())
            data_path = os.path.join(prj_root, "data")
            df: pd.DataFrame = read_excel2dataframe(os.path.join(data_path, "operations.xlsx"))

            if menu_choice == "1":
                print(generate_json_response(work_dt, df))

            elif menu_choice == "2":
                rounding_limits_dict = {"1": 10, "2": 50, "3": 100}
                print(
                    "\nВыберите цифру лимита округления (в рублях) (Enter - лимит 100 руб.):\n"
                    "1. 10\n"
                    "2. 50\n"
                    "3. 100\n"
                )

                rounding_limit_choice = ""
                while rounding_limit_choice not in rounding_limits_dict.keys():
                    rounding_limit_choice = input("Ваш выбор (1, 2, 3 (default)): ")

                    if rounding_limit_choice.strip() == "":
                        rounding_limit_choice = "3"

                # if not os.path.exists("user_settings.json"):
                #     result["limit"] = limit
                #
                #     with open("user_settings.json", "w", encoding="utf-8") as settings_file:
                #         json.dump(result, settings_file)
                #
                # limit = result.get("limit")

                transactions_list = get_transactions_list(df)
                print(investment_bank(work_dt, transactions_list, rounding_limits_dict[rounding_limit_choice]))

            elif menu_choice == "3":
                expenditures_and_reporting(df, work_dt)

            else:
                print("Недопустимая опция.")
                continue


if __name__ == "__main__":
    main()
