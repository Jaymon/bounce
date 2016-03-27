import re

from flask import Flask, session, redirect, url_for, escape, request

from .core import commands


app = Flask(__name__)


@app.route('/')
def index():
    q = request.args.get('q', '')
    if q in set(["list", "ls"]):
        return redirect(url_for('ls'))

    url = commands.find(q)
    return "\n".join([
        "<!DOCTYPE html>",
        "<html>",
        "    <head>",
        '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',
        '        <meta http-equiv="refresh" content="0;url=\'{}\'">'.format(url),
        '        <meta name="referrer" content="none">',
        "    </head>",
        "    <body></body>",
        "</html>",
    ])


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
    lines = []
    lines.append('<table style="width: 100%;" border="1">')
    lines.append('<tr>')
    lines.append('<th>Keywords</th>')
    lines.append('<th>domain</th>')
    lines.append('<th>note</th>')
    lines.append('</tr>')

    for cmd, val, note in commands:
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

