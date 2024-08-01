import re
import logging
import runpy

from endpoints import Controller, param

from .core import Q
from .config import commands


logger = logging.getLogger(__name__)


class Default(Controller):
    content_type = "text/html"

    @param("q", default="", type=Q, help="The query value")
    async def ANY(self, q, **kwargs):
        if q:
            v = commands.find(
                q,
                request=self.request,
                response=self.response,
                controller=self
            )

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
                    '<form name="autoform" action="{}" method="{}">'.format(
                        v["action"],
                        v.get("method", "POST")
                    )
                )

                for vk, vv in v.items():
                    body.append(
                        '    <input type="hidden" name="{}" value="{}" />'.format(
                            vk,
                            vv
                        )
                    )

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

        else:
            # if q is empty then give an input box to submit q

            # https://www.w3schools.com/html/html_forms.asp
            body = [
                "<!DOCTYPE html>",
                "<html>",
                "    <head>",
                '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',
                '        <meta name="referrer" content="none">',
                "    </head>",
                "    <body>",
                '<form action="/" method="GET">',
                '    <input type="text" name="q" id="q">',
                "</form>",
                "    </body>",
            ]

        return "\n".join(body)


class Favicon(Controller):
    """Ignores browser's auto /favicon.ico requests"""
    content_type = None
    ext = "ico"

    async def ANY(self):
        self.response.code = 404


class Robots(Controller):
    content_type="text/plain"
    ext = "txt"

    async def GET(self):
        return "\n".join([
            "User-agent: *",
            "Disallow: /",
        ])


class Opensearch(Controller):
    content_type = "text/xml"
    ext = "xml"

    async def GET(self):
        host = self.request.url.host()

        return "\n".join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            "",
            (
                '<OpenSearchDescription'
                ' xmlns="http://a9.com/-/spec/opensearch/1.1/"'
                ' xmlns:moz="http://www.mozilla.org/2006/browser/search/">'
            ),
            "    <ShortName>bounce</ShortName>",
            "    <Description>Bounce Search</Description>",
            "    <InputEncoding>UTF-8</InputEncoding>",
            #'    <Image height="16" width="16" type="image/x-icon">http://marcyes.com/favicon.ico</Image>',
            "",
            #"    <Contact>name@email.com</Contact>",
            '    <Url type="text/html" template="{}" method="GET">'.format(
                host
            ),
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
        ])


class List(Controller):
    content_type = "text/html"

    @param("q", default="", type=lambda q: q.lower(), help="The query value")
    async def GET(self, q):
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


class Healthcheck(Controller):
    """Here mainly for a docker healthcheck

    https://docs.docker.com/reference/dockerfile/#healthcheck
    """
    content_type="text/plain"

    async def GET(self):
        return "HEALTHY"

