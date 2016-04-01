import os

from .core import commands
from . import config
from server import app as server


__version__ = "0.1.1"


def import_configs(name='BOUNCE_CONFIG'):
    if name in os.environ:
        import_config(os.environ[name])

    increment_name = lambda name, num: '{}_{}'.format(name, num)
    num = 1
    name_num = increment_name(name, num)
    try:
        while True:
            import_config(os.environ[name_num])
            num += 1
            name_num = increment_name(name, num)

    except KeyError:
        pass


def import_config(config_module_path):
    # not 3+ compatible
    # http://stackoverflow.com/questions/6357361/alternative-to-execfile-in-python-3
    execfile(config_module_path)


# actually import any environment set configs
import_configs()

