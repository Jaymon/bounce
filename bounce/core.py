# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import re
import inspect

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    from urllib import quote_plus, unquote_plus
except ImportError:
    from urllib.parse import quote_plus, unquote_plus


class Url(str):
    def __new__(cls, val):
        instance = super(Url, cls).__new__(cls, val)

        parts = urlparse.urlparse(val)
        instance.scheme = parts.scheme
        instance.hostname = parts.hostname

        instance.path_args = []
        instance.path = parts.path
        if instance.path:
            instance.path_args = filter(None, parts.path.split("/"))

        instance.netloc = parts.netloc
        instance.port = parts.port
        instance.fragment = parts.fragment
        instance.username = parts.username
        instance.password = parts.password

        instance.query = parts.query
        instance.query_kwargs = {}
        if instance.query:
            query_kwargs = {}
            for k, kv in urlparse.parse_qs(parts.query, True, True).items():
                if len(kv) > 1:
                    query_kwargs[k] = kv
                else:
                    query_kwargs[k] = kv[0]
            instance.query_kwargs = query_kwargs

        return instance


class Q(str):
    def __new__(cls, val):
        instance = super(Q, cls).__new__(cls, val)
        return instance

    def unquote(self):
        return unquote_plus(self)

    def quote(self):
        return quote_plus(self)

    def url(self):
        return Url(self)

    def is_url(self):
        return True if re.match("\S+://\S+", self) else False

    def match(self, regex, flags=re.I):
        return re.match(regex, flags=flags)


class Commands(object):
    def __init__(self):
        self.commands = {}
        self.default_cmd = ""

    def unquote(self, val):
        # py3 http://stackoverflow.com/questions/11768070/transform-url-string-into-normal-string-in-python-20-to-space-etc#comment44058808_11768102
        return Q(val).unquote()

    def quote(self, val):
        return Q(val).quote()

    def is_url(self, val):
        return Q(val).is_url()

    def add(self, commands, val, note="", default=False):
        cmds = re.split("\s+", commands)
        if default:
            self.default_cmd = cmds[0]

        for cmd in cmds:
            cmd = cmd.lower()
            if cmd in self.commands:
                raise ValueError("{} already assigned".format(cmd))

            if isinstance(val, basestring):
                self.commands[cmd] = {
                    "url": val,
                    "note": note
                }

            else:
                self.commands[cmd] = {
                    "callback": val,
                    "note": note
                }

    def find(self, q):
        if self.is_url(q): 
            return q

        bits = re.split("\s+", q, 1)
        cmd = bits[0].lower()
        if cmd in self.commands:
            question = Q(bits[1] if len(bits) > 1 else "")

        else:
            question = Q(q)
            cmd = self.default_cmd

        if "callback" in self.commands[cmd]:
            url = self.commands[cmd]["callback"](question)

        else:
            # http://stackoverflow.com/a/9345102/5006
            url = self.commands[cmd]["url"].format(question.quote())

        return url

    def __iter__(self):
        d = {}
        for cmd, options in self.commands.items():
            if "callback" in options:
                key = inspect.getsource(options["callback"])

            else:
                key = options["url"]

            if key not in d:
                d[key] = {
                    "cmds": [],
                    "note": options.get("note", "")
                }

            d[key]["cmds"].append(cmd)

        for key, vals in d.items():
            yield " ".join(vals["cmds"]), key, vals["note"]


commands = Commands()

