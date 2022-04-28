# 3.
# Приведите столбцы датафрейма data_raw к нужным типам.
# Заполните переменные columns_str, columns_numeric и columns_datetime именами нужных колонок.
# Год выхода игры должен иметь тип datetime, все колонки продаж и оценок — числовые, а остальные — строковые;
# Дополните определение переменной data_raw['total_copies_sold'] так,
# чтобы в ней хранилась сумма продаж по всем регионам для каждой игры;
# Примените метод groupby() к датафрейму data_raw чтобы получить датафреймы agg_games_year_genre_platform и agg_games_year_score так,
# чтобы данные соответствовали агрегационным таблицам agg_games_year_genre_platform и agg_games_year_score с такой структурой:
# CREATE TABLE agg_games_year_genre_platform(record_id serial PRIMARY KEY,
#                                            year_of_release TIMESTAMP,
#                                            genre VARCHAR(128),
#                                            platform VARCHAR(128),
#                                            games INT,
#                                            total_copies_sold INT);
#
# CREATE TABLE agg_games_year_score(record_id serial PRIMARY KEY,
#                                   year_of_release TIMESTAMP,
#                                   genre VARCHAR(128),
#                                   platform VARCHAR(128),
#                                   avg_critic_score REAL,
#                                   avg_user_score REAL);
# Названия столбцов пока не меняйте.
#
# Подсказка:
# Вот порядок столбцов в переменных:
# columns_str: 'name', 'platform', 'genre', 'rating';
# columns_numeric: 'na_players', 'eu_players', 'jp_players', 'other_players', 'critic_score', 'user_score';
# total_copies_sold: 'na_players', 'eu_players', 'jp_players', 'other_players';
# agg_games_year_genre_platform: 'year_of_release', 'genre', 'platform'.

# !/usr/bin/python
import sys

import getopt
from datetime import datetime

import pandas as pd

from sqlalchemy import create_engine

if __name__ == "__main__":

    unixOptions = "sdt:edt:"
    gnuOptions = ["start_dt=", "end_dt="]

    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]

    try:
        arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    start_dt = '1981-01-01'
    end_dt = '1998-01-01'
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-sdt", "--start_dt"):
            start_dt = currentValue
        elif currentArgument in ("-edt", "--end_dt"):
            end_dt = currentValue

    db_config = {'user': 'my_user',
                 'pwd': 'my_user_password',
                 'host': 'localhost',
                 'port': 5432,
                 'db': 'games'}
    connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_config['user'],
                                                             db_config['pwd'],
                                                             db_config['host'],
                                                             db_config['port'],
                                                             db_config['db'])

    engine = create_engine(connection_string)

    query = ''' SELECT *
                FROM data_raw
                WHERE year_of_release::TIMESTAMP BETWEEN '{}'::TIMESTAMP AND '{}'::TIMESTAMP
            '''.format(start_dt, end_dt)

    data_raw = pd.io.sql.read_sql(query, con=engine, index_col='game_id')

    columns_str = ['name', 'platform', 'genre', 'rating']  # напишите код
    columns_numeric = ['na_players', 'eu_players', 'jp_players', 'other_players', 'critic_score', 'user_score']  # напишите код
    columns_datetime = ['year_of_release']  # напишите код

    for column in columns_str: data_raw[column] = data_raw[column].astype(str)
    for column in columns_numeric: data_raw[column] = pd.to_numeric(data_raw[column], errors='coerce')
    for column in columns_datetime: data_raw[column] = pd.to_datetime(data_raw[column])

    data_raw['total_copies_sold'] = data_raw[['na_players', 'eu_players', 'jp_players', 'other_players']].sum(axis=1)  # ваш код

    agg_games_year_genre_platform = data_raw.groupby(['year_of_release', 'genre', 'platform']).agg(
        {'name': 'count', 'total_copies_sold': 'sum'})  # ваш код
    agg_games_year_score = data_raw.groupby(['year_of_release', 'genre', 'platform']).agg({'critic_score': 'mean', 'user_score': 'mean'})  # ваш код

    print(data_raw.info())
    print(agg_games_year_genre_platform.head(5))
    print(agg_games_year_score.head(5))

    print(data_raw.info())