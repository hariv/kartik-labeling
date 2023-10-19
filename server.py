import os
import sys
import json
import time
import json
import random

from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

hostname = "localhost"
port = os.environ['PORT']
#port = 8080

class StaticServer(BaseHTTPRequestHandler):
    def __init__(self, *args):
        self.not_found_file = "404.html"
        self.index_file = "index.html"
        self.assets_path = "assets"
        self.imgs_path = "imgs"
        self.imgs_list = os.listdir(os.path.join(self.assets_path, self.imgs_path))
        self.img_1_placeholder = "img_1.jpg"
        self.img_2_placeholder = "img_2.jpg"
        self.init_mime_type_map()
        BaseHTTPRequestHandler.__init__(self, *args)

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
    
    def send_content_headers(self, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        
    def read_file(self, file_path, binary=False):
        with open(file_path, 'rb' if binary else 'r') as f:
            content = f.read()
        return content
    
    def fetch_image_content(self, path):
        if path.endswith(".jpg") or path.endswith(".jpeg") or path.endswith(".png"):
            image_file = os.path.join(self.assets_path, path[1:])
            
            if os.path.exists(image_file):
                _, image_extension = os.path.splitext(image_file)
                self.send_content_headers(self.mime_type_map[image_extension])
                return self.read_file(image_file, binary=True)
            
    def fetch_static_content(self, path):
        resource_file = os.path.join(self.assets_path, path[1:])
        _, resource_extension = os.path.splitext(resource_file)
        
        if os.path.exists(resource_file) and os.path.isfile(resource_file):
            if path.endswith(".html"):
                self.send_content_headers(self.mime_type_map[resource_extension])
                html_content = self.read_file(resource_file)
                html_content = html_content.replace(self.img_1_placeholder,
                                                    random.choice(self.imgs_list))
                html_content = html_content.replace(self.img_2_placeholder,
                                                    random.choice(self.imgs_list))
                return html_content

            self.send_content_headers(self.mime_type_map[resource_extension])
            return self.read_file(resource_file)

        if os.path.basename(path) == "home":
            html_content = self.read_file(os.path.join(self.assets_path, self.index_file))
            html_content = html_content.replace(self.img_1_placeholder,
                                                random.choice(self.imgs_list))
            html_content = html_content.replace(self.img_2_placeholder,
                                                random.choice(self.imgs_list))
            
            self.send_content_headers(self.mime_type_map[".html"])
            return html_content
            
        self.send_content_headers(self.mime_type_map[".html"])
        return self.read_file(os.path.join(self.assets_path, self.not_found_file))

    def do_GET(self):
        content = self.fetch_image_content(self.path)
        
        if content:
            self.wfile.write(content)
        else:
            content = self.fetch_static_content(self.path)
            self.wfile.write(bytes(content, encoding='utf8'))
            
if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    
    server = HTTPServer(('', int(port)), StaticServer)
    print("Server running on port " + str(port))

    server.serve_forever()
