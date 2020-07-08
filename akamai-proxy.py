"""
Proxy Akamai Production Requests to Staging
"""
from mitmproxy import http, ctx

production = "www.akamai.com"
staging = "www.akamai.com.edgekey-staging.net"


def load(l):
    ctx.log.info("Registering option 'production'")
    l.add_option("production", str, production, "Production Hostname")
    ctx.log.info("Registering option 'staging'")
    l.add_option("staging", str, staging, "Staging Hostname")


def configure(updated):
    if "production" in updated:
        ctx.log.info("production hostname option value: %s" % ctx.options.production)
    if "staging" in updated:
        ctx.log.info("staging hostname option value: %s" % ctx.options.staging)


def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_host == ctx.options.production:
        flow.request.host = ctx.options.staging
        flow.request.headers["Host"] = ctx.options.production
