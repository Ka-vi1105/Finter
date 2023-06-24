from watcherrr import *
from data_base import *


if __name__ == '__main__':
    w = watch()
    w.run()
    database_events()
    insert_logs_table()
    w = watch()
    w.run()
    insert_logs_table()
