## Приложение 'Анализ банковских транзакций'

Этот проект представляет собой курсовую работу по Блоку 3 курса по Python на платформе SkyPro
ученика Олега Жадана (поток Prof 40.0).

## Инструкция по установке

SSH-ссылка для клонирования проекта с Github:

```
git@github.com:verbilki/SkyBank.git
```

Найти в корне проекта файл .env_template, скопировать его в .env и заполнить конфиденциальными данными
(например, для ключа FMP_API_KEY ввести токен подключения к API котировок биржевых
активов https://financialmodelingprep.com/api/v3/stock/).

1. Создать в PyCharm виртуальное окружение

### Для Windows

```commandline
python -m venv venv
```

### Для Linux, macOS

```bash
python3 -m venv venv
```

2. Активировать виртуальное окружение
   Следующую команду следует запускать из корня проекта:

### Для Windows

```commandline
venv\Scripts\activate
```

### Для Linux, macOS

```bash
source ./venv/bin/activate
```

3. Установить Poetry.

```bash
poetry install
```

4. Установить линтер flake8, анализатор статического кода mypy, форматтеры (black, isort)
   на основании файла конфигурации pyproject.toml.

Пример настройки flake8, black, isort и mypy в файле pyproject.toml:

```
[tool.poetry.dependencies]
   python = "^3.8"
   flake8 = "^3.8.4"
   black = "^20.8b1"
   isort = "^5.6.4"
   mypy = "^0.790"
```

5. Установить в терминале дополнительные пакеты:

Если в файле pyproject.toml отсутствуют записи о пакетах requests и python-dotenv,
то их необходимо установить из терминала:

```bash
poetry add requests
poetry add python-dotenv

pip install pandas pandas-stubs openpyxl numpy types-requests
```

6. Запуск приложения
   Для запуска приложения необходимо запустить на исполнение модуль src/main.py, состоящий из единственной функции
   main().

Приложение предоставляет три функциональности:

### 1. Главная страница

Сервис генерации базовых статистических данных в формате JSON по заданной дате, содержащий:
* приветствие,
* актуальные обменные курсы валют по заданному списку
* текущие котировки биржевых активов на американских биржах,
* также данные по каждой карте (включая номер карты, общую сумму расходов и кешбэк),
* топ-5 транзакций по абсолютной сумме платежа.

Валюты и акции для отображения на Главной странице задаются пользователем в файле user_settings.json в корне проекта.
Данные для анализа берутся за период с начала месяца по текущую дату.

Пример JSON-ответа:

```commandline
{
  "greeting": "Добрый день",
  "cards": [
    {
      "last_digits": "5814",
      "total_spent": 1262.00,
      "cashback": 12.62
    },
    {
      "last_digits": "7512",
      "total_spent": 7.94,
      "cashback": 0.08
    }
  ],
  "top_transactions": [
    {
      "date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    },
    {
      "date": "20.12.2021",
      "amount": 829.00,
      "category": "Супермаркеты",
      "description": "Лента"
    },
    {
      "date": "20.12.2021",
      "amount": 421.00,
      "category": "Различные товары",
      "description": "Ozon.ru"
    },
    {
      "date": "16.12.2021",
      "amount": -14216.42,
      "category": "ЖКХ",
      "description": "ЖКУ Квартира"
    },
    {
      "date": "16.12.2021",
      "amount": 453.00,
      "category": "Бонусы",
      "description": "Кешбэк за обычные покупки"
    }
  ],
  "currency_rates": [
    {
      "currency": "USD",
      "rate": 73.21
    },
    {
      "currency": "EUR",
      "rate": 87.08
    }
  ],
  "stock_prices": [
    {
      "stock": "AAPL",
      "price": 150.12
    },
    {
      "stock": "AMZN",
      "price": 3173.18
    },
    {
      "stock": "GOOGL",
      "price": 2742.39
    },
    {
      "stock": "MSFT",
      "price": 296.71
    },
    {
      "stock": "TSLA",
      "price": 1007.08
    }
  ]
}
```

### 2. Доходы по инвесткопилке

Сервис рассчитывает сумму, которую можно было бы отложить на Инвесткопилку в заданном месяце.
При первом запуске пользователь устанавливает комфортный порог округления трат: *10*, *50* или *100* рублей.

***Например***

*При настройке шага округления в 50 ₽, покупка на 1712 ₽ автоматически округлится до 1750 ₽, и 38 ₽ попадут
в Инвесткопилку.*

Формат JSON-результата:

```commandline
{"month": "2024-08", "investment_amount": 204.5}
```

По умолчанию для анализа берется текущий месяц.

### 3. Траты по заданной категории

Для формирования отчета берётся интервал в три месяца от заданной даты.
Выгрузка отчёта по расходным операциям возможна в трёх форматах *.json, .xlxs* и *.csv* (по умолчанию - *.json*).
Отчеты сохраняются в папке *data/*
с названием формата *rspending_by_cat_<Выбранная категория трат>.<выбранное расширение>*.

Для выхода из приложения необходимо в главном меню приложения выбрать опцию *4. Выход*.

## 7. Настройка и использование фреймворка unit-тестирования Pytest

Исходный код модулей покрыт юнит-тестами Pytest на более, чем 80%. Для запуска выполните команды:

```bash
poetry add --group dev pytest # установка pytest в виртуальное окружение приложения
pytest # запуск тестов
```

Команда для формирования HTML-отчёта в терминале:

```bash
pytest --cov=src --cov-report=html
```

В результате зтого запуска будет сформирован HTML-отчет (файл htmlcov/index.html) о покрытии тестами.

## Лицензия

[GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.html#license-text)