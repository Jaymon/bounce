
import testdata
from testdata import TestCase
from datatypes import (
    WSGIServer,
    ServerThread,
)

from bounce.core import Q, Url
from bounce.__main__ import application
from bounce import commands


testdata.basic_logging()


class Server(ServerThread):
    def __new__(cls, **kwargs):
        kwargs.setdefault("application", application)
        server = WSGIServer(**kwargs)
        return super().__new__(cls, server, **kwargs)

    def fetch(self, q):
        with self:
            return testdata.fetch(self, query={"q": q})


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


class DefaultTest(TestCase):
    def test_unicode(self):
        s = Server()
        r = s.fetch("yt {}".format(testdata.get_unicode_words()))
        self.assertEqual(200, r.code)


class FaviconTest(TestCase):
    def test_404(self):
        s = Server()
        with s:
            r = self.fetch(s.child("favicon.ico"))
            self.assertEqual(404, r.code)


class RobotsTest(TestCase):
    def test_success(self):
        s = Server()
        with s:
            r = self.fetch(s.child("robots.txt"))
            self.assertEqual(200, r.code)
            self.assertTrue(
                r.headers.get("Content-Type").startswith("text/plain")
            )


class OpensearchTest(TestCase):
    def test_success(self):
        s = Server()
        with s:
            r = self.fetch(s.child("opensearch.xml"))
            self.assertEqual(200, r.code)
            media_type = "application/opensearchdescription+xml"
            content_type = r.headers.get("Content-Type")
            self.assertTrue(
                content_type.startswith(media_type),
                f"{content_type} is not {media_type}",
            )


class ListTest(TestCase):
    def test_success(self):
        s = Server()
        with s:
            r = self.fetch(s.child("list"))
            self.assertEqual(200, r.code)
            self.assertTrue(
                r.headers.get("Content-Type").startswith("text/html")
            )

    def test_redirect(self):
        s = Server()
        with s:
            r = self.fetch(s.child(query_kwargs={"q": "list"}))
            body = r.text
            self.assertEqual(200, r.code)
            self.assertTrue("referrer" in body)
            self.assertTrue("refresh" in body)
            self.assertTrue("/list" in body)


class SuggestTest(TestCase):
    def test_success(self):
        s = Server()
        with s:
            r = self.fetch(s.child("suggest"), query={"q": "g"})
            self.assertEqual(200, r.code)
            media_type = "application/x-suggestions+json"
            content_type = r.headers.get("Content-Type")
            self.assertTrue(
                content_type.startswith(media_type),
                f"{content_type} is not {media_type}",
            )
            self.assertEqual("g", r.json()[0])

