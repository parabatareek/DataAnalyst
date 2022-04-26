# 3.
# Добавьте к скрипту ещё два параметра:
# start_dt — дата начала анализа. Unix-имя: s, GNU-имя: start_dt;
# end_dt — дата завершения анализа. Unix-имя: e, GNU-имя: end_dt.
# Добавьте к фильтрации условие на выбор наблюдений между start_dt и end_dt.
# Отсортируйте датафрейм urbanization по возрастанию полей 'Entity' и 'Year'.
# Ваш скрипт будет вызван так:
# python urbanization.py --regions='Germany,France,Russia' --start_dt='1998-01-01 00:00:00' --end_dt='1999-12-31 23:59:59'

# Подсказка:
# Приведите значения параметров и колонку 'Year' к типу datetime.
# Для входных параметров примените формат '%Y-%m-%d %H:%M:%S', для колонки 'Year' — формат '%Y-%m-%d'.
# Обратите внимание на разделители имён параметров в переменных unixOptions и gnuOptions.

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
from datetime import datetime

import pandas as pd

if __name__ == "__main__":

    # Задаём определения входных параметров
    unixOptions = "r:s:e:" # напишите код
    gnuOptions = ["regions=", "start_dt=", "end_dt="] # напишите код

    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]
    try:
        arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    # Обрабатываем входные параметры
    regions = 'Germany,France,Russia'.split(',')
    start_dt = '1998-01-01 00:00:00'
    end_dt = '1999-12-31 23:59:59'
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-r", "--regions"):
            regions = currentValue.split(',')
        elif currentArgument in ("-s", "--start_dt"):
            start_dt = datetime.strptime(start_dt, '%Y-%m-%d %H:%M:%S') # напишите код
        elif currentArgument in ("-e", "--end_dt"):
            end_dt = datetime.strptime(currentValue, '%Y-%m-%d %H:%M:%S') # напишите код

    urbanization = pd.read_csv('/datasets/urbanization.csv')[['Entity', 'Year', 'Urban']]

    # Приводим колонки urbanization к нужным типам
    urbanization['Year'] = pd.to_datetime(urbanization['Year'], format='%Y-%m-%d') # ваш код

    # Фильтруем и определяем максимальный уровень урбанизации
    urbanization = urbanization.query('Entity in @regions and Year >= @start_dt and Year <= @end_dt') # напишите код

    print(urbanization.sort_values(by = ['Entity', 'Year'])) # ваш код