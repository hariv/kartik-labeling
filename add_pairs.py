import os
import sys
import json
import base64
import psycopg2

IMAGES_BASE_PATH = os.path.join('assets', 'imgs')
CONFIG_JSON = "config_sample.json"

def read_json(json_name):
    with open(json_name) as f:
        d = json.loads(f.read())
    return d

def read_image(img_name):
    with open(os.path.join(IMAGES_BASE_PATH, img_name), 'rb') as f:
        img_binary = f.read()
    return img_binary

def get_base64(img_name):
    img_data = read_image(img_name)
    img_b64 = base64.b64encode(img_data)
    return "data:image/jpeg;base64," + img_b64.decode()

def init_database():
    conf = read_json(CONFIG_JSON)
    conn = psycopg2.connect(host=conf['host'], port=conf['port'],
                            database=conf['database'], user=conf['user'],
                            password=conf['password'])
    return conn

def run_insert_query(conn, img1_b64, img2_b64, pair_id, data_version):
    insert_pair_query = f"INSERT INTO public.{data_version} (pair_id, img1_b64, img2_b64) VALUES (%s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(insert_pair_query, (pair_id, img1_b64, img2_b64))
    conn.commit()
    cursor.close()
                   
def add_pair(img1_name, img2_name, pair_id, data_version):
    conn = init_database()
    img1_b64 = get_base64(img1_name)
    img2_b64 = get_base64(img2_name)
    
    run_insert_query(conn, img1_b64, img2_b64, pair_id, data_version)
    conn.close()
    
if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('Usage: python3 add_labels.py <img_1_name> <img_2_name> <pair_id> <data_version>')
        exit()
    add_pair(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
