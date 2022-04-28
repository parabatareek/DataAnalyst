# 4.
#     1. Чтобы записать данные в агрегированные таблицы нужно, чтобы колонки датафреймов и таблиц совпадали.
# В вызовах методов agg_games_year_genre_platform.rename() и agg_games_name.rename() переименуйте колонки так,
# чтобы они совпадали со столбцами соответствующих таблиц;
#     2. В словаре tables укажите датафреймы, соответствующие именам таблиц;
#     3. В цикле обновления агрегированных таблиц укажите нужные имя таблицы (для команд DELETE и to_sql) и имя датафрейма для команды to_sql.
#
# Подсказка
# Ещё раз изучите определения таблиц agg_games_year_genre_platform и agg_games_year_score:
# сравните названия их столбцов со столбцами соответствующих им датафреймов (agg_games_year_genre_platform и agg_games_year_score).
# Проверьте аргументы запроса на удаление данных — из каких таблиц ведётся удаление?
# Проверьте аргументы запросов на запись данных — в какие таблицы из каких датафреймов ведётся запись?

#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import getopt
from datetime import datetime

import pandas as pd

from sqlalchemy import create_engine

if __name__ == '__main__':

    # задаём входные параметры
    unixOptions = 'sdt:edt:'
    gnuOptions = ['start_dt=', 'end_dt=']

    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]  # excluding script name

    try:
        arguments, values = getopt.getopt(
            argumentList, unixOptions, gnuOptions
        )
    except getopt.error as err:
        # output error, and return with an error code
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
                WHERE year_of_release::TIMESTAMP BETWEEN '{}'::TIMESTAMP AND '{}'::TIMESTAMP
            '''.format(
        start_dt, end_dt
    )

    data_raw = pd.io.sql.read_sql(query, con=engine, index_col='game_id')

    columns_str = ['name', 'platform', 'genre', 'rating']
    columns_numeric = [
        'na_players',
        'eu_players',
        'jp_players',
        'other_players',
        'critic_score',
        'user_score',
    ]
    columns_datetime = ['year_of_release']

    for column in columns_str:
        data_raw[column] = data_raw[column].astype(str)
    for column in columns_numeric:
        data_raw[column] = pd.to_numeric(data_raw[column], errors='coerce')
    for column in columns_datetime:
        data_raw[column] = pd.to_datetime(data_raw[column])
    data_raw['total_copies_sold'] = data_raw[
        ['na_players', 'eu_players', 'jp_players', 'other_players']
    ].sum(axis=1)

    agg_games_year_genre_platform = data_raw.groupby(
        ['year_of_release', 'genre', 'platform']
    ).agg({'name': 'count', 'total_copies_sold': 'sum'})
    agg_games_year_score = data_raw.groupby(
        ['year_of_release', 'genre', 'platform']
    ).agg({'critic_score': 'mean', 'user_score': 'mean'})

    agg_games_year_genre_platform = agg_games_year_genre_platform.rename(
        columns={'name':'games'}
    )  # напишите код
    agg_games_year_score = agg_games_year_score.rename(
        columns={'critic_score': 'avg_critic_score', 'user_score': 'avg_user_score'}
    )  # напишите код

    agg_games_year_genre_platform = agg_games_year_genre_platform.fillna(0).reset_index()
    agg_games_year_score = agg_games_year_score.fillna(0).reset_index()

    tables = {
        'agg_games_year_genre_platform': agg_games_year_genre_platform,  # ваш код
        'agg_games_year_score': agg_games_year_score,
    }  # ваш код

    for table_name, table_data in tables.items():

        query = '''
                  DELETE FROM {} WHERE year_of_release BETWEEN '{}'::TIMESTAMP AND '{}'::TIMESTAMP
                '''.format(
            table_name, start_dt, end_dt
        )  # напишите код
        engine.execute(query)

        table_data.to_sql(
            name=table_name, con=engine, if_exists='append', index=False
        )  # напишите код

    print('All done.')

