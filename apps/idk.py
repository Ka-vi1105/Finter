import psycopg2
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris


# data = 'hii'


# def iterate_lmao(self, id, events, path, time):
#     connection = psycopg2.connect(
#         host='localhost',
#         database='learn_db',
#         user='postgres',
#         password='atavisrunakos@69'
#     )
#
#     pointer = connection.cursor()
#     pointer.execute("select * from logs_table")
#     rows = pointer.fetchall()
# globals()['data'] = pd.DataFrame(rows)
# pd.DataFrame(rows)

#     return f'{id} / {events} / {path} / {time}'
#
#
# iter_funct = np.vectorize(iterate_lmao)
# iter_funct(data)

# visualize it using pandas
# data = pd.DataFrame(rows)
# print(data.head())
# try:
#     while True:
#         print(data.head())
# except KeyboardInterrupt:
#     pass

def idklmao():
    connection = psycopg2.connect(
        host='localhost',
        database='learn_db',
        user='postgres',
        password='atavisrunakos@69'
    )

    pointer = connection.cursor()
    pointer.execute("select * from logs_table")
    table = pointer.fetchall()
    data = pd.DataFrame(table)
    print(data)

    try:
        pointer.execute("SELECT id, time, event, path FROM logs_table ORDER BY id DESC LIMIT 1")
        rows = pointer.fetchall()
        data_s = pd.DataFrame(rows)
        print(data_s)
    except KeyboardInterrupt:
        print("Pressed ctrl+c")
    # # visualize it using pandas
    # data = pd.DataFrame(table)
    # # print("icic")
    # # data.head(4)
    # print(data)


idklmao()
