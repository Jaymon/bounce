# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import

import testdata
from testdata import TestCase
from testdata.server import WSGIServer

from bounce.compat import *
from bounce.core import Q
from bounce import commands


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


class RequestTest(TestCase):
    def test_unicode(self):
        s = Server()
        r = s.fetch("yt {}".format(testdata.get_unicode_words()))
        self.assertEqual(200, r.code)


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

