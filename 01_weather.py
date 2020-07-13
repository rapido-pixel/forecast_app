# -*- coding: utf-8 -*-

import click
from forecast_engine import *
import database_updater
from image_maker import *
import csv
from datetime import date, timedelta

IMPORTED_FORECASTS_FILE = "./import_f.csv"


def import_from_db():
    from_date = input("Введите начальную дату в формате 'гггг-мм-дд': ")
    to_date = input("Введите конечную дату в формате 'гггг-мм-дд': ")
    databaseupdater = database_updater.DatabaseUpdater(from_date=from_date, to_date=to_date)
    databaseupdater.import_forecasts()


def show_forecasts():
    with open(IMPORTED_FORECASTS_FILE, 'r', newline='') as csv_file:
        csv_data = csv.DictReader(csv_file)
        forecasts_for_draw = list(csv_data)
        for forecast in forecasts_for_draw:
            print(f"""
            Прогноз погоды на {forecast['дата']}
            ---------------------------------
            Температура: {forecast['температура']}
            Погода: {forecast['погода']}
            """)


def get_info_to_last_week():
    today = str(date.today())
    last_days = str(date.today() - timedelta(days=60))
    weather_maker = WeatherMaker(URL, MONTHS_NUMBERS, last_days, today)
    databaseupdater = database_updater.DatabaseUpdater(days_forecasts=weather_maker.days_forecasts)
    weather_maker.run()
    databaseupdater.create_table()
    databaseupdater.export_forecasts()
    databaseupdater.show_lastweek_forecasts()


def export_to_db():
    from_date = input("Введите начальную дату в формате 'гггг-мм-дд': ")
    days_count = input("Введите конечную дату в формате 'гггг-мм-дд': ")
    weather_maker = WeatherMaker(URL, MONTHS_NUMBERS, from_date, days_count)
    databaseupdater = database_updater.DatabaseUpdater(days_forecasts=weather_maker.days_forecasts)
    weather_maker.run()
    databaseupdater.export_forecasts()


@click.command()
@click.option("-draw", is_flag=True, help="draw images")
@click.option('-import_', is_flag=True, help="import data from database")
@click.option("-show", is_flag=True, help="show forecasts")
@click.option("-export", is_flag=True, help="export data to database")
def get_info(import_, draw, show, export):
    get_info_to_last_week()
    if import_:
        import_from_db()
    if draw:
        image_maker = ImageMaker(IMAGE, CLOUD, RAIN, SNOW, SUN, IMG_PATH)
        image_maker.run()
    if show:
        try:
            show_forecasts()
        except FileNotFoundError:
            print("Нет прогнозов для показа")
            print("Пожалуйста, выберите период дат для формирования прогнозо погоды")
            import_from_db()
            show_forecasts()
    if export:
        export_to_db()


get_info()
