#!/usr/bin/python
# -*- coding: utf-8 -*-

# 1.
# В файле /datasets/urbanization.csv данные об исторической динамике урбанизации — росте доли городского населения — с разбивкой по странам и географическим регионам. 
# Структура файла:
# Entity — название страны или региона;
# Year — год наблюдений;
# Urban — % городского населения.
# Напишите скрипт, который запускается из командной строки, читает данные урбанизации в датафрейм urbanization и выводит на экран 5 первых строк датафрейма urbanization.

# Подсказка
# В условии укажите определение блока исполняемого кода. 
# Проверьте, что включили поддержку кодировки для русскоязычных комментариев и указали, на каком языке написан скрипт.

import pandas as pd
import sys
import getopt

if __name__ == '__main__':
    unix_options = "p:"
    gnu_options = ["path="]

    cmd_args = sys.argv[1:]

    try: 
        arguments, values = getopt.getopt(args=cmd_args,
                                          shortopts=unix_options,
                                          longopts=gnu_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    path = ''

    for current_argumet, current_value in arguments:
        if current_argumet in ("-p", "--path"):
            path = current_value

    urbanization = pd.read_csv(filepath_or_buffer=path)
    print(urbanization.head(5))