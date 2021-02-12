import csv
import os
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import comments.csv to DB table review_comment'

    def handle(self, *args, **options):
        base_dir = os.getcwd()
        csv_file = os.path.join(base_dir, 'data/comments.csv')

        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()

        with open(csv_file, 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [
                (i['id'], i['review_id'], i['text'], i['author'],
                 i['pub_date'])
                for i in dr
            ]

        cur.executemany(
            '''INSERT INTO review_comment (id, review_id, text, author_id,
            pub_date)
            VALUES (?, ?, ?, ?, ?);''',
            to_db
        )
        conn.commit()
        conn.close()
