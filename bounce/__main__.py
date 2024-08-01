# -*- coding: utf-8 -*-
import os
import sys
import argparse
import subprocess

from endpoints.interface.wsgi import Application, Server
from datatypes import logging, Host

from bounce import commands, __version__, import_config


def app_serve(args):
    """bounce serve subcommand

    start a local bounce server
    """
    kwargs = {
        "server_address": args.host,
        "application": Application("bounce.controllers")
    }

    with Server(**kwargs) as s:
        s.serve_forever()

    return 0


def app_q(args):
    """bounce q subcommand

    Answer the passed in question
    """
    code = 0

    q = " ".join(args.qs)
    url = commands.find(q)
    if callable(url):
        url = url(q)

    print(url)

    if args.redirect:
        code = subprocess.call(["open", url])

    return code


def application():
    """bounce command

    This is the main hook to run bounce commands
    """
    logging.quick_config(stream=sys.stderr)

    parser = argparse.ArgumentParser(description='Bounce')
    parser.add_argument(
        "-V", "--version",
        action='version',
        version="%(prog)s {}".format(__version__)
    )

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        '--config', '-c',
        dest="configs",
        action="append",
        #default=[],
        help='a custom configuration module'
    )

    subparsers = parser.add_subparsers(dest="command", help="a sub command")

    # $ bounce q
    desc = "Answer the passed in question"
    subparser = subparsers.add_parser(
        "q",
        parents=[common_parser],
        help=desc,
        description=desc,
        conflict_handler="resolve",
    )
    subparser.add_argument(
        'qs',
        metavar='Q',
        nargs='*',
        default=[],
        help='the search string'
    )
    subparser.add_argument(
        "--redirect", "-r",
        action="store_true",
        help='Do not just print the url but redirect also'
    )
    subparser.set_defaults(func=app_q)

    # $ bounce serve
    desc = "Run a bounce server"
    subparser = subparsers.add_parser(
        "serve",
        parents=[common_parser],
        help=desc,
        description=desc,
        conflict_handler="resolve",
    )
    subparser.add_argument(
        "--host", "-H",
        default="localhost",
        type=Host,
        help="The host to serve on in the form host:port"
    )
    subparser.set_defaults(func=app_serve)

    args = parser.parse_args()

    if args.configs:
        for config in args.configs:
            import_config(config)

    return args.func(args)


if __name__ == "__main__":
    sys.exit(application())

