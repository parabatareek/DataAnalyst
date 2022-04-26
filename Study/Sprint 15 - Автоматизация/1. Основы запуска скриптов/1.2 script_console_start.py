# 2.
# Напишите скрипт urbanization.py, получающий на вход переменную regions — строку с названиями стран через запятую.
# Внутри скрипта прочитайте переменную urbanization из файла data/urbanization.csv.
# Отфильтруйте только страны, указанные во входном параметре, и определите для них максимальный уровень урбанизации за всю историю наблюдений.
# Формат входного параметра:
# Unix-имя: r
# GNU-имя: regions
# Ваш скрипт вызывается так:
# python urbanization.py --regions='Germany,France,Russia'

# Подсказка:
# Проверьте переменные unixOptions и gnuOptions.
# В блоке обработки параметров конвертируйте строки с именами стран в массив методом split(',').

#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt

import pandas as pd

if __name__ == "__main__":

    # Задаём определения входных параметров
    unixOptions = "r:" # напишите код
    gnuOptions = ["regions="] # напишите код

    # Читаем входные параметры
    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]
    try:
        arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    # Обрабатываем входные параметры
    regions = 'Germany,France,Russia'.split(',')
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-r","--regions"): # ваш код здесь
            regions = currentValue.split(',') # ваш код здесь

    urbanization = pd.read_csv('/datasets/urbanization.csv')

    # Фильтруем и определяем максимальный уровень урбанизации
    urbanization = urbanization.query('Entity in @regions')
    urbanization = urbanization.groupby('Entity').agg({'Urban': 'max'}) # ваш код

    print(urbanization)