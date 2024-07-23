#!/usr/bin/env python

from endpoints.interface.asgi import Application

application = Application("bounce.controllers")

