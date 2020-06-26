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
    RUB_RATE = 1
    exchange_rate = {'usd':['USD_RATE', 'USD'] ,'eur':['EURO_RATE', 'Euro'],'rub':['RUB_RATE', 'руб']}
    def __init__(self, limit: int):
        super().__init__(limit)

    def get_today_cash_remained(self, currency: str):
        money = self.limit - self.get_today_stats()
        rate_value, word_course = self.exchange_rate[currency]
        rate_course=float(eval('self.'+rate_value))
        exchanged_money = money / rate_course
        if money > 0:
            return 'На сегодня осталось {:.2f} {}'.format(exchanged_money,word_course)
        elif money == 0:
            return 'Денег нет, держись'
        else:
            return 'Денег нет, держись: твой долг - {:.2f} {}'.format(abs(exchanged_money),word_course)
       
class CaloriesCalculator (Calculator):
    def get_calories_remained(self):
        calories = self.limit - self.get_today_stats()
        if calories > 0:
            return 'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {} кКал'.format(calories)
        else:
            return 'Хватит есть!'