#!/usr/bin/env python3
import threading
from typing import Callable
import socket
from . import utils

class HTTPConsts:
    MAX_REC_BUF_SIZE = 4096


def handle_http_request(conn_socket: socket.socket):
    """
    Handles single http request coming from conn_socket.
    """
    req_raw = conn_socket.recv(HTTPConsts.MAX_REC_BUF_SIZE).decode("ascii")
    print(utils.parse_http_request(req_raw))


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
                target=handler,
                args=(conn[0],),
                daemon=True,
            ).start()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
