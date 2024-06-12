#!/usr/bin/env python3
import socket
import argparse
import webserver
import os
import stat

class ReadableDir(object):
    def __init__(self):
        pass

    def _raise_error(self, string):
        raise argparse.ArgumentTypeError(f'{string} is not a path to a directory.')

    def __call__(self, string):
        try:
            mode = os.stat(string)
            return string
        except FileNotFoundError:
            pass
        self._raise_error(string)


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
    parser.add_argument('-d', '--directory',
                        help='Directory to fetch resources from',
                        default='./htdocs/',
                        type=ReadableDir())

    return parser.parse_args()


def main():
    arg_namespace = parse_args()
    listen_addr = (arg_namespace.host, arg_namespace.port)

    with socket.create_server(listen_addr) as server_socket:
        webserver.accept_and_split(server_socket, webserver.handle_http_request, arg_namespace.directory)


if __name__ == "__main__":
    main()
