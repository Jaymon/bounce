# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import re
import inspect
import datetime
import calendar

from flask import url_for
from .compat import *

from .core import commands, Url


commands.add("g google", "http://www.google.com/search?q={}", default=True) # google
commands.add("gm googlemap", "http://maps.google.com/?q={}") # google maps
commands.add("goopat gp googlepatent googlepatents", "http://www.google.com/patents?btnG=Search+Patents&q={}")
commands.add("gi", "http://images.google.com/images?um=1&ie=UTF-8&sa=N&tab=wi&q={}")
# 9-29-11
commands.add("gt translate trans", "http://translate.google.com/translate?hl=en&sl=auto&tl=en&u={}")

commands.add("dictionary", "http://www.dictionary.com/browse/{}") # dictionary
commands.add("wd wikidict dw", "https://en.wiktionary.org/wiki/{}") # dictionary
# 11-13-09
commands.add("d dict dic nw ninja", "http://ninjawords.com/?q={}", "definition for word")
# 09-26-2017
commands.add("s ds sy syn", "https://www.powerthesaurus.org/{}/synonyms", "Synonyms for word")
commands.add("da an ant", "https://www.powerthesaurus.org/{}/antonyms", "Antonyms for word")

commands.add("wk", "http://en.wikipedia.org/wiki/Special:Search?fulltext=Search&search={}")
commands.add("wpg wkg wikigoogle", "http://www.google.com/custom?domains=en.wikipedia.org&sitesearch=en.wikipedia.org&q={}")
commands.add("tv", "http://www.tv.com/search.php?type=11&stype=all&tag=search%3Bbutton&qs={}")
commands.add("yhoo", "http://search.yahoo.com/bin/search?p={}")
commands.add("a am amazon amaz", "http://www.amazon.com/s/ref=nb_ss_gw/102-5754341-9464967?url=search-alias%3Daps&Go=Go&field-keywords={}")
commands.add("epg ep epguides eg", "http://www.google.com/search?hl=en&q=allintitle%3A&q=site%3Aepguides.com&btnG=Search&q={}")
#commands.add("yt", "http://www.youtube.com/results?search=Search&search_query={}")
def yt_callback(q):
    # updated to just go to homescreen on 1-21-2021
    if q:
        url = "http://www.youtube.com/results?search=Search&search_query={}".format(q)
    else:
        url = "http://www.youtube.com/"
    return url
commands.add("yt", yt_callback, "Search Youtube")
#commands.add("yt", "http://www.youtube.com/results?search=Search&search_query={}")

# 8-8-12, updated to youtubensfw on 1-22-2021
def ytnsfw_callback(q):
    # allows watching youtube nsfw vidoes without logging in
    url = re.sub(r".youtube.", ".youtubensfw.", q, count=1)
#     m = re.match("/v=([^&]+)/", q)
#     if m:
#         url = 'http://deturl.com/play.asp?v={}'.format(m.group(1))
    return url
commands.add("yti ty yta ytnsfw", ytnsfw_callback)

commands.add("imdb", "http://www.imdb.com/find?s=all&q={}")
commands.add("bmn bug bugmenot", "http://www.bugmenot.com/view/{}")
commands.add("wks wikiseek", "http://www.wikiseek.com/results.php?q={}")
commands.add("gd", "http://www.godaddy.com/gdshop/registrar/search.asp?isc=ffsearch&checkavail=1&domaintocheck={}")
commands.add("ws websnif websniff", "http://web-sniffer.net/?submit=Submit&http=1.1&gzip=yes&type=GET&url={}")
commands.add("e eb ebay", "http://www.ebay.com/sch/i.html?_nkw={}")
# added 1-6-08...
def php_callback(q):
    if q:
        url = "http://us2.php.net/{}".format(q)
    else:
        url = "http://us2.php.net/manual/en/funcref.php"
    return url
#commands.add("php", "http://us2.php.net/{}")
commands.add("php", php_callback)
commands.add("yf stock symbol", "http://finance.yahoo.com/q?s={}")


# 9-30-10
# 3-31-2020 adds callback and fleshes out this search
def rb_callback(q):
    # NOTE -- ruby urls are case-sensitive (let that sink in), I use title here
    # but it would be better to do things like `String` instead of `string`

    d = {
        "str": "String",
        "strings": "String",

        "arr": "Array",
        "list": "Array",
        "[]": "Array",

        "dict": "Hash",
        "dicts": "Hash",
        "dictionary": "Hash",
        "{}": "Hash",
    }

    if q.lower() in d:
        q = d[q.lower()]

    if q:
        url = "https://ruby-doc.org/core/{}.html".format(q.title())

    else:
        # This has a cool class/function filter at the bottom
        url = "https://ruby-doc.org/core/"

    return url
