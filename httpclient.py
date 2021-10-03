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
    def get_remote_ip(self, host):
        print(f'Getting IP for {host}')
        try:
            remote_ip = socket.gethostbyname(host)
        except socket.gaierror:
            print ('Hostname could not be resolved. Exiting')
            sys.exit()
        print (f'Ip address of {host} is {remote_ip}')
        return remote_ip

    def get_host_port(self,url):
        information = url.split(':')
        try:
            host = information[0]
            port = information[1]
        except:
            host = self.get_remote_ip(url)
            port = 80

        return host, port
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        information = data.split("\r\n")
        first_line = information[0]
        first_line = first_line.split()
        code = first_line[1]
        return int(code)

    def get_headers(self,data):
        information = data.split("\r\n\r\n")
        header = information[0]
        return header

    def get_body(self, data):
        information = data.split("\r\n\r\n")
        if(len(information)  > 1):
            body = information[1]
        else:
            return None
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            print(part.decode('utf-8'))
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        parsed_url = urllib.parse.urlparse(url)
        print(url)
        print(parsed_url)
        print("gooooood!!!!!!!!!!")
        try:
            host = parsed_url.netloc
        except:
            print("No host was detected")
            sys.exit()
        try:
            if(parsed_url.path != ''):
                path = parsed_url.path
            else:
                path = '/'
        except:
            path = "/"
        #print("more more gooooood!!!!!!!!!!")
        first_line = "GET %s HTTP/1.1\r\n"%(path)
        user_agent = "User-Agent: Senyu_Li/happyagent1.0\r\n"
        target_host = "Host: %s\r\n"%(host)
        accept = "Accept: */*\r\n"
        request = first_line + user_agent + target_host + accept + '\r\n' 
        h,p = self.get_host_port(host)
        #print("fuck!!!!!!!!!!")
        try:
            p = int(p)
        except:
            print('port number should be an interger')
            sys.exit()
        #print(h)
        #print(p)
        #print("fuck  you you!!!!!!!!!!")
        self.connect(h,p)
        #print("fuck  you!!!!!!!!!!")
        #print(request)
        self.sendall(request)
        #print("nice!!!!!!!!!")
        self.socket.shutdown(socket.SHUT_WR)
        response = self.recvall(self.socket)
        #print("boy")
        code = self.get_code(response)
        if(code == 200):
            body = self.get_body(response)
        else:
            body = None
        print("girl")
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path
        first_line = "POST %s HTTP/1.1\r\n"%(path)
        user_agent = "User-Agent: Senyu_Li/happyagent1.0\r\n"
        target_host = "Host: %s\r\n"%(host)
        accept = "Accept: */*\r\n"
        content_type = "Content-Type: application/x-www-form-urlencoded\r\n"
        if args:
            content_length = "Content-Length: %d\r\n"%(len(args))
            arg_transformed = ""
            for index, argument in args.items():
                #print(index)
                #print(argument)
                #print("herehere")
                arg_transformed = arg_transformed + "%s=%s&"%(str(index), str(argument.replace(' ', '+')))
            arg_transformed = arg_transformed[:-1]
            print(arg_transformed[0])
            arg_transformed + "\r\n"       
            content_length = "Content-Length: %d\r\n"%(len(arg_transformed))
            request =  first_line + user_agent + target_host + accept + content_length + content_type + '\r\n' + arg_transformed 
        else:
            content_length = "Content-Length: 0 \r\n"
            request =  first_line + user_agent + target_host + accept + content_length + content_type + '\r\n' 
        
        h,p = self.get_host_port(host)
        try:
            p = int(p)
        except:
            print('port number should be an interger')
            sys.exit()
        #print(h)
        #print(p)
        self.connect(h,p)
        #print(request)
        self.sendall(request)
        self.socket.shutdown(socket.SHUT_WR)
        response = self.recvall(self.socket)

        code = self.get_code(response)
        body = self.get_body(response)
        #print("code: ")
        #print(code)
        #print("body: ")
        #print(body)
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
        print(client.command( sys.argv[2], sys.argv[1]))
    else:
        print(client.command( sys.argv[1] ))
