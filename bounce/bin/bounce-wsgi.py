#!/usr/bin/env python

from endpoints.interface.wsgi import Application

application = Application("bounce.controllers")

