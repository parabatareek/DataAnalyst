# Добавьте элементы управления и графики.
# Укажите следующие идентификаторы:
# Диалог выбора режима отображения графиков — mode_selector;
# График выпуска игр по годам и жанрам — launches_by_year;
# График выпуска игр по годам и платформам — launches_by_platform;
# График продаж игр по годам и жанрам — sales_by_year;
# График средних оценок — score_scatter;
#
# Подсказка:
# Пройдитесь по тексту программы и последовательно проставьте у элементов дашборда вот такие id:
# dcc.RadioItems — id = 'mode_selector'
# Первый dcc.Graph — id = 'launches_by_year'
# Второй dcc.Graph — id = 'launches_by_platform'
# Третий dcc.Graph — id = 'sales_by_year'
# Четвёртый dcc.Graph — id = 'score_scatter'
# dcc.DatePickerRange — id = 'dt_selector'
# Первый cc.Dropdown — id = 'genre_selector'
# Второй dcc.Dropdown — id = 'platform_selector'

# !/usr/bin/python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from datetime import datetime

import pandas as pd

# задаём данные для отрисовки
from sqlalchemy import create_engine

# пример подключения к базе данных для Postresql
# db_config = {'user': 'my_user',
#             'pwd': 'my_user_password',
#             'host': 'localhost',
#             'port': 5432,
#             'db': 'games'}
# engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(db_config['user'],
#                                                            db_config['pwd'],
#                                                            db_config['host'],
#                                                            db_config['port'],
#                                                            db_config['db']))
# пример подключения к базе данных для Sqlite
engine = create_engine('sqlite:////db/games.db', echo=False)

# получаем сырые данные
query = '''
            SELECT * FROM agg_games_year_genre_platform
        '''
agg_games_year_genre_platform = pd.io.sql.read_sql(query, con=engine)
agg_games_year_genre_platform['year_of_release'] = pd.to_datetime(agg_games_year_genre_platform['year_of_release'])

query = '''
            SELECT * FROM agg_games_year_score
        '''
agg_games_year_score = pd.io.sql.read_sql(query, con=engine)
agg_games_year_score['year_of_release'] = pd.to_datetime(agg_games_year_score['year_of_release'])
# игнорируем записи без оценок
agg_games_year_score = agg_games_year_score.query('avg_user_score > 0 and avg_critic_score > 0')

note = '''
          Этот дашборд показывает историю игрового рынка (исключая мобильные устройства).
          Используйте выбор интервала даты выпуска, жанра и платформы для управления дашбордом.
          Используйте селектор выбора режима отображения для того, чтобы показать абсолютные
          или относительные значения выпуска и продаж игр по годам.
       '''

# задаём лейаут
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, compress=False)
app.layout = html.Div(children=[

    # формируем html
    html.H1(children='История игрового рынка'),

    html.Br(),

    html.Div([
        html.Div([

            # график выпуска игр по годам и жанрам
            html.Label('Выпуск игр по жанрам:'),

            dcc.RadioItems(
                options=[
                    {'label': 'Абсолютные значения', 'value': 'absolute_values'},
                    {'label': '% от общего выпуска', 'value': 'relative_values'},
                ],
                value='absolute_values',
                id='mode_selector'  # напишите код
            ),

            dcc.Graph(
                id='launches_by_year'  # напишите код
            ),
        ], className='eight columns'),

        html.Div([
            # график выпуска игр по платформам
            html.Label('Выпуск игр по платформам:'),
            dcc.Graph(
                id='launches_by_platform'  # напишите код
            ),
        ], className='four columns'),

    ], className='row'),

    html.Div([
        html.Div([

            # график продаж игр по жанрам
            html.Label('Продажи игр по жанрам:'),

            dcc.Graph(
                id='sales_by_year'  # напишите код
            ),
        ], className='eight columns'),

        html.Div([
            # график средних оценок по жанрам
            html.Label('Средние оценки по жанрам:'),

            dcc.Graph(
                id='score_scatter'  # напишите код
            ),
        ], className='four columns'),

    ], className='row'),

    # пояснения
    html.Label(note),

    html.Br(),

    html.Div([

        html.Div([
            # выбор временного периода
            html.Label('Года выпуска:'),
            dcc.DatePickerRange(
                start_date=agg_games_year_genre_platform['year_of_release'].dt.date.min(),
                end_date=datetime(2016, 1, 1).strftime('%Y-%m-%d'),
                display_format='YYYY-MM-DD',
                id='dt_selector'  # напишите код
            ),
        ], className='two columns'),

        html.Div([
            # выбор жанра
            html.Label('Жанры:'),
            dcc.Dropdown(
                options=[{'label': x, 'value': x} for x in agg_games_year_genre_platform['genre'].unique()],
                value=agg_games_year_genre_platform['genre'].unique().tolist(),
                multi=True,
                id='genre_selector'  # напишите код
            ),
        ], className='four columns'),

        html.Div([
            # выбор платформы
            html.Label('Платформы:'),
            dcc.Dropdown(
                options=[{'label': x, 'value': x} for x in agg_games_year_genre_platform['platform'].unique()],
                value=agg_games_year_genre_platform['platform'].unique().tolist(),
                multi=True,
                id='platform_selector'  # напишите код
            ),
        ], className='six columns'),

    ], className='row'),

])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=3000)