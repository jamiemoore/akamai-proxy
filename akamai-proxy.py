"""
Proxy Akamai Production Requests to Staging
"""

import configparser
from mitmproxy import http, ctx

config = configparser.ConfigParser()
with open("config.ini", "r") as file_object:
    config.read_file(file_object)

for prod, stage in config["environments"].items():
    print("REDIRECTING:", prod, "->", stage)


def server_connect(server_connection):
    # ctx.log.info("server  %s" % server_connection)
    ctx.log.info("ORIG: server sni  %s" % server_connection.server.sni)
    for prod, stage in config["environments"].items():
        if server_connection.server.sni == stage:
            server_connection.server.sni = prod
            ctx.log.info("NEW: server sni  %s" % server_connection.server.sni)


def request(flow: http.HTTPFlow) -> None:
    for prod, stage in config["environments"].items():
        if flow.request.host == prod:
            ctx.log.info("ORIG: host: %s" % flow.request.host)
            flow.request.host = stage
            flow.request.headers["Host"] = prod
            ctx.log.info("NEW: host: %s" % flow.request.host)