commands.add("rb rubyc rbc", rb_callback)


# 5-19-2016
def py_callback(q, version="3"):
    d = {
        "set": "https://docs.python.org/{}/library/stdtypes.html#set",
        "iobase": "https://docs.python.org/3/library/io.html#io.IOBase",
        "open2": "https://docs.python.org/3/library/io.html#io.IOBase",
        "file": "https://docs.python.org/3/library/io.html#io.IOBase",
        "file2": "https://docs.python.org/{}/tutorial/inputoutput.html#methods-of-file-objects",
        "open": "https://docs.python.org/{}/library/functions.html#open",
        "mode": "https://docs.python.org/{}/library/functions.html#open",
        "modes": "https://docs.python.org/{}/library/functions.html#open",
        "filemode": "https://docs.python.org/{}/library/functions.html#open",
        "filemodes": "https://docs.python.org/{}/library/functions.html#open",

        "list": "https://docs.python.org/{}/tutorial/datastructures.html#more-on-lists",
        "lists": "https://docs.python.org/{}/tutorial/datastructures.html#more-on-lists",
        "[]": "https://docs.python.org/{}/tutorial/datastructures.html#more-on-lists",
        #"list": "http://infohost.nmt.edu/tcc/help/pubs/python/web/list-methods.html",

        "tuple": "https://docs.python.org/{}/library/functions.html#tuple",
        "tuples": "https://docs.python.org/{}/library/functions.html#tuple",
        "dict": "https://docs.python.org/{}/library/stdtypes.html#dict",
        "dicts": "https://docs.python.org/{}/library/stdtypes.html#dict",
        "{}": "https://docs.python.org/{}/library/stdtypes.html#dict",
        "collections": "https://docs.python.org/{}/library/collections.html#module-collections",
        "format": "https://docs.python.org/{}/library/string.html#formatspec",

        "logformat": "https://docs.python.org/3/library/logging.html#logrecord-attributes",
        "logform": "https://docs.python.org/3/library/logging.html#logrecord-attributes",
        "log": "https://docs.python.org/3/library/logging.html#logrecord-attributes",
        "logging": "https://docs.python.org/3/library/logging.html#logrecord-attributes",
        "logrecord": "https://docs.python.org/3/library/logging.html#logrecord-attributes",

        "functions": "https://docs.python.org/{}/library/functions.html",
        "funcs": "https://docs.python.org/{}/library/functions.html",
        "func": "https://docs.python.org/{}/library/functions.html",
        "builtins": "https://docs.python.org/{}/library/functions.html",
        "builtin": "https://docs.python.org/{}/library/functions.html",

        "date": "https://docs.python.org/{}/library/datetime.html#strftime-strptime-behavior",
        "dateformat": "https://docs.python.org/{}/library/datetime.html#strftime-strptime-behavior",

        "test": "https://docs.python.org/{}/library/unittest.html#unittest.TestCase",
        "testing": "https://docs.python.org/{}/library/unittest.html#unittest.TestCase",
        "assert": "https://docs.python.org/{}/library/unittest.html#unittest.TestCase",
        "asserts": "https://docs.python.org/{}/library/unittest.html#unittest.TestCase",

        "exceptions": "https://docs.python.org/{}/library/exceptions.html",
        "exception": "https://docs.python.org/{}/library/exceptions.html",
        "except": "https://docs.python.org/{}/library/exceptions.html",
        "exc": "https://docs.python.org/{}/library/exceptions.html",
        "error": "https://docs.python.org/{}/library/exceptions.html",
        "err": "https://docs.python.org/{}/library/exceptions.html",
        "errors": "https://docs.python.org/{}/library/exceptions.html",

        "strings": "https://docs.python.org/{}/library/stdtypes.html#string-methods",
        "string2": "https://docs.python.org/{}/library/stdtypes.html#string-methods",
        "str": "https://docs.python.org/{}/library/stdtypes.html#string-methods",
        "byte": "https://docs.python.org/{}/library/stdtypes.html#bytes-methods",
        "bytes": "https://docs.python.org/{}/library/stdtypes.html#bytes-methods",

        "pdb": "https://docs.python.org/{}/library/pdb.html#pdbcommand-commands",

        "code": "https://github.com/python/cpython/tree/master/Lib",
        "code3": "https://github.com/python/cpython/tree/master/Lib",
        "3": "https://github.com/python/cpython/tree/master/Lib",
        "code2": "https://github.com/python/cpython/tree/2.7/Lib",
        "2": "https://github.com/python/cpython/tree/2.7/Lib",

        "env": "https://docs.python.org/3/using/cmdline.html#environment-variables",
        "environ": "https://github.com/python/cpython/tree/2.7/Lib",
        "environment": "https://github.com/python/cpython/tree/2.7/Lib",

        "context": "https://docs.python.org/3/reference/datamodel.html#context-managers",
        "with": "https://docs.python.org/3/reference/datamodel.html#context-managers",
        "__enter": "https://docs.python.org/3/reference/datamodel.html#context-managers",
        "__enter__": "https://docs.python.org/3/reference/datamodel.html#context-managers",
        "__exit": "https://docs.python.org/3/reference/datamodel.html#context-managers",
        "__exit__": "https://docs.python.org/3/reference/datamodel.html#context-managers",

        "magic": "https://docs.python.org/3/reference/datamodel.html#special-method-names",
        "special": "https://docs.python.org/3/reference/datamodel.html#special-method-names",
        "__": "https://docs.python.org/3/reference/datamodel.html#special-method-names",
    }
    q = q.lower()
    if not q:
        q = "code{}".format(version)

    if q in d:
        url = d[q].format(version)

    else:

        bd = {}
        for k, v in inspect.getmembers(builtins):
            bd[k.lower()] = v

        if q in bd:
            v = bd[q]
            if q.lower().endswith("error"):
                url = "{}#{}".format(d["error"], q).format(version)
            else:
                url = "{}#{}".format(d["func"], q).format(version)

        else:
            url = "https://docs.python.org/{}/library/{}.html".format(version, q)

    return url
