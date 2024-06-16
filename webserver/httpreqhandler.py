#!/usr/bin/env python3
import threading
from typing import Callable
import socket
from . import utils
import os

class HTTPConsts:
    MAX_REC_BUF_SIZE = 4096


def get_resource(resource_path: str) -> tuple[int, bytes]:
    """
    Returns tuple containing status code and resource contained in resource_path.
    """
    pass
def handle_http_request(conn_socket: socket.socket, htdocs_dir: str):
    """
    Handles single http request coming from conn_socket.
    """
    req_raw = conn_socket.recv(HTTPConsts.MAX_REC_BUF_SIZE).decode("ascii")
    req = utils.parse_http_request(req_raw)
    # This method of creating a resource path is very dangerous and prone to trivial exploits.
    # Writing a better solution is beyond the scope of this work
    resource_path = os.path.join(htdocs_dir, '.'+req['reqdata']['path'])

    res_headers : list[tuple[str, str]] = list()
    res_data : bytes
    res_statuscode : int
    res_statusmessage : str

    match req['reqdata']['reqtype']:
        case 'GET':
            res_data = get_resource(resource_path)
        case _:
            pass


def accept_and_split(
        socket: socket.socket,
        handler: Callable[[socket.socket, tuple], None],
        *args):
    """
    Accepts all incoming connections on socket indefinitely
    (unless a KeyboardInterrupt is received),
    handling them by generating separate threads
    """
    handler_target : Callable[[socket.socket], None] = lambda s: handler(s, *args)
    try:
        while True:
            conn = socket.accept()
            threading.Thread(
                target=handler_target,
                args=(conn[0],),
                daemon=True,
            ).start()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
