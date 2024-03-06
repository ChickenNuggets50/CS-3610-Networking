#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import threading
from typing import Optional


def serve_client(client_socket: socket.socket) -> None:
    """
    1. receives from the client,
    2. extracts the hostname and port from its request,
    3. forwards the message unchanged to the remote,
    4. receives a response from the remote by calling receive_response,
    5. sends that message back to the client
    6. Close the out_socket at the end of the request
    """
    request = receive_header(client_socket)
    hostname_info = extract_hostname(request)

    if hostname_info is not None:
        out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out_socket.connect(hostname_info)
        out_socket.send(request)
        response_message = receive_response(out_socket)
        client_socket.send(response_message)

        client_socket.close()
        out_socket.close()
    else:
        client_socket.close()


def receive_header(sock: socket.socket) -> bytes:
    """
    receives from the socket until either:
    a HTTP header is received,
    or the socket is closed.
    """
    header = b""
    while True:
        data = sock.recv(4096)
        if not data:
            break
        header += data
        if b"\r\n\r\n" in header:
            break
    return header


def extract_hostname(message: bytes) -> Optional[tuple[bytes, int]]:
    """
    Extracts the hostname and port from the HTTP header's Host field,
    and returns them as a tuple (hostname, port).
    Does not decode the hostname (leaves it as bytes)
    If no port is specified, it assumes the port is 80
    If no hostname is present, it returns None
    """
    host_line = message.split(b"\r\n")[1]
    host_line = host_line.strip()
    if b"Host" in host_line:
        host_info = host_line.split(b" ")[1].split(b":")
        if len(host_info) == 1:
            return host_info[0], 80
        elif len(host_info) == 2:
            try:
                port = int(host_info[1])
                return host_info[0], port
            except ValueError:
                return None
    return None


def receive_response(out_socket: socket.socket) -> bytes:
    """
    Receives the messages from the out_socket,
    and sends them to the client_socket.
    Receives HTTP message from the out_socket
    (HTTP request must already be sent by caller)
    Receive until the content is fully transmitted
    Return the message in full
    """
    response = b""
    while True:
        data = out_socket.recv(4096)
        if not data:
            break
        response += data
    return response


def main() -> None:
    """
    Creates the proxy server's main socket and binds to it.
    With each new client that connects,
    serves their requests.
    This one is done for you.
    """
    # create the server socket, a TCP socket on localhost:6789
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("", 6789))

    # listen for connections
    server_sock.listen(20)

    # forever accept connections
    # thread list is never cleaned (this is a vulnerability)
    threads = []
    while True:
        client_sock, addr = server_sock.accept()
        threads.append(threading.Thread(target=serve_client, args=(client_sock,)))
        threads[-1].start()


if __name__ == "__main__":
    main()
