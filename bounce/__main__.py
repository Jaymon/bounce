import sys
import argparse
import subprocess


#sys.path.insert(0, "/Users/jaymon/Projects/bounce/_bounce")
sys.path.insert(0, "")


from bounce import commands, server, __version__, import_config


# def api():
#     server.debug = True
#     server.run()


def console():
    parser = argparse.ArgumentParser(description='Bounce')
    parser.add_argument('qs', metavar='Q', nargs='*', default=[], help='the search string')
    parser.add_argument('--config', '-c', dest="config", default="", help='a custom configuration module')
    parser.add_argument("-V", "--version", action='version', version="%(prog)s {}".format(__version__))
    parser.add_argument("-p", "--print-only", dest="print_only", action="store_true", help='Just print url, do not redirect')
    args = parser.parse_args()

    if args.config:
        import_config(args.config)

    q = " ".join(args.qs)
    url = commands.find(q)
    print url
    if not args.print_only:
        subprocess.call(["open", url])


sys.exit(console())
#sys.exit(api())

