import csv
import os.path
import time
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import psycopg2
from config import config
import pandas as pd
import socket

params_ = config()
conn = psycopg2.connect(**params_)
cur = conn.cursor()


class watch:
    to_watch = input("Enter the folder path to watch: ")

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(PatternMatchingEventHandler):
    targets = logging.StreamHandler(sys.stdout), logging.FileHandler("logs.txt")
    logging.basicConfig(format="%(message)s", level=logging.INFO, handlers=targets)

    def __init__(self):
        super(Handler, self).__init__(ignore_patterns=['*/*.swp', '*/*.swpx'], ignore_directories=True)

    csv_file = '/home/uwu/Finterpvt/apps/logs_table.csv'
    if not os.path.exists(csv_file):
        with open("logs_table.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'date', 'time', 'event', 'path'])

    def on_created(self, event):
        # logging.info(f"{Fore.BLUE} {date_time} -- created : {event.src_path}")
        queries = (
            f"""
            INSERT INTO logs_table VALUES (
            nextval('serial'),
            'created',
            '{event.src_path}'
            )
            """
        )
        cur.execute(queries)
        cur.execute("SELECT id, date, time, event, path FROM logs_table ORDER BY id DESC LIMIT 1")
        rows = cur.fetchall()
        data_s = pd.DataFrame(rows, columns=['id', 'event', 'path', 'date', 'time'])
        print(data_s.to_string(index=False, header=False))
        data_s.to_csv(r'/home/uwu/Finterpvt/apps/logs_table.csv', mode='a', index=False, header=False,
                      columns=['id', 'event', 'path', 'date', 'time'])
        conn.commit()

    def on_deleted(self, event):
        # logging.info(f"{Fore.RED} {date_time} -- deleted : {event.src_path}")
        queries = (
            f"""
            INSERT INTO logs_table VALUES (
            nextval('serial'),
            'deleted',
            '{event.src_path}'
            )
            """
        )
        cur.execute(queries)
        cur.execute("SELECT id, date, time, event, path FROM logs_table ORDER BY id DESC LIMIT 1")
        rows = cur.fetchall()
        data_s = pd.DataFrame(rows, columns=['id', 'event', 'path', 'date', 'time'])
        print(data_s.to_string(index=False, header=False))
        data_s.to_csv(r'/home/uwu/Finterpvt/apps/logs_table.csv', mode='a', index=False, header=False,
                      columns=['id', 'event', 'path', 'date', 'time'])
        conn.commit()

    def on_closed(self, event):
        # logging.info(f"{Fore.LIGHTMAGENTA_EX} {date_time} -- closed : {event.src_path}")
        queries = (
            f"""
            INSERT INTO logs_table VALUES (
            nextval('serial'),
            'closed',
            '{event.src_path}'
            )
            """
        )
        cur.execute(queries)
        cur.execute("SELECT id, date, time, event, path FROM logs_table ORDER BY id DESC LIMIT 1")
        rows = cur.fetchall()
        data_s = pd.DataFrame(rows, columns=['id', 'event', 'path', 'date', 'time'])
        print(data_s.to_string(index=False, header=False))
        data_s.to_csv(r'/home/uwu/Finterpvt/apps/logs_table.csv', mode='a', index=False, header=False,
                      columns=['id', 'event', 'path', 'date', 'time'])
        conn.commit()

    def on_moved(self, event):
        # logging.info(f"{Fore.MAGENTA} {date_time} -- moved : {event.src_path} to {event.dest_path}")
        queries = (
            f"""
            INSERT INTO logs_table VALUES (
            nextval('serial'),
            'moved',
            '{event.src_path} to {event.dest_path}'
            )
            """
        )
        cur.execute(queries)
        cur.execute("SELECT id, date, time, event, path FROM logs_table ORDER BY id DESC LIMIT 1")
        rows = cur.fetchall()
        data_s = pd.DataFrame(rows, columns=['id', 'event', 'path', 'date', 'time'])
        print(data_s.to_string(index=False, header=False))
        data_s.to_csv(r'/home/uwu/Finterpvt/apps/logs_table.csv', mode='a', index=False, header=False,
                      columns=['id', 'event', 'path', 'date', 'time'])
        # data_s.to_csv(r'/home/uwu/Finter/logs_table.csv', mode='a', index=False, header=False)
        conn.commit()

    def on_modified(self, event):
        # logging.info(f"{Fore.GREEN} {date_time} -- modified : {event.src_path}")
        queries = (
            f"""
            INSERT INTO logs_table VALUES (
            nextval('serial'),
            'modified',
            '{event.src_path}'
            )
            """
        )
        cur.execute(queries)
        cur.execute("SELECT id, date, time, event, path FROM logs_table ORDER BY id DESC LIMIT 1")
        rows = cur.fetchall()
        data_s = pd.DataFrame(rows, columns=['id', 'event', 'path', 'date', 'time'])
        print(data_s.to_string(index=False, header=False))
        data_s.to_csv(r'/home/uwu/Finterpvt/apps/logs_table.csv', mode='a', index=False, header=False,
                      columns=['id', 'event', 'path', 'date', 'time'])
        conn.commit()

    if __name__ == "__main__":
        event_handler = PatternMatchingEventHandler()
        # call for functions
        event_handler.on_created = on_created
        event_handler.on_deleted = on_deleted
        event_handler.on_closed = on_closed
        event_handler.on_moved = on_closed
        event_handler.on_modified = on_modified


if __name__ == '__main__':
    w = watch()
    w.run()
