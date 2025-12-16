# -*- coding: utf-8 -*-
"""
This contains the configuration object that should be used to customize

To customize, create a `bounce_config.py` file and import the `commands`:

:example:
    from bounce import commands

    commands.add(
        "<KEYWORD>[ <KEYWORD>...]",
        "<SEARCH-URL>",
        "<DESCRIPTION>",
    )

As many keywords as you want can be added, if you use the same keyword in a
later `.add` call it will override the previous one.

This file contains a couple of "default" keywords to show how they are added
"""

from .core import Commands, Url


commands = Commands()

commands.add(
    "g",
    "http://www.google.com/search?q={}",
    "Google search",
    default=True, # a non-keyword search will default to this
)
commands.add(
    "gm",
    "http://maps.google.com/?q={}",
    "Google maps search",
)
commands.add(
    "wk",
    "http://en.wikipedia.org/wiki/Special:Search?fulltext=Search&search={}",
    "Wikipedia search",
)

commands.add(
    "ddg",
    "https://duckduckgo.com/?q={}&ia=web",
    "DuckDuckGo search",
)

def yt_callback(q):
    # updated to just go to homescreen on 1-21-2021
    if q:
        url = "http://www.youtube.com/results?search=Search&search_query={}".format(q)

    else:
        url = "http://www.youtube.com/"

    return url
commands.add(
    "yt",
    yt_callback,
    "Youtube search",
)

# 5-19-2016
def list_callback(q):
    if q:
        ret = Url(path="/list", query_kwargs={"q": q})

    else:
        ret = Url(path="/list")

    return ret
commands.add(
    "bounce list ls",
    list_callback,
    "List all the available commands/keywords",
)

