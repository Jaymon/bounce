import re
import urllib

from .core import commands


commands.add("g google", "http://www.google.com/search?q={}", default=True) # google
commands.add("gm googlemap", "http://maps.google.com/?q={}") # google maps
commands.add("goopat gp googlepatent googlepatents", "http://www.google.com/patents?btnG=Search+Patents&q={}")
commands.add("gi", "http://images.google.com/images?um=1&ie=UTF-8&sa=N&tab=wi&q={}")
# 9-29-11
commands.add("gt translate trans", "http://translate.google.com/translate?hl=en&sl=auto&tl=en&u={}")

commands.add("d dict dic dictionary", "http://www.dictionary.com/browse/{}") # dictionary
commands.add("pb", "http://thepiratebay.org/search.php?q={}") # pirate bay torrent
commands.add("wk", "http://en.wikipedia.org/wiki/Special:Search?fulltext=Search&search={}")
commands.add("wpg wkg wikigoogle", "http://www.google.com/custom?domains=en.wikipedia.org&sitesearch=en.wikipedia.org&q={}")
commands.add("tv", "http://www.tv.com/search.php?type=11&stype=all&tag=search%3Bbutton&qs={}")
commands.add("y yhoo", "http://search.yahoo.com/bin/search?p={}")
commands.add("am amazon amaz a", "http://www.amazon.com/s/ref=nb_ss_gw/102-5754341-9464967?url=search-alias%3Daps&Go=Go&field-keywords={}")
commands.add("msn", "http://search.msn.com/results.aspx?q={}")
commands.add("epg ep epguides eg", "http://www.google.com/search?hl=en&q=allintitle%3A&q=site%3Aepguides.com&btnG=Search&q={}")
commands.add("yt", "http://www.youtube.com/results?search=Search&search_query={}")

# 8-8-12
def ytnsfw_callback(q):
    # allows watching youtube nsfw vidoes without logging in
    url = q
    m = re.match("/v=([^&]+)/", q)
    if m:
        url = 'http://deturl.com/play.asp?v={}'.format(m.group(1))
    return url
commands.add("yti ty yta ytnsfw", ytnsfw_callback)

commands.add("imdb", "http://www.imdb.com/find?s=all&q={}")
commands.add("bmn bug bugmenot", "http://www.bugmenot.com/view/{}")
commands.add("wks wikiseek", "http://www.wikiseek.com/results.php?q={}")
commands.add("godaddy godad gd", "http://www.godaddy.com/gdshop/registrar/search.asp?isc=ffsearch&checkavail=1&domaintocheck={}")
commands.add("ws websnif websniff", "http://web-sniffer.net/?submit=Submit&http=1.1&gzip=yes&type=GET&url={}")
commands.add("ebay eb", "http://search.ebay.com/search/search.dll?from=R40&category0=&satitle={}")
# added 1-6-08...
commands.add("php", "http://us2.php.net/{}")
commands.add("yf stock symbol", "http://finance.yahoo.com/q?s={}")
# added 8-16-08
commands.add("pydoc py p", "http://docs.python.org/library/{}.html")
# added 10-28-8...
commands.add("mtv", "http://www.mtvmusic.com/search/?term={}")
commands.add("hulu h", "http://www.hulu.com/videos/search?query={}")
commands.add("gf", "http://finance.google.com/finance?q={}")
# 11-6-08...
commands.add("t tw twit ts", "https://twitter.com/search?q={}&src=tyah")
# 11-19-08...
commands.add("yc syc hn", "http://searchyc.com/{}")
commands.add("li", "http://www.lipsum.com/feed/html")
# 12-4-08...
commands.add("ne", "http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description={}&x=0&y=0")
commands.add("al alexa", "http://www.alexa.com/data/details/traffic_details/{}")

# 1-9-09...
commands.add("nf netflix net", "http://www.netflix.com/Search?lnkce=iwsceOf&v1={}&lnkce=acsNoEnhRt")
# 10-17-12 better netflix search
commands.add("nfi neti", "http://instantwatcher.com/titles?q={}&search_episodes=")

# 1-31-09
commands.add("down", "http://downforeveryoneorjustme.com/{}")
# 11-13-09
commands.add("nw ninja", "http://ninjawords.com/?q={}")
# 11-19-09
commands.add("tviv", "http://tviv.org/w/index.php?search={}&title=Special%3ASearch")
# 9-30-10
commands.add("rubyc rbc", "http://www.ruby-doc.org/core/classes/{}.html")
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
        chapter = bits[1] if bits[1] else ''

        if book:
            url += "/{}".format(book)

        if chapter:
            url += "/{}".format(int(chapter))

    return url

def dc_callback(q):
    q = "dc {}".format(q) if q else "dc"
    return lds_callback('dc-testament', q)
commands.add("dc dandc", dc_callback)
commands.add("bible", lambda q: lds_callback("bible", q))
commands.add("ot", lambda q: lds_callback("ot", q))
commands.add("nt", lambda q: lds_callback("nt", q))
commands.add("bofm bm bom", lambda q: lds_callback("bofm", q))
commands.add("pgp pearl pg", lambda q: lds_callback("pgp", q))

# 2-1-2012
commands.add('sec 10k 10q s1', 'http://www.sec.gov/cgi-bin/browse-edgar?company={}&owner=exclude&Find=Find+Companies&action=getcompany')
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
    url = 'http://explainshell.com/explain/{}?args={}'.format(cmd, urllib.quote_plus(args))
    return url
commands.add(
    'explain exsh esh explainsh',
    exsh_callback,
    'explainshell.com - write down a command-line to see the help text that matches each argument'
)
# 1-21-2014
commands.add(
  'cb',
  'http://www.crunchbase.com/search?query={}',
  'Crunchbase company search'
)

