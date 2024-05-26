#!/usr/bin/env python3
import re


class HTTPMessage:
    HTTPVER_EXPR = r'HTTP/(?P<httpver>[\d\.]+)'
    PARAMETER_RE = re.compile(r'([\w-]+):\s*(.*)\n?')
    PARAMETER_FMTS = "{name}: {value}\n"
    REQ_RE = re.compile(
        r'^(?P<reqtype>\w+)\s+(?P<path>.*)\s+' + HTTPVER_EXPR + r'\s+')
    RES_RE = re.compile(
            r'^' + HTTPVER_EXPR +
            r'\s+(?P<statuscode>\d+)\s+(?P<statusmessage>.*)')
    RES_HEADER_FMTS = "HTTP/{ver} {statuscode} {statusmsg}\n"


def parse_http_parameters(text: str, starting_pos=0) -> dict:
    """
    Parses the given text for parameters in the form expressed by
    http requests/responses.
    Returns a dictionary representing the parameters.
    """
    ret_dict = dict()
    position = starting_pos
    m: re.Match
    while (m := HTTPMessage.PARAMETER_RE.match(text, position)):
        position = m.span()[1]
        re_groups = m.groups()
        ret_dict[re_groups[0]] = re_groups[1]
    return ret_dict


def parse_http_request(req_text: str) -> dict:
    """
    Parses the given http request, returning a dictionary containing the
    http request's details
    """
    ret_dict: dict = None
    m = HTTPMessage.REQ_RE.match(req_text)
    if m is not None:
        ret_dict = dict()
        ret_dict['reqdata'] = dict(m.groupdict())
        ret_dict['parameters'] = parse_http_parameters(req_text, m.span()[1])
    return ret_dict


def generate_http_response(
        protocol_version: str,
        status_code: int,
        status_message: str,
        additional_params: dict,
        body: bytes = b"") -> bytes:
    """
    Encodes an http response.
    the additional_params dict must contain a
    'parameters' key containing a list of tuple
    pairs denoting the parameter's name and value, respectively.
    """
    response_str_list = list()
    response_text.append(HTTPMessage.RES_HEADER_FMTS.format(
        ver=protocol_version,
        statuscode=status_code,
        statusmsg=status_text))
    for name, value in additional_params.items():
        response_text.append(HTTPMessage.PARAMETER_FMTS.format(name, value))
    return bytes.join((str.join(response_str_list).encode('ascii'), body))
