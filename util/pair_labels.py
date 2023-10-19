import os
import psycopg2

class PairLabel:
    def __init__(self):
        self.db_url = os.environ["DATABASE_URL"]
        self.conn = psycopg2.connect(self.db_url, sslmode="require")

    def add_label(self, image_one_name, image_two_name, label, labeler):
        add_label_query = """INSERT INTO public.pair_labels (img_pair, label, labeler, req_ts) VALUES (%s, %s, %s, CURRENT_TIMESTAMP(5))"""
        cursor = self.conn.cursor(name="kartik_cursor")
        cursor.execute(add_label_query, (image_one_name + "," + image_two_name, label, labeler))
        self.conn.commit()
        cursor.close()

    def close_connection(self):
        if self.conn.closed != 0:
            self.conn.close()
                       
        