# added 8-16-08
commands.add("py", py_callback)
# 5-19-2016
def py3_callback(q, version="3"):
    return py_callback(q, version)
commands.add("py3", py3_callback)
# 1-2-2018
def py2_callback(q, version="2"):
    return py_callback(q, version)
commands.add("py2", py2_callback)


# 7-21-2016
# 3-19-2019 I fleshed chef search out more
# 3-31-2020 Updates to latest chef links and fixes search
def chef_callback(q):
    if q:
        q = q.lower()
        if q == "custom":
            url = "https://docs.chef.io/custom_resources.html"

        elif q in set(["common", "prop", "props", "properties"]):
            url = "https://docs.chef.io/resources/#common-functionality"

        else:
            url = "https://docs.chef.io/resources/{}/".format(q.replace(" ", "_").replace("-", "_"))

    else:
        url = "https://docs.chef.io/resources/"

    return url
commands.add("ch chefdoc", chef_callback, "Chef documentation")


# added 10-28-2008...
commands.add("mtv", "http://www.mtvmusic.com/search/?term={}")
commands.add("h", "http://www.hulu.com/videos/search?query={}")
commands.add("gf", "http://finance.google.com/finance?q={}")
# 11-6-08...
commands.add("t tw twit ts", "https://twitter.com/search?q={}&f=tweets&vertical=news")
# 11-19-08...
commands.add("yc syc hn", "https://hn.algolia.com/?query={}&sort=byPopularity&prefix&page=0&dateRange=all&type=story")

commands.add("li", "http://www.lipsum.com/feed/html")
# 12-4-08...
commands.add("new", "http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description={}&x=0&y=0")
commands.add("al alexa", "http://www.alexa.com/data/details/traffic_details/{}")

# 1-9-09...
commands.add("nf ne net", "https://www.netflix.com/search/{}")
# 10-17-12 better netflix search
commands.add("nfi neti", "http://instantwatcher.com/titles?q={}&search_episodes=")

# 1-31-09
commands.add("down", "http://downforeveryoneorjustme.com/{}")
# 11-19-09
commands.add("tviv", "http://tviv.org/w/index.php?search={}&title=Special%3ASearch")
# 8-30-11...
commands.add("camel", "http://camelcamelcamel.com/products?sq={}")
# 1-14-12
commands.add("lds scriptures", "http://lds.org/scriptures/search?lang=eng&query={}&x=0&y=0")
# 2-1-12
def lds_callback(volume, question):
    url = 'http://www.lds.org/scriptures/{}'.format(volume)
    if question:
        bits = question.split(" ", 1)
        book = bits[0] if bits[0] else ''
        chapter = bits[1] if len(bits) > 1 else ''

        if book:
            url += "/{}".format(book)

        if chapter:
            url += "/{}".format(int(chapter))

    return url

