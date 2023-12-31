import os
import sys
import json
import time
import json
import random

from util.pair import PairHelper
from urllib.parse import urlparse
from util.pair_labels import PairLabel
from http.server import BaseHTTPRequestHandler, HTTPServer

hostname = "localhost"
port = os.environ['PORT']
#port = 8080

class StaticServer(BaseHTTPRequestHandler):
    def __init__(self, *args):
        self.not_found_file = "404.html"
        self.oncomplete_file = "complete.html"
        self.index_file = "index.html"
        self.assets_path = "assets"
        self.imgs_path = "imgs"
        self.js_path = "js"
        self.main_js_name = "main.js"
        self.imgs_list = os.listdir(os.path.join(self.assets_path, self.imgs_path))
        self.img_1_placeholder = "img1PlaceHolder.jpg"
        self.img_2_placeholder = "img2PlaceHolder.jpg"
        self.pair_id_placeholder = "pairIdPlaceHolder"
        self.cookie_str = "Cookie"
        self.student_id_str = "Student-Id"
        self.label_str = "label"
        self.pair_id_str = "pairId"
        self.image_one_name_str = "imageOneName"
        self.image_two_name_str = "imageTwoName"
        self.versions_file = "versions.txt"
        self.version_cookie_file = "version_cookie_map.json"
        self.users_file = "users.txt"
        self.shift = 3
        self.init_kartik_cookie_map()
        self.init_mime_type_map()
        self.load_versions_list()
        self.load_users_list()
        BaseHTTPRequestHandler.__init__(self, *args)

    def load_list(self, list_file):
        with open(list_file) as f:
            d = f.read().splitlines()
        return d

    def init_kartik_cookie_map(self):
        with open(self.version_cookie_file) as f:
            d = json.loads(f.read())
        self.version_cookie_map = d
        
    def load_versions_list(self):
        self.versions_list = self.load_list(self.versions_file)

    def load_users_list(self):
        self.users_list = self.load_list(self.users_file)
    
    def init_mime_type_map(self):
        self.mime_type_map = {}
        self.mime_type_map[".apk"] = "application/vnd.android.package-archive"
        self.mime_type_map[".json"] = "application/json"
        self.mime_type_map[".jpg"] = "image/jpeg"
        self.mime_type_map[".jpeg"] = "image/jpeg"
        self.mime_type_map[".png"] = "image/png"
        self.mime_type_map[".html"] = "text/html"
        self.mime_type_map[".css"] = "text/css"
        self.mime_type_map[".js"] = "text/javascript"

    def substitution_cipher(self, student_id):
        result = ""
        for char in student_id:
            if not char.isdigit():
                break
            pos = int(char)

            shifted = (pos + self.shift) % 10

            result += str(shifted)

        return result
    
    def send_content_headers(self, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        
    def read_file(self, file_path, binary=False):
        with open(file_path, "rb" if binary else "r") as f:
            content = f.read()
        return content
    
    def fetch_image_content(self, path):
        if path.endswith(".jpg") or path.endswith(".jpeg") or path.endswith(".png"):
            image_file = os.path.join(self.assets_path, path[1:])
            
            if os.path.exists(image_file):
                _, image_extension = os.path.splitext(image_file)
                self.send_content_headers(self.mime_type_map[image_extension])
                return self.read_file(image_file, binary=True)
            
    def fetch_static_content(self, path, version, user, request_count):
        print("fetch static content")
        print(request_count)
        
        if version in self.versions_list and user in self.users_list:
            resource_file = os.path.join(self.assets_path, path[1:])
            _, resource_extension = os.path.splitext(resource_file)
        
            if os.path.exists(resource_file) and os.path.isfile(resource_file):
                if path.endswith(".html"):
                    pair_helper = PairHelper(version)
                    fetch_results = pair_helper.fetch_pair(request_count)
                    pair_helper.close_connection()

                    html_content = self.read_file(os.path.join(self.assets_path, self.oncomplete_file))
                    if fetch_results:
                        img_1_b64, img_2_b64, pair_id = fetch_results[0], fetch_results[1], fetch_results[2]
                    
                        html_content = self.read_file(resource_file)
                        html_content = html_content.replace(self.img_1_placeholder,
                                                            img_1_b64)
                        html_content = html_content.replace(self.img_2_placeholder,
                                                            img_2_b64)
                        html_content = html_content.replace(self.pair_id_placeholder,
                                                            pair_id)

                    self.send_content_headers(self.mime_type_map[resource_extension])
                    return html_content
                
                self.send_content_headers(self.mime_type_map[resource_extension])
                return self.read_file(resource_file)
                
            elif "main.js" in path:
                # Hacky again
                js_content = self.read_file(os.path.join(self.assets_path, self.js_path, self.main_js_name))
                self.send_content_headers(self.mime_type_map[".js"])
                return js_content

                self.send_content_headers(self.mime_type_map[resource_extension])
                return self.read_file(resource_file)

            elif os.path.basename(path) == "home":
                pair_helper = PairHelper(version)
                fetch_results = pair_helper.fetch_pair(request_count)
                pair_helper.close_connection()
                
                html_content = self.read_file(os.path.join(self.assets_path, self.oncomplete_file))
                if fetch_results:
                    img_1_b64, img_2_b64, pair_id = fetch_results[0], fetch_results[1], fetch_results[2]
                
                    html_content = self.read_file(os.path.join(self.assets_path, self.index_file))
                    html_content = html_content.replace(self.img_1_placeholder,
                                                        img_1_b64)
                    html_content = html_content.replace(self.img_2_placeholder,
                                                        img_2_b64)
                    html_content = html_content.replace(self.pair_id_placeholder,
                                                        pair_id)

                self.send_content_headers(self.mime_type_map[".html"])
                return html_content
        self.send_content_headers(self.mime_type_map[".html"])
        return self.read_file(os.path.join(self.assets_path, self.not_found_file))

    def extract_post_data(self, post_data):
        label = None
        pair_id = None

        print("post data")
        print(post_data)
        post_data_pairs = post_data.split("&")

        print("post data pairs")
        print(post_data_pairs)
        
        for data_pair in post_data_pairs:
            param_val = data_pair.split("=")

            print(param_val[0])
            print(param_val[1])
            if param_val[0] == self.label_str:
                label = param_val[1]

            elif param_val[0] == self.pair_id_str:
                pair_id = param_val[1]

        return label, pair_id

    def get_count_from_cookie(self, req_headers, target_cookie_name):
        print("target cookie name")
        print(target_cookie_name)
        header_list = req_headers.split("\n")

        for h in header_list:
            h_pair = h.split(": ")

            if h_pair[0] == self.cookie_str:
                cookie_key_vals = h_pair[1]
                cookie_key_val_list = cookie_key_vals.split("; ")

                for c_k in cookie_key_val_list:
                    cookie_name = c_k.split("=")[0]
                    cookie_val = c_k.split("=")[1]
                    
                    if cookie_name == target_cookie_name:
                        return cookie_val                
        return "1"
    
    def extract_student_id(self, req_headers):
        header_list = req_headers.split("\n")

        for h in header_list:
            h_pair = h.split(": ")

            if h_pair[0] == self.student_id_str:
                return h_pair[1]
        
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length).decode("utf-8"));
        base_path = '/'.join(self.path.split('/')[:-2])

        print("path")
        print(self.path)
        
        request_user = self.path.split('/')[-1]
        request_version = self.path.split('/')[-2]

        cookie_name = self.version_cookie_map[request_version] if request_version in self.version_cookie_map else ""
        print("cookie name")
        print(cookie_name)
        
        request_counter = self.get_count_from_cookie(str(self.headers), cookie_name)

        print("post data")
        print(post_data)
        print("request counter")
        print(request_counter)
        print("request user")
        print(request_user)
        print("request version")
        print(request_version)

        #label, pair_id = self.extract_post_data(post_data)
        label = post_data["label"]
        pair_id = post_data["pairId"]
        pair_label_helper = PairLabel()

        print(label)
        print(pair_id)
        print(request_user)
        if label and pair_id and request_user:
            print("all 3 present")
            pair_label_helper.add_label(label, pair_id, request_user)
        else:
            print("something missing")
        pair_label_helper.close_connection()
        
        pair_helper = PairHelper(request_version)
        fetch_results = pair_helper.fetch_pair(request_counter)
        pair_helper.close_connection()
        
        if fetch_results:
            img_1_b64, img_2_b64, pair_id = fetch_results[0], fetch_results[1], fetch_results[2]
            response_dict = {}
            response_dict['complete'] = False
            response_dict['img_1_b64'] = img_1_b64
            response_dict['img_2_b64'] = img_2_b64
            response_dict['pair_id'] = pair_id
            json_response = json.dumps(response_dict)
            self.send_content_headers(self.mime_type_map[".json"])
            self.wfile.write(json_response.encode(encoding='utf_8'))
        else:
            response_dict = {}
            response_dict['complete'] = True
            json_response = json.dumps(response_dict)
            self.send_content_headers(self.mime_type_map[".json"])
            self.wfile.write(json_response.encode(encoding='utf_8'))
            
        #content = self.fetch_static_content(base_path, request_version, request_user, request_counter)
        #self.wfile.write(bytes(content, encoding="utf8"))
            
    def do_GET(self):
        if self.path == "/ecs152a_ass1":
            student_id = self.extract_student_id(str(self.headers))
            
            if student_id:
                encrypted_id = self.substitution_cipher(student_id)
                if encrypted_id:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.send_header("ecs152a-resp", encrypted_id)
                    self.end_headers()
                    self.wfile.write("You should look at the response headers".encode())
                else:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.send_header("ecs152a-resp", "Invalid ID")
                    self.end_headers()
                    self.wfile.write("You should look at the response headers".encode())
            else:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.send_header("ecs152a-resp", "Expected student-id header missing")
                self.end_headers()
                self.wfile.write("You should look at the response headers".encode())
        else:
            if self.path == "/main.js":
                # hacky
                self.path = "/home/js/main.js/hzoK4PdUsc/SO7m1jbMJI"
            
            request_user = self.path.split('/')[-1]
            request_version = self.path.split('/')[-2]
            base_path = '/'.join(self.path.split('/')[:-2])
            cookie_name = self.version_cookie_map[request_version] if request_version in self.version_cookie_map else ""
            request_counter = self.get_count_from_cookie(str(self.headers), cookie_name)
            
            content = self.fetch_static_content(base_path, request_version, request_user, request_counter)
            self.wfile.write(bytes(content, encoding="utf8"))
                
if __name__ == "__main__":
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    
    server = HTTPServer(("", int(port)), StaticServer)
    print("Server running on port " + str(port))

    server.serve_forever()
