#!/usr/bin/env python

from endpoints.interface.wsgi import Application

application = Application("bounce.controllers")


# import os
# import sys
# import logging
# 
# logging.basicConfig(format="%(message)s", level=logging.DEBUG, stream=sys.stdout)
# 
# from bounce import server as application