def dc_callback(q):
    q = "dc {}".format(q) if q else ""
    return lds_callback('dc-testament', q)
commands.add("dc dandc", dc_callback)
commands.add("bible", lambda q: lds_callback("bible", q))
commands.add("ot", lambda q: lds_callback("ot", q))
commands.add("nt", lambda q: lds_callback("nt", q))
commands.add("bofm bm bom", lambda q: lds_callback("bofm", q))
commands.add("pgp pearl pg pofpg pgop", lambda q: lds_callback("pgp", q))
# 10-15-2017
def jst_callback(q):
    url = "http://www.centerplace.org/hs/iv/"
    return url
commands.add("jst", jst_callback, "The Joseph Smith Translation of the Bible")

# 2-1-2012
#commands.add('sec 10k 10q s1', 'http://www.sec.gov/cgi-bin/browse-edgar?company={}&owner=exclude&Find=Find+Companies&action=getcompany')
commands.add(
    'sec 10k 10q s1',
    'https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany',
    "Search SEC for company stock symbol"
)

# 1-30-13
commands.add('mf msf msnm', 'http://investing.money.msn.com/investments/institutional-ownership?symbol={}')
# 5-18-12
def stw_callback(q):
    return 'http://stocktwits.com/symbol/{}'.format(q.lstrip("$").upper())
commands.add("stocktwits sts stt sk stw", stw_callback)
# 1-31-13
commands.add('rev revere rv', 'https://reports.reveredata.com/reports/store/lookup?q={}&submit=Search')

# 4-3-12
commands.add('app', 'http://appshopper.com/search/?search={}')
# 2-8-13
commands.add('harmonica harm', 'http://www.harptabs.com/searchsong.php?Name={}&Author=&Username=&Difficulty=0&Range=0&HarpType=0')
# 5-25-13
commands.add('fw', 'http://www.fatwallet.com/forums/search/results.php?query={}&type=forums&forum=18&match=titles')

# 6-27-13
commands.add('gip giphy', 'http://giphy.com/tags/{}', 'GIF search engine')
commands.add('gif', 'http://www.google.com/search?q={}&source=lnms&tbm=isch&tbs=itp:animated', 'Google image GIF specific search')
# 9-14-13
# https://news.ycombinator.com/item?id=6296634
def exsh_callback(q):
    bits = re.split("\s+", q, 1)
    cmd = bits[0]
    args = ""
    if len(bits) > 1:
        args = bits[1]
    url = 'http://explainshell.com/explain/{}?args={}'.format(cmd, quote_plus(args))
    return url
commands.add(
    'explain exsh esh explainsh',
    exsh_callback,
    'explainshell.com - write down a command-line to see the help text that matches each argument'
)
# 1-21-2014 (updated 11-28-2018 to use https://www.crunchbase.com/opensearch.xml?version=2)
commands.add(
  'cb',
  'https://www.crunchbase.com/textsearch?q={}',
  'Crunchbase company search'
)

# 5-19-2016
def list_callback(q):
    return url_for("ls", q=q) if q else url_for("ls")
commands.add("bounce", list_callback, "list all the available commands")

# 8-19-2016
commands.add('color', 'http://www.color-hex.com/color/{}', 'Color information about hex color')

# 5-15-2017
commands.add('wb way wayback', 'https://web.archive.org/web/*/{}', 'Wayback machine of Internet archive, pass in full urls')


