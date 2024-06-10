#!/usr/bin/env python3
import socket
import argparse
import webserver

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
        webserver.accept_and_split(server_socket, webserver.handle_http_request)


if __name__ == "__main__":
    main()
