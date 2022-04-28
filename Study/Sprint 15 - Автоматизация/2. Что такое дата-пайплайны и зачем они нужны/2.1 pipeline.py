# 1.
# Присоединитесь к базе данных games и через библиотеку sqlalchemy прочитайте данные из таблицы data_raw.
# Результат сохраните в переменной data_raw.
# Установите в датафрейме data_raw столбец 'game_id' в качестве индекса.
# Выведите на экран описание типов данных методом info().
# Выведите 5 первых строк датафрейма data_raw. Вот параметры для присоединения к БД:
# Имя пользователя: 'my_user';
# Пароль: 'my_user_password';
# Адрес сервера: 'localhost';
# Порт: 5432;
# База данных: 'games';
#
# Подсказка:
# Присоединитесь к базе данных, как это показано в теории урока.
# Для запроса к БД вызовите команду ''' SELECT * FROM '''.
# Установите индексы так: index_col = 'game_id'.

# !/usr/bin/python
import pandas as pd
from sqlalchemy import create_engine

db_config = {
                'user': 'my_user',  # ваш код
                'pwd': 'my_user_password',  # ваш код
                'host': 'localhost',  # ваш код
                'port': 5432,  # ваш код
                'db': 'games',  # ваш код
}
connection_string = f'postgresql://{db_config["user"]}:{db_config["pwd"]}@{db_config["host"]}:{db_config["port"]}/{db_config["db"]}'  # напишите код

engine = create_engine(connection_string)  # напишите код

query = ''' SELECT * FROM data_raw '''  # напишите код

data_raw = pd.io.sql.read_sql(query, con=engine, index_col='game_id')  # ваш код

print(data_raw.info)  # ваш код
print(data_raw.head())  # ваш код