# 9-29-2017
# https://news.ycombinator.com/item?id=15346541
def punc_callback(q):
    url = "http://www.thepunctuationguide.com/"
    d = {
        ".": "http://www.thepunctuationguide.com/period.html",
        "?": "http://www.thepunctuationguide.com/question-mark.html",
        "!": "http://www.thepunctuationguide.com/exclamation-point.html",
        ",": "http://www.thepunctuationguide.com/comma.html",

        ";": "http://www.thepunctuationguide.com/semicolon.html",
        ":": "http://www.thepunctuationguide.com/colon.html",

        "-": "http://www.thepunctuationguide.com/hyphen.html",
        "--": "http://www.thepunctuationguide.com/en-dash.html",
        "---": "http://www.thepunctuationguide.com/em-dash.html",

        "(": "http://www.thepunctuationguide.com/parentheses.html",
        ")": "http://www.thepunctuationguide.com/parentheses.html",

        "'": "http://www.thepunctuationguide.com/apostrophe.html",
        "\"": "http://www.thepunctuationguide.com/quotation-marks.html",

        "/": "http://www.thepunctuationguide.com/slash.html",

        "<": "http://www.thepunctuationguide.com/angle-brackets.html",
        ">": "http://www.thepunctuationguide.com/angle-brackets.html",

        "{": "http://www.thepunctuationguide.com/braces.html",
        "}": "http://www.thepunctuationguide.com/braces.html",

        "...": "http://www.thepunctuationguide.com/ellipses.html",

        "[": "http://www.thepunctuationguide.com/brackets.html",
        "]": "http://www.thepunctuationguide.com/brackets.html",

    }

    if q in d:
        url = d[q]
    return url
commands.add(
    'punc p pu',
    punc_callback,
    'Punctuation and style guide'
)

# 10-15-2017
commands.add('ip myip', 'https://www.where-am-i.co/my-ip-location', 'My IP Address and current location')

# 11-7-2017
commands.add('dns', 'https://www.whatsmydns.net/?utm_source=whatsmydns.com&utm_medium=redirect#A/{}', 'DNS check for domain (so pass in something like "example.com"')

# 1-2-2018
commands.add('y yelp', 'https://www.yelp.com/search?find_desc=burgers&ns=1', 'Search Yelp listings')
commands.add('ig insta', 'https://www.instagram.com/{}/', 'Redirect to instangram username')
commands.add('gh code', 'https://github.com/search?q={}&type=', 'Search Github repos')

# 6-5-2018
commands.add('mojo', 'https://www.boxofficemojo.com/search/?q={}', 'Search for movies on Box Office Mojo')

# 4-12-2019
def videoeta(q):
    dt = datetime.datetime.utcnow()
    month = dt.month
    year = dt.year
    first_day = 1
    last_day = calendar.monthrange(dt.year, dt.month)[1]

    query_kwargs = {
        "datetype": "videoreleases",
        "start_date": "{:02}/{:02}/{}".format(month, first_day, year),
        "end_date": "{:02}/{:02}/{}".format(month, last_day, year),
        "keywords": "*",
        "ord_by": "box_office",
        "ord_sort": "desc",
        "search_type": "daterange"
    }
    base_url = "https://videoeta.com/search"
    return Url(base_url, **query_kwargs)
commands.add("veta videoeta bluray movies releases videos vids dvd", videoeta, "Get the new video releases for the current month")


# 4-12-2019
def unquote(q):
    return commands.unquote(q)
commands.add("unquote urldecode", unquote, "url decode the input")


# 6-7-2019
commands.add("ikea", 'https://www.ikea.com/us/en/search/?query={}', "Search IKEA")


# 6-20-2019
def tweetthread(q):
    url = q
    m = re.search(r"\/(\d+)(?:\/|\?)?", q)
    if m:
        url = "https://threadreaderapp.com/thread/{}.html?refreshed=yes".format(m.group(1))
    return url
commands.add("thread storm tweetstorm tweetthread", tweetthread, "Convert a tweet storm into easy to read longform")


# 7-9-2019
def unsplash(q):
    q = re.sub(r"\s+", "-", q)
    return "https://unsplash.com/search/photos/{}".format(q)
commands.add("unsplash blogpic", unsplash, "Freely useable images")


# 8-4-2019
commands.add("nin", "https://www.nintendo.com/search/#category=all&page=1&query={}", "Search Nintendo", plus=False)
# 5-7-2020
commands.add("nindeals nind", "https://www.dekudeals.com/search?q={}", "Search Nintendo deals and price history")

# 4-3-2020
commands.add("ps", "https://store.playstation.com/en-us/grid/search-game/1?query={}", "Search Playstation store", plus=False)
# 5-7-2020
commands.add("ps psdeals psd", "https://psprices.com/region-us/search/?q={}&dlc=show", "Search Playstation deals and price history")

# 8-19-2019
def howlong(q):
    # curl -d "queryString=QUERY_STRING&page=1&t=games&sorthead=popular" "https://howlongtobeat.com/search_results.php"
    d = {
        "action": "https://howlongtobeat.com/search_results.php",
        "queryString": q,
        "page": 1,
        "t": "games",
        "sorthead": "popular"
    }
    return d
commands.add("howlong game beat", howlong, "How long to beat the game")


