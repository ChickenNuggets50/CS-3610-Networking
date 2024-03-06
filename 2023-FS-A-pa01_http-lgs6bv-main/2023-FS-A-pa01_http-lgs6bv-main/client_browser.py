#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Run with the following command line parameters:
python3 client_browser.py <hostname> <port> <file>

Examples:
$ python3 client_browser.py info.cern.ch 80 "" # defaults to index.html
$ python3 client_browser.py localhost 6789 "hello_world.html"
"""

import sys
import socket

if len(sys.argv) != 4:
    server_hostname = "localhost"
    server_ip = "127.0.0.1"
    server_port = 6789
    file_name = "web_files/hello_world.html"
else:
    # Delete the pass and do your arg parsing here.
    # Hint, you may need to get an IP from a hostame.
    server_hostname = sys.argv[1]
    # print(server_hostname)
    server_port = int(sys.argv[2])
    # print(server_port)
    file_name = sys.argv[3]
    # print(file_name)


try:
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # Delete the pass and make your GET request here
    server_ip = socket.gethostbyname(server_hostname)
    # print(server_ip)
    server_address = (server_ip, server_port)
    # print(server_address)
    client_socket.connect(server_address)

    get_request = f"GET /{file_name} HTTP/1.1\r\nHost: {server_hostname}\r\n\r\n"
    client_socket.send(get_request.encode())

    # Delete the pass and parse the return data here.
    # Hint: a loop helps to make sure you got all the data.
    # Just print what's returned from the server.
    response_data = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response_data += data

    print(response_data.decode())


except Exception as e:
    print("Exception was: ", e)

finally:
    client_socket.close()
