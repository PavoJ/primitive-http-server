#!/usr/bin/env python3
import socket
import argparse
import sys
from typing import Callable
import threading
import webserver


def handle_http_request(conn_socket: socket.socket):
    MAX_BUF_SIZE = 4096
    req_raw = conn_socket.recv(MAX_BUF_SIZE).decode("ascii")
    print(webserver.parse_http_request(req_raw))


def accept_and_split(
        socket: socket.socket,
        handler: Callable[[socket.socket], None]):
    """
    Accepts all incoming connections on socket indefinitely
    (unless a KeyboardInterrupt is received),
    handling them by generating separate threads
    """
    try:
        while True:
            conn = socket.accept()
            threading.Thread(
                target=handle_http_request,
                args=(conn[0],),
                daemon=True,
            ).start()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")


def parse_args() -> argparse.Namespace:
    """
    Parses the CLI arguments, prints the help message if asked for by the user.
    """
    parser = argparse.ArgumentParser(
        prog='Simple HTTP Server',
        description='Simple HTTP server made with sockets.',
        epilog='Made by Giovanni Paone (1089378)')

    parser.add_argument('--host',
                        help='Host to listen on',
                        default='0.0.0.0')
    parser.add_argument('-p', '--port',
                        help='Port to listen on',
                        default=80,
                        type=int)

    return parser.parse_args()


def main():
    arg_namespace = parse_args()
    listen_addr = (arg_namespace.host, arg_namespace.port)

    with socket.create_server(listen_addr) as server_socket:
        accept_and_split(server_socket, handle_http_request)


if __name__ == "__main__":
    main()