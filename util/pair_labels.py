import os
import psycopg2

class PairLabel:
    def __init__(self):
        self.db_url = os.environ["DATABASE_URL"]
        self.conn = psycopg2.connect(self.db_url, sslmode="require")

    def add_label(self, label, pair_id, labeler):
        add_label_query = """INSERT INTO public.labels (pair_id, score, user_string, req_ts) VALUES (%s, %s, %s, CURRENT_TIMESTAMP(5))"""
        cursor = self.conn.cursor()
        cursor.execute(add_label_query, (pair_id, label, labeler))
        self.conn.commit()
        cursor.close()

    def close_connection(self):
        if self.conn.closed != 0:
            self.conn.close()
                       
        
