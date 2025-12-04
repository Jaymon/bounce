import re
import logging
import runpy
from typing import Annotated
from collections.abc import Iterable
from string import Template

from endpoints import Controller

from .core import Q
from .config import commands


logger = logging.getLogger(__name__)


class Default(Controller):
    """The bounce homepage

    Usually, you would call this like this:

        <HOST>?q=<QUERY>

    If you don't include the `q` though it will give you a search box
    """
    async def ANY(self, q: Q|None = None, **kwargs) -> str:
        """
        :param q: The query value
        :returns: html
        """
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


class Favicon_ico(Controller):
    """Ignores browser's auto /favicon.ico requests"""
    async def ANY(self):
        self.response.code = 404


class Robots_txt(Controller):
    """Reject all robots"""
    async def GET_txt(self) -> str:
        return "\n".join([
            "User-agent: *",
            "Disallow: /",
        ])


class Opensearch_xml(Controller):
    """Handle Opensearch xml file

    https://developer.mozilla.org/en-US/docs/Web/XML/Guides/OpenSearch
    https://github.com/dewitt/opensearch

    draft docs:
        https://github.com/dewitt/opensearch/blob/master/opensearch-1-1-draft-6.md

    Other helpful links:
        https://theorangeone.net/posts/opensearch-browser-search-engine/
        https://perishablepress.com/custom-opensearch-functionality-for-your-website/
    """
    async def GET(self) -> Annotated[str, "application/opensearchdescription+xml"]:
        # the xmlns doesn't resolve, see: https://github.com/dewitt/opensearch/issues/3
        # That doesn't seem to matter though:
        #   The actual namespace itself, often a IRI, is of no real
        #   consequence. It should be unique, so people tend to choose a
        #   IRI/URI that they own, but it has no greater meaning than that.
        #   Sometimes people will place the schema (definition) for the XML at
        #   the specified IRI, but that is a convention of some people only.
        return Template("""
            <?xml version="1.0" encoding="UTF-8"?>

            <OpenSearchDescription
                xmlns="http://a9.com/-/spec/opensearch/1.1/">

                <ShortName>bounce</ShortName>
                <Description>Bounce Search</Description>
                <InputEncoding>UTF-8</InputEncoding>

                <Url type="text/html"
                    method="GET"
                    template="$HOST?q={searchTerms}" />

                <Url type="application/x-suggestions+json"
                    rel="suggestions"
                    template="$HOST?q={searchTerms}" />

                <SyndicationRight>limited</SyndicationRight>
                <AdultContent>false</AdultContent>
                <Language>en-us</Language>
            </OpenSearchDescription>
        """).substitute(
            HOST=self.request.url.host(),
        )


class List(Controller):
    """List all the configured keywords"""
    async def GET(self, q: str = "") -> str:
        lines = []
        lines.append('<table style="width: 100%;" border="1">')
        lines.append('<tr>')
        lines.append('<th>Keywords</th>')
        lines.append('<th>Domain</th>')
        lines.append('<th>Help</th>')
        lines.append('</tr>')

        if q:
            q = q.lower()

        # for display, sort the commands in alphabetical order
        cs = sorted(commands, key=lambda cmd: cmd[0])

        for cmd, val, note in cs:
            if q and q not in cmd.lower():
                continue
            lines.append('<tr >')
            lines.append('<td style="padding: 10px;">{}</td>'.format(cmd))
            lines.append('<td style="padding: 10px;">')
            if re.match(r"\S://", val):
                lines.append(val)

            else:
                lines.append('<pre>{}</pre>'.format(val))

            lines.append('</td>')
            lines.append('<td style="padding: 10px;">{}</td>'.format(note))
            lines.append('</tr>')

        lines.append('</table>')
        return "\n".join(lines)


class Suggest(Controller):
    """Return search suggestions

    https://github.com/dewitt/opensearch/blob/master/mediawiki/Specifications/OpenSearch/Extensions/Suggestions/1.1/Draft%201.wiki
    """
    async def GET(
        self,
        q: str = ""
    ) -> Annotated[
        list[
            str, # q
            list[str], # matching search terms
            list[str], # descriptions
        ],
        "application/x-suggestions+json",
    ]:
        search_terms = []
        descriptions = []
        for keyword, info in commands.commands.items():
            if keyword.startswith(q):
                search_terms.append(keyword)
                descriptions.append(info["note"])

        return [q, search_terms, descriptions]


class Healthcheck(Controller):
    """Here mainly for a docker healthcheck

    https://docs.docker.com/reference/dockerfile/#healthcheck
    """
    async def GET(self) -> Annotated[str, "text/plain"]:
        return "HEALTHY"

