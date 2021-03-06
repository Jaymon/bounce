# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import

import testdata
from testdata import TestCase
from testdata.server import WSGIServer

from bounce.compat import *
from bounce.core import Q, Url
from bounce import commands


testdata.basic_logging()


class Server(WSGIServer):
    def __new__(cls, hostname="", port=None):
        instance = super(Server, cls).__new__(
            cls,
            hostname=hostname,
            port=port,
            wsgifile="bounce/bin/bouncefile.py"
        )
        return instance

    def fetch(self, q):
        with self:
            return testdata.fetch(self, query={"q": q})


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

    def test_concat(self):
        cmd = testdata.get_ascii()
        commands.add(cmd, b"{}")
        # no exception being raised is a success
        url = commands.find("{} {}".format(cmd, testdata.get_unicode_words()))

        #url = commands.find("{} \U0001F646".format(cmd))
        #pout.v(url)

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


class UrlTest(TestCase):
    def test_combine(self):
        url = Url.combine("http://example.com", foo="bar", che="*")
        self.assertEqual("http://example.com?foo=bar&che=%2A", url)

        url = Url("http://foo.com?foo=bar", che="1/2/3")
        self.assertEqual("http://foo.com?foo=bar&che=1%2F2%2F3", url)

