# -*- coding: utf-8 -*-
import os
import logging
import runpy

from datatypes import Environ

from .config import commands
from . import config


__version__ = "0.6.1"


logger = logging.getLogger(__name__)


def import_environ_configs(name='BOUNCE_CONFIG'):
    environ = Environ()
    for path in environ.paths(name):
        import_config(path)


def import_config(config_module_path):
    config_module_path = os.path.abspath(
        os.path.expanduser(
            str(config_module_path)
        )
    )

    runpy.run_path(config_module_path)
    logger.info(f"Imported {config_module_path}")


# actually import any environment set configs
import_environ_configs()

