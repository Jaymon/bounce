# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import os
import logging

from .compat import *
from .core import commands
from . import config
from .server import app as server


__version__ = "0.2.4"


logger = logging.getLogger(__name__)
logging.getLogger(__name__).addHandler(logging.NullHandler())


def import_configs(name='BOUNCE_CONFIG'):
    if name in os.environ:
        logger.info("Imported {} = {}".format(name, os.environ[name]))
        import_config(os.environ[name])

    increment_name = lambda name, num: '{}_{}'.format(name, num)
    num = 1
    name_num = increment_name(name, num)
    try:
        while True:
            import_config(os.environ[name_num])
            logger.info("Imported {} = {}".format(name_num, os.environ[name_num]))
            num += 1
            name_num = increment_name(name, num)

    except KeyError:
        pass


def import_config(config_module_path):
    # not 3+ compatible
    # http://stackoverflow.com/questions/6357361/alternative-to-execfile-in-python-3
    config_module_path = os.path.abspath(os.path.expanduser(str(config_module_path)))
    execfile(config_module_path)


# actually import any environment set configs
import_configs()

