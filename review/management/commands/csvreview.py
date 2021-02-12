import csv
import os
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import review.csv to DB table review_review'

    def handle(self, *args, **options):
        base_dir = os.getcwd()
        csv_file = os.path.join(base_dir, 'data/review.csv')

        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()

        with open(csv_file, 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [
                (i['id'], i['title_id'], i['text'], i['author'],
                 i['score'], i['pub_date'])
                for i in dr
            ]

        cur.executemany(
            '''INSERT INTO review_review (id, title_id, text, author_id, score,
            pub_date)
            VALUES (?, ?, ?, ?, ?, ?);''',
            to_db
        )
        conn.commit()
        conn.close()
