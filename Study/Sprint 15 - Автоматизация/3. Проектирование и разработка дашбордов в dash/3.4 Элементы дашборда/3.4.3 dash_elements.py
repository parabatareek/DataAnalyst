# Отобразите на дашборде график launches_by_year и его заголовок.
# Вот его код:
# # график выпуска игр по годам и жанрам
# html.Label('Выпуск игр по жанрам:'),
# dcc.Graph(
#     style = {'height': '50vw'},
#     id = 'launches_by_year'
# ),
# «Оберните» график и его заголовок в два элемента div.
# Первый div служит для отображения ряда элементов дашборда и имеет имя класса 'row'.
# Второй div вложен в него и служит для отображения колонки дашборда.
# Он-то и должен иметь ширину в двенадцать (twelve) колонок (т. е. занимать всю ширину дашборда).
#
# Подсказка:
# Напишите код:
# html.Div([
#     html.Div([
#         # график выпуска игр по годам и жанрам
#         html.Label('Выпуск игр по жанрам:'),
#         dcc.Graph(
#             style = {'height': '50vw'},
#             id = 'launches_by_year'
#         ),
#     ], className = 'twelve columns'),
# ], className = 'row'),

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
agg_games_year_genre_platform["year_of_release"] = pd.to_datetime(agg_games_year_genre_platform["year_of_release"])

note = '''
          Этот дашборд поможет вам выучить правила композиции дашбордов.
       '''

# задаём лейаут
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, compress=False)
app.layout = html.Div(children=[

    # формируем html
    html.H1(children='История игрового рынка'),

    html.Br(),

    # пояснения
    html.Label(note),

    html.Br(),

    # выбор временного периода
    html.Label('Года выпуска:'),
    dcc.DatePickerRange(
        start_date=agg_games_year_genre_platform['year_of_release'].dt.date.min(),
        end_date=datetime(2016, 1, 1).strftime('%Y-%m-%d'),
        display_format='YYYY-MM-DD',
        id='dt_selector',
    ),

    html.Div([
        html.Div([
            html.Label('Выпуск игр по жанрам:'),
            dcc.Graph(
                style={'height': '50vw'},
                id='launches_by_year'
            )], className='twelve columns')
    ], className='row'),
    # напишите код

])


# описываем логику дашборда
@app.callback(
    [Output('launches_by_year', 'figure'),
     ],
    [Input('dt_selector', 'start_date'),
     Input('dt_selector', 'end_date'),
     ])
def update_figures(start_date, end_date):
    # для простоты игнорируем фильтрацию

    games_by_genre = (agg_games_year_genre_platform.groupby(['year_of_release', 'genre'])
                      .agg({'games': 'sum'})
                      .reset_index()
                      )
    y_label = 'Выпущенные игры'

    # график выпуска по жанрам
    data_by_genre = []
    for genre in games_by_genre['genre'].unique():
        data_by_genre += [go.Scatter(x=games_by_genre.query('genre == @genre')['year_of_release'],
                                     y=games_by_genre.query('genre == @genre')['games'],
                                     mode='lines',
                                     stackgroup='one',
                                     name=genre)]

    # формируем результат для отображения
    return (
        {
            'data': data_by_genre,
            'layout': go.Layout(xaxis={'title': 'Год'},
                                yaxis={'title': y_label})
        },
    )


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=3000)