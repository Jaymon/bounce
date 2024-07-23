# -*- coding: utf-8 -*-

import testdata
from testdata import TestCase
from datatypes import (
    WSGIServer,
    ServerThread
)

from bounce.core import Q, Url
from bounce import commands


testdata.basic_logging()


class Server(ServerThread):
    def __new__(cls, **kwargs):
        kwargs.setdefault("wsgifile", "bounce/bin/bounce-wsgi.py")
        server = WSGIServer(**kwargs)
        return super().__new__(cls, server, **kwargs)

    def fetch(self, q):
        with self:
            return testdata.fetch(self, query={"q": q})


# class Server(WSGIServer):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault("wsgifile", "bounce/bin/bounce-wsgi.py")
# 
#     def fetch(self, q):
#         with self:
#             return testdata.fetch(self, query={"q": q})


class CommandsTest(TestCase):
    def test_space(self):
        cmd = testdata.get_ascii()
        commands.add(cmd, "{}", plus=False)

        url = commands.find("{} foo bar che".format(cmd))
        self.assertTrue("%20" in url)
        self.assertFalse("+" in url)

        commands.add(cmd, "{}")
        url = commands.find("{} foo bar che".format(cmd))
        self.assertTrue("+" in url)
        self.assertFalse("%20" in url)

    def test_py(self):
        url = commands.find("py max")
        self.assertTrue("/functions.html" in url)
        url = commands.find("py RuntimeError")
        self.assertTrue("/exceptions.html" in url)

    def test_chef(self):
        url = commands.find("ch execute")
        self.assertTrue(url.endswith("/execute/"))

        url = commands.find("ch")
        self.assertTrue(url.endswith("/resources/"))

        url = commands.find("ch common")
        self.assertTrue(url.endswith("#common-functionality"))

    def test_ruby(self):
        url = commands.find("rb string")
        self.assertTrue(url.endswith("String.html"))

        url = commands.find("rb {}")
        self.assertTrue(url.endswith("Hash.html"))

    def test_videoeta(self):
        url = commands.find("videoeta")
        # no errors is good

    def test_unquote(self):
        v = commands.find("unquote %2A")
        self.assertEqual("*", v)

    def test_list(self):
        v = commands.find("list foo bar")
        self.assertTrue("foo+bar" in v)

        v = commands.find("list")
        self.assertTrue("/list" in v)

    def test_syntax_errors(self):
        for key, val in commands.commands.items():
            q = f"{key} {testdata.get_words()}"
            try:
                commands.find(q)

            except ValueError as e:
                if "invalid literal for int() with base 10" in str(e):
                    q = f"{key} {testdata.get_int(1, 999)}"
                    commands.find(q)


class RequestTest(TestCase):
    def test_unicode(self):
        s = Server()
        r = s.fetch("yt {}".format(testdata.get_unicode_words()))
        self.assertEqual(200, r.code)

    def test_body(self):
        s = Server()
        r = s.fetch("unquote %2A")
        pout.v(r)


class QTest(TestCase):
    def test_url(self):
        url = testdata.get_url()
        v = Q(url)
        self.assertTrue(v.is_url())

        u = v.url()
        self.assertTrue(url.endswith(u.netloc))

    def test_unicode(self):
        s = "yt {}".format(testdata.get_unicode_words())
        q = Q(s)
        self.assertEqual(s, q)

