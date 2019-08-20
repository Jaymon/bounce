# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import re
import inspect
import logging

from .compat import *
from . import environ
from .compat import String as BaseString


logger = logging.getLogger(__name__)


class String(BaseString):
    """Small wrapper around string/unicode that guarantees output will be a real
    string ("" in py3 and u"" in py2) and won't fail with a UnicodeException"""
    def __new__(cls, arg):
        '''
        make sure arg is a unicode string
        arg -- mixed -- arg can be anything
        return -- unicode -- a u'' string will always be returned
        '''
        if isinstance(arg, Bytes):
            arg = arg.decode(environ.ENCODING)

        else:
            if not isinstance(arg, BaseString):
                arg = BaseString(arg)

        return super(String, cls).__new__(cls, arg)


class Url(String):
    def __new__(cls, *paths, **query_kwargs):
        val = cls.combine(*paths, **query_kwargs)
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

    @classmethod
    def combine(cls, *paths, **query_kwargs):
        """take the basic parts of the path and combine them

        :param *paths: strings, these are the parts of a url to the left of the ?
        :param **query_kwargs: dict, keys are variable names and values are those variable's values
        :returns: string, a full combined url that contains all of paths and query_kwargs
        """
        path = "/".join(paths)
        if query_kwargs:
            query = urlencode(query_kwargs, doseq=True)

            if path.endswith("?"):
                ret = "{}{}".format(path, query)

            elif "?" in path:
                ret = "{}&{}".format(path, query)

            else:
                ret = "{}?{}".format(path, query)

        else:
            ret = path

        return ret


class Q(String):
    def __new__(cls, val):
        instance = super(Q, cls).__new__(cls, val)
        return instance

    def unquote(self):
        return unquote_plus(self)

    def quote(self, plus=True):
        bs = self.encode(environ.ENCODING)
        qs = quote_plus(bs) if plus else quote(bs)
        return qs.decode(environ.ENCODING)

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

    def add(self, commands, val, note="", default=False, plus=True):
        cmds = re.split("\s+", commands)
        if default:
            self.default_cmd = cmds[0]

        for cmd in cmds:
            cmd = cmd.lower()
            if cmd in self.commands:
                logger.warning("{} already assigned".format(cmd))

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

            self.commands[cmd]["plus"] = plus


    def find(self, q):
        logger.debug("Searching for q: {}".format(q))

        if self.is_url(q): 
            logger.debug("q is a url, redirecting")
            return q

        bits = re.split("\s+", q, 1)
        cmd = bits[0].lower()
        if cmd in self.commands:
            logger.debug("Command {} was found".format(cmd))
            question = Q(bits[1] if len(bits) > 1 else "")

        else:
            logger.debug("Command {} was NOT found, using default command: {}".format(
                cmd,
                self.default_cmd
            ))
            question = Q(q)
            cmd = self.default_cmd

        if "callback" in self.commands[cmd]:
            logger.debug("Command {} is a callback".format(cmd))
            ret = self.commands[cmd]["callback"](question)
            if isinstance(ret, basestring):
                ret = BaseString(ret)

        else:
            # http://stackoverflow.com/a/9345102/5006
            ret = BaseString(self.commands[cmd]["url"]).format(question.quote(self.commands[cmd]["plus"]))

        logger.debug("Found {}".format(ret))
        return ret

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

