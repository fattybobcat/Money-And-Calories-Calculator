import datetime as dt


class Record:
    def __init__(self,
                 amount: int,
                 comment: str,
                 date: dt.datetime.date = dt.datetime.now().date()):
        self.amount = amount
        self.comment = comment
        if type(date) == str:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = date


class Calculator:
    def __init__(self, limit: int):
        self.limit = limit
        self.records = []

    def add_record(self,record):
        self.records.append(record)

    def get_today_stats(self):
        """Calculates the amount value for today"""
        today_stat = 0
        for rec in self.records:
            if rec.date == dt.datetime.today().date():
                today_stat += rec.amount
        return today_stat

    def get_week_stats(self):
        """Calculates the amount value for the last 7 days"""
        week_stat = 0
        seven_days = dt.datetime.now().date() - dt.timedelta(7)
        for rec in self.records:
            if dt.datetime.now().date() >= rec.date >= seven_days:
                week_stat += rec.amount
        return week_stat


class CashCalculator(Calculator):
    USD_RATE = float(50)
    EURO_RATE = float(80)

    def __init__(self, limit: int):
        super().__init__(limit)

    def get_today_cash_remained(self, currency: str):

        money = self.limit - self.get_today_stats()
        if money > 0:
            if currency == 'usd':
                usd_rest = money / self.USD_RATE
                return 'На сегодня осталось {:.2f} USD'.format(usd_rest)
            elif currency == 'eur':
                eur_rest = money / self.EURO_RATE
                return 'На сегодня осталось {:.2f} Euro'.format(eur_rest)
            elif currency == 'rub':
                return 'На сегодня осталось {:.2f} руб'.format(money)
        elif money == 0:
            return 'Денег нет, держись'
        else:
            if currency == 'usd':
                usd_rest = money / self.USD_RATE
                return 'Денег нет, держись: твой долг - {:.2f} USD'.format(abs(usd_rest))
            elif currency == 'eur':
                eur_rest = money / self.EURO_RATE
                return 'Денег нет, держись: твой долг - {:.2f} Euro'.format(abs(eur_rest))
            elif currency == 'rub':
                return 'Денег нет, держись: твой долг - {:.2f} руб'.format(abs(money))


class CaloriesCalculator (Calculator):
    def get_calories_remained(self):
        calories = self.limit - self.get_today_stats()
        if calories > 0:
            return 'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {} кКал'.format(calories)
        else:
            return 'Хватит есть!'
