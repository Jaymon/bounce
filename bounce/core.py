import re
import urllib
import inspect


class Commands(object):
    def __init__(self):
        self.commands = {}
        self.default_cmd = ""

    def unquote(self, val):
        # py3 http://stackoverflow.com/questions/11768070/transform-url-string-into-normal-string-in-python-20-to-space-etc#comment44058808_11768102
        return urllib.unquote_plus(val)

    def quote(self, val):
        return urllib.quote_plus(val)

    def is_url(self, val):
        return True if re.match("\S+://\S+", val) else False

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
            # q is already a url
            return q

        bits = re.split("\s+", q, 1)
        cmd = bits[0].lower()
        question = bits[1] if len(bits) > 1 else ""
        if cmd not in self.commands:
            question = q
            cmd = self.default_cmd

        if "callback" in self.commands[cmd]:
            url = self.commands[cmd]["callback"](question)

        else:
            # http://stackoverflow.com/a/9345102/5006
            url = self.commands[cmd]["url"].format(urllib.quote_plus(question))

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

