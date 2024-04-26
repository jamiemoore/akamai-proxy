"""
Proxy Akamai Production Requests to Staging
"""

import configparser
from mitmproxy import http, ctx, proxy


config = configparser.ConfigParser()
with open("config.ini", "r") as file_object:
    config.read_file(file_object)

for prod, stage in config["environments"].items():
    print("REDIRECTING:", prod, "->", stage)


def server_connect(server_connection):
    # ctx.log.info("server  %s" % server_connection)
    # ctx.log.info("server sni  %s" % server_connection.server.sni)
    for prod, stage in config["environments"].items():
        if server_connection.server.sni == stage:
            server_connection.server.sni = prod
            # ctx.log.info("new server sni  %s" % server_connection.server.sni)


def request(flow: http.HTTPFlow) -> None:
    for prod, stage in config["environments"].items():
        if flow.request.host == prod:
            # ctx.log.info("ORIGIONAL: flow header host: %s" % flow.request.headers["Host"])
            flow.request.host = stage
            flow.request.headers["Host"] = prod
