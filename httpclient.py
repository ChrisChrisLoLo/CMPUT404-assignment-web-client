#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    # def get_host_port(self,url):

    def connect(self, host, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f'Connecting to {(host,port)}')
            self.socket.connect((host, port))
        except Exception as e:
            if self.socket:
                self.socket.close()
            raise e
        return None

    def get_code(self, data):
        print("Parsed Code: "+data.split('\r\n')[0].split(' ')[1])
        return int(data.split('\r\n')[0].split(' ')[1])

    def get_headers(self,data):
        # return data.split('\r\n')[0].split(' ')[1]
        return

    def get_body(self, data):
        # TODO: add check if \r\n is in html
        print("Parsed Body: "+data.split('\r\n')[-1])
        return data.split('\r\n')[-1]
    
    def sendall(self, data):
        print(f'sending {data}')
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(4096)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        print(buffer)
        return buffer.decode('utf-8', 'backslashreplace')

    def GET(self, url_string, args=None):
        # if 'http://' not in url_string:
        #     url_string = 'http://' + url_string
        # url_string='http://127.0.0.1'

        url = urllib.parse.urlparse(url_string)
        print(url)
        print(f'SOCKET:::: {socket.gethostbyname(url.hostname)}')
        
        # hostAndPort = ip_addr+f':{url.port}' if url.port else ip_addr

        port = url.port if url.port else 80
        self.connect(socket.gethostbyname(url.hostname), port)
        try:
            # host = url.netloc+f':{url.port}' if url.port else url.hostname
            path = url.path if url.path else '/'
            self.sendall(f'GET {path} HTTP/1.0\r\nHost: {url.netloc}\r\n\r\n')
            data = self.recvall(self.socket)

            # print(data)
            code = self.get_code(data)
            body = self.get_code(data)
            return HTTPResponse(code, body)
        except Exception as e:
            print(e)
        finally:
            self.close()

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
