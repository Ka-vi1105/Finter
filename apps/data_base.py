import psycopg2
from config import config
# import datetime

params_ = config()
conn = psycopg2.connect(**params_)
cur = conn.cursor()

# now = datetime.datetime.now()
# now_date = now.strftime("%d-%m-%Y")
# now_time = now.strftime("%H:%M:%S")


class database_events:
    #  Check if connection set up
    @staticmethod
    def connect():
        print('Connected to Database')

        cur.execute('Select version()')
        db_version = cur.fetchone()
        print(db_version)

        conn.commit()

    # create logs table
    @staticmethod
    def create_logs_table():
        queries = (
            """
            CREATE TABLE IF NOT EXISTS logs_table (
                    id      int PRIMARY key,
                    Event   varchar (255) NOT NULL,
                    Path    varchar(255) NOT NULL,
                    date    DATE DEFAULT CURRENT_DATE,
                    time    TIME DEFAULT CURRENT_TIME
        )
        """
        )
        cur.execute(queries)
        conn.commit()

    connect()
    create_logs_table()


class insert_logs_table:

    # creating a sequence named serial for id
    @staticmethod
    def sequence_table():
        sequence = '''CREATE SEQUENCE IF NOT EXISTS serial start 1;'''
        cur.execute(sequence)
        conn.commit()

    sequence_table()

    if KeyboardInterrupt:
        cur.close()


if __name__ == '__main__':
    database_events()
    insert_logs_table()
