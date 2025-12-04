# -*- coding: utf-8 -*-
import re
import inspect
import logging
from urllib.parse import quote_plus, quote, unquote_plus

from datatypes import (
    String,
    Url
)


logger = logging.getLogger(__name__)


class Q(String):
    def __new__(cls, q, **kwargs):
        instance = super().__new__(cls, q)

        for k, v in kwargs.items():
            setattr(instance, k, v)

        return instance

    def unquote(self):
        return unquote_plus(self)

    def quote(self, plus=True):
        return quote_plus(self) if plus else quote(self)

    def url(self):
        return Url(self)

    def is_url(self):
        return True if re.match(r"\S+://\S+", self) else False

    def match(self, regex, flags=re.I):
        return re.match(regex, flags=flags)


class Commands(object):
    def __init__(self):
        self.commands = {}
        self.default_cmd = ""

    def unquote(self, val):
        # py3 http://stackoverflow.com/questions/11768070/
        return Q(val).unquote()

    def quote(self, val):
        return Q(val).quote()

    def is_url(self, val):
        return Q(val).is_url()

    def add(self, commands, val, note="", default=False, plus=True):
        cmds = re.split(r"\s+", commands)
        if default:
            self.default_cmd = cmds[0]

        for cmd in cmds:
            cmd = cmd.lower()
            if cmd in self.commands:
                logger.warning("{} already assigned".format(cmd))

            if isinstance(val, str):
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

    def find(self, q, **kwargs):
        logger.debug("Searching for q: {}".format(q))

        if self.is_url(q): 
            logger.debug("q is a url, redirecting")
            return q

        bits = re.split(r"\s+", q, 1)
        cmd = bits[0].lower()
        if cmd in self.commands:
            logger.debug("Command {} was found".format(cmd))
            question = Q(bits[1] if len(bits) > 1 else "", **kwargs)

        else:
            logger.debug(
                "Command {} was NOT found, using default command: {}".format(
                    cmd,
                    self.default_cmd
                )
            )
            question = Q(q, **kwargs)
            cmd = self.default_cmd

        if "callback" in self.commands[cmd]:
            logger.debug("Command {} is a callback".format(cmd))
            ret = self.commands[cmd]["callback"](question)
            if isinstance(ret, str):
                ret = str(ret)

        else:
            # http://stackoverflow.com/a/9345102/5006
            ret = String(self.commands[cmd]["url"]).format(
                question.quote(self.commands[cmd]["plus"])
            )

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

