# Лучше испортировать from datetime import datetime as dt т.к. не используются другие модули из datetime
import datetime as dt
# Неиспользуемый импорт
import json

# Общее замечание - оформить код в соответствии с pep8.
# autopep8 https://pypi.org/project/autopep8/ или ручками https://pep8.org/
# Так же добавить docstring к функциям и классам
class Record:
    def __init__(self, amount, comment, date=''):
        self.amount=amount
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment=comment
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records=[]
    def add_record(self, record):
        self.records.append(record)
    def get_today_stats(self):
        today_stats=0
        # Название переменной Record в lowercase (pep8 + конфликт с именем класса)
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats+Record.amount
        return today_stats
    def get_week_stats(self):
        week_stats=0
        today = dt.datetime.now().date()
        for record in self.records:
            # Лучше использовать метод isocalendar для определения текущей недели и недели в record
            if (today -  record.date).days <7 and (today -  record.date).days >=0:
                week_stats +=record.amount
        return week_stats
class CaloriesCalculator(Calculator):
    # Перенести комментаий в docstring
    def get_calories_remained(self): # Получает остаток калорий на сегодня
        # Использовать осмысленные названия переменны (calories, ...)
        x=self.limit-self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        else:
            return 'Хватит есть!'
class CashCalculator(Calculator):
    USD_RATE=float(60) #Курс доллар США.
    EURO_RATE=float(70) #Курс Евро.
    def get_today_cash_remained(self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type=currency
        cash_remained = self.limit - self.get_today_stats()
        if currency=='usd':
            cash_remained /= USD_RATE
            # Не заменять переданное значение курса.
            # Либо выделить отдельную переменную для стокового отображение валюты, либо форматировать переданную
            # переменную (к примеру upper()). Так же можно использовать маппинг {"usd": "USD", "rub": "RUB", ...}
            currency_type ='USD'
        elif currency_type=='eur':
            cash_remained /= EURO_RATE
            currency_type ='Euro'
        elif currency_type=='rub':
            # Бесполезная строка
            cash_remained == 1.00
            currency_type ='руб'
        if cash_remained > 0:
            # Не использовать динамические операции в fstring
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Использовать либо fstring, либо форматированные строки, сохранять консистентность по всей программе
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)
    # Лишний метод, родительский метод будет предоставлять по-умолчанию
    def get_week_stats(self):
        super().get_week_stats()
