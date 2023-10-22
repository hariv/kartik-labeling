import os
import json
import psycopg2

class PairHelper():
    def init_table_version_map(self):
        with open(self.table_version_map_file) as f:
            self.table_version_map = json.loads(f.read())
        
    def __init__(self, url_version):
        self.table_version_map_file = "table_version_map.json"
        self.db_url = os.environ["DATABASE_URL"]
        self.conn = psycopg2.connect(self.db_url, sslmode="require")
        self.init_table_version_map()
        self.table_name = self.table_version_map[url_version]

    def fetch_pair(self, request_count):
        fetch_pair_query = f"SELECT {self.table_name}.img1_64, {self.table_name}.img2_64, {self.table_name}.pair_id FROM public.{self.table_name} WHERE id = %s"
        cursor = self.conn.cursor()
        cursor.execute(fetch_pair_query, (request_count))
        result = cursor.fetchone()
        return result

    def close_connection(self):
        if self.conn.closed != 0:
            self.conn.close()
                       
        
