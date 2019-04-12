# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import sys


# ripped from https://github.com/kennethreitz/requests/blob/master/requests/compat.py
_ver = sys.version_info
is_py2 = (_ver[0] == 2)
is_py3 = (_ver[0] == 3)


if is_py2:
    basestring = basestring
    unicode = unicode
    range = xrange

    import urlparse
    from urllib import quote_plus, unquote_plus
    from urllib import quote
    import __builtin__ as builtins
    from urllib import urlencode


elif is_py3:
    basestring = (str, bytes)
    unicode = str

    range = range

    import urllib.parse as urlparse
    from urllib.parse import quote_plus, unquote_plus
    from urllib.parse import quote
    import builtins
    from urllib.parse import urlencode


String = unicode if is_py2 else str
Bytes = str if is_py2 else bytes

