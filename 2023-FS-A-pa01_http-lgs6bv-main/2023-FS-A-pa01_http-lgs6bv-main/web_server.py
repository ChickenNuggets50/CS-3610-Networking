#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
A simple Web server.
GET requests must name a specific file,
since it does not assume an index.html.
"""

import socket
import threading


def handler(conn_socket: socket.socket, address: tuple[str, int]) -> None:
    """
    Handles the part of the client work-flow that is client-dependent,
    and thus may be delayed by the user, blocking program flow.
    """
    try:
        # Receives the request message from the client
        msg = conn_socket.recv(1024)
        # print(address, " sent message: ", msg)

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        request_lines = msg.decode().split("\n")
        # print(request_lines)
        request_path = request_lines[0].split()[1]
        # print(request_path)

        # Because the extracted path of the HTTP request includes
        # a character '\', we read the path from the second character
        # Read file off disk, to send
        # Store the content of the requested file in a temporary buffer
        with open(request_path[1:], "rb") as file:
            file_data = file.read()

        # Send the HTTP response header line to the connection socket
        response_header = "HTTP/1.1 200 OK\r\n\r\n"
        conn_socket.send(response_header.encode())

        # Send the content of the requested file to the connection socket
        conn_socket.send(file_data)

    except IOError:
        # Send HTTP response message for file not found (404)

        response_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        conn_socket.send(response_header.encode())

        # Open file, store the content of the requested file in a temporary buffer (variable).
        error_file_data = open("web_files/not_found.html", "r")
        buffer = error_file_data.read()

        # Send the content of the requested file to the connection socket
        conn_socket.send(buffer.encode())

    except:
        print("Bad request")
    finally:
        conn_socket.close()


def main() -> None:
    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_port = 6789

    # print("Server started!")
    # print("Waiting for clients...")

    # Bind the socket to server address and server port
    # Delete pass and write
    server_socket.bind(("", server_port))

    # Listen to at most 2 connection at a time
    # Server should be up and running and listening to the incoming connections
    # Delete pass and write
    server_socket.listen(2)

    threads = []
    try:
        while True:
            # Set up a new connection from the client
            # Delete pass and write
            c, addr = server_socket.accept()
            # print("Got connection from", addr)

            # call handler here, start any threads needed
            # Delete pass and write
            new_thread = threading.Thread(target=handler, args=(c, addr))
            new_thread.start()

            # Just to keep track of threads
            threads.append(new_thread)
            # print(threads)
    except Exception as e:
        print("Exception occured (maybe you killed the server)")
        print(e)
    except:
        print("Exception occured (maybe you killed the server)")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
