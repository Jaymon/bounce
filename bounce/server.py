import re
import logging

from flask import Flask, session, redirect, url_for, escape, request

from .core import commands


app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/')
def index():

    q = request.args.get('q', '')
    if commands.is_url(q):
        # we pull out q this way because we are tricksy here, because q can contain urls
        # and those urls can have ? and & we want to respect that without the person submitting
        # having to worry about encoding the url. So everything after the q is considered part of the
        # q regardless of it has & in it, this also means that we violate the http spec because
        # query string parameters actually have order, shrug
        m = re.search("q=(.*$)", request.environ.get("QUERY_STRING", ""))
        q = commands.unquote(m.group(1))

    v = commands.find(q)
    if commands.is_url(v):
        body = [
            "<!DOCTYPE html>",
            "<html>",
            "    <head>",
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',
            '        <meta http-equiv="refresh" content="0;url=\'{}\'">'.format(v),
            '        <meta name="referrer" content="none">',
            "    </head>",
            "    <body></body>",
            "</html>",
        ]

        logger.info("Redirecting to {}".format(v))

    elif isinstance(v, dict):
        body = [
            "<!DOCTYPE html>",
            "<html>",
            "    <head>",
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',
            '        <meta name="referrer" content="none">',
            "    </head>",
            '    <body onload="setTimeout(function() { document.autoform.submit() }, 0)">',
        ]

        body.append(
            '<form name="autoform" action="{}" method="{}">'.format(v["action"], v.get("method", "POST"))
        )

        for vk, vv in v.items():
            body.append('    <input type="hidden" name="{}" value="{}" />'.format(vk, vv))

        body.append('</form>')
        body.extend(["</body>", "</html>",])

    else:
        body = [
            "<!DOCTYPE html>",
            "<html>",
            "    <head>",
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',
            "        <title>{}</title>".format(q),
            "    </head>",
            "    <body>",
            v,
            "    </body>",
            "</html>",
        ]

    return "\n".join(body)


@app.route("/robots.txt")
def robots():
    #<link rel="search" type="application/opensearchdescription+xml" title="search" href="/opensearch.xml">
    headers = {"Content-Type": "text/plain; charset=utf-8"}
    return ("\n".join([
        "User-agent: *",
        "Disallow: /",
    ]), 200, headers)


@app.route("/opensearch.xml")
def opensearch():
    #<link rel="search" type="application/opensearchdescription+xml" title="search" href="/opensearch.xml">
    headers = {"Content-Type": "text/xml; charset=utf-8"}
    host = url_for("index", _external=True)
    return ("\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        "",
        '<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/" xmlns:moz="http://www.mozilla.org/2006/browser/search/">',
        "    <ShortName>bounce</ShortName>",
        "    <Description>Bounce Search</Description>",
        "    <InputEncoding>UTF-8</InputEncoding>",
        #'    <Image height="16" width="16" type="image/x-icon">http://marcyes.com/favicon.ico</Image>',
        "",
        #"    <Contact>name@email.com</Contact>",
        '    <Url type="text/html" template="{}" method="GET">'.format(host),
        '        <Param name="q" value="{searchTerms}"/>',
        #'        <Param name="collection" value="default_collection"/>',
        '        <Param name="opensearch" value="1"/>',
        "    </Url>",
        "    <moz:SearchForm>{}</moz:SearchForm>".format(host),
        "    <SyndicationRight>limited</SyndicationRight>",
        "",
        "    <AdultContent>false</AdultContent>",
        "    <Language>en-us</Language>",
        "</OpenSearchDescription>",
    ]), 200, headers)


@app.route("/list/")
def ls():
    q = request.args.get('q', '')
    if q: q = q.lower()

    lines = []
    lines.append('<table style="width: 100%;" border="1">')
    lines.append('<tr>')
    lines.append('<th>Keywords</th>')
    lines.append('<th>domain</th>')
    lines.append('<th>note</th>')
    lines.append('</tr>')

    # for display, sort the commands in alphabetical order
    cs = sorted(commands, key=lambda cmd: cmd[0])

    for cmd, val, note in cs:
        if q and q not in cmd.lower(): continue
        lines.append('<tr >')
        lines.append('<td style="padding: 10px;">{}</td>'.format(cmd))
        lines.append('<td style="padding: 10px;">')
        if re.match("\S://", val):
            lines.append(val)

        else:
            lines.append('<pre>{}</pre>'.format(val))

        lines.append('</td>')
        lines.append('<td style="padding: 10px;">{}</td>'.format(note))
        lines.append('</tr>')

    lines.append('</table>')
    return "\n".join(lines)

