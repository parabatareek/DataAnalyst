# !/usr/bin/python
# -*- coding: utf-8 -*-

import dash
from dash import dcc
from dash import html

# задаём лейаут
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    children=[
        # формируем html
        html.H1(children='Первый простой дашборд!'),
    ]
)

# описываем логику дашборда

if __name__ == '__main__':
    app.run_server(debug=True)