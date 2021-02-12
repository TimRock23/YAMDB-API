import csv
import os
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import category.csv to DB table api_category'

    def handle(self, *args, **options):
        base_dir = os.getcwd()
        csv_file = os.path.join(base_dir, 'data/category.csv')

        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()

        with open(csv_file, 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [
                (i['id'], i['name'], i['slug'])
                for i in dr
            ]

        cur.executemany(
            '''INSERT INTO api_category (id, name, slug)
            VALUES (?, ?, ?);''',
            to_db
        )
        conn.commit()
        conn.close()
