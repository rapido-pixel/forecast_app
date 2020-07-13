import csv
from peewee import *
from datetime import timedelta
import datetime
import locale

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

db = PostgresqlDatabase(database="forecast", user="postgres", password="1", host="localhost")


class WeatherForecasts(Model):
    date = TextField()
    temperature = TextField()
    weather = TextField()

    class Meta:
        database = db


class DatabaseUpdater:

    def __init__(self, days_forecasts=None, from_date=None, to_date=None):
        self.result = []
        self.days_forecasts = days_forecasts
        self.from_date = from_date
        self.to_date = to_date

    def create_table(self):
        db.connect()
        WeatherForecasts.create_table()

    def export_forecasts(self):
        for day in self.days_forecasts:
            exists = WeatherForecasts.select().where(WeatherForecasts.date == day['date'])

            if exists:
                WeatherForecasts.update(temperature=day["temperature"], weather=day["weather"]).where(
                    WeatherForecasts.date == day['date']).execute()
            else:
                WeatherForecasts.create(date=day["date"], temperature=day["temperature"], weather=day["weather"])

    def import_forecasts(self):
        dates_range = WeatherForecasts.select().where(WeatherForecasts.date.between(self.from_date, self.to_date))
        for date in dates_range:
            self.result.append({"дата": datetime.datetime.strptime(date.date, "%Y-%m-%d %H:%M:%S").strftime("%d %B %Y"),
                                "температура": date.temperature,
                                "погода": date.weather})
        self.write()

    def write(self):
        keys = self.result[0].keys()
        with open("./import_f.csv", "w", newline="") as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.result)

    def show_lastweek_forecasts(self):
        last_days = str(datetime.date.today() - timedelta(days=7))
        dates_range = WeatherForecasts.select().where(WeatherForecasts.date.between(last_days, datetime.date.today()))
        print("Погода за прошедшие 7 дней")
        print("-" * 30)
        for date in dates_range:
            print(f"Дата: {datetime.datetime.strptime(date.date, '%Y-%m-%d %H:%M:%S').strftime('%d %B %Y')}")
            print(f"Температура: {date.temperature}")
            print(f"Погода: {date.weather}")
            print("*" * 30)
