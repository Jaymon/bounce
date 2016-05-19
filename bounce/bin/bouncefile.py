#!/usr/bin/env python

import os
import logging

logging.basicConfig(format="%(message)s", level=logging.DEBUG, stream=sys.stdout)

from bounce import server as application

