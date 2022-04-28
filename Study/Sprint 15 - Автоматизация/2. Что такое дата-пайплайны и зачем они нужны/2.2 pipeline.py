# 2.
# Добавьте скрипту входные параметры start_dt и end_dt так:
# unixOptions = "sdt:edt:"
# gnuOptions = ["start_dt=", "end_dt="]
# Прочитайте из базы данных все записи, у которых year_of_release больше или равен start_dt и меньше или равен end_dt.
# Выведите на экран уникальные значения поля 'year_of_release' датафрейма data_raw.

# Подсказка
# Выведите уникальные данные методом unique().

#!/usr/bin/python
import sys

import getopt
from datetime import datetime

import pandas as pd

from sqlalchemy import create_engine

if __name__ == '__main__':

    # укажите входные параметры в строках
    unixOptions = "sdt:edt:"  # ваш код
    gnuOptions = ["start_dt=", "end_dt="]  # ваш код

    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]

    try:
        arguments, values = getopt.getopt(
            argumentList, unixOptions, gnuOptions
        )
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    start_dt = '1981-01-01'
    end_dt = '1998-01-01'
    for currentArgument, currentValue in arguments:
        if currentArgument in ('-sdt', '--start_dt'):
            start_dt = currentValue
        elif currentArgument in ('-edt', '--end_dt'):
            end_dt = currentValue

    db_config = {
        'user': 'my_user',
        'pwd': 'my_user_password',
        'host': 'localhost',
        'port': 5432,
        'db': 'games',
    }
    connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(
        db_config['user'],
        db_config['pwd'],
        db_config['host'],
        db_config['port'],
        db_config['db'],
    )

    engine = create_engine(connection_string)

    query = ''' SELECT *
                FROM data_raw
                WHERE year_of_release::TIMESTAMP BETWEEN '{0}'::TIMESTAMP AND '{1}'::TIMESTAMP
            '''.format(
        start_dt, end_dt
    )  # напишите код

    data_raw = pd.io.sql.read_sql(query, con=engine, index_col='game_id')
    print(data_raw['year_of_release'].unique())  # ваш код