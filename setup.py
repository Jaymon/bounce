#!/usr/bin/env python
# http://docs.python.org/distutils/setupscript.html
# http://docs.python.org/2/distutils/examples.html

from setuptools import setup, find_packages
import re
import os


name = "bounce"
with open(os.path.join(name, "__init__.py"), 'rU') as f:
    version = re.search("^__version__\s*=\s*[\'\"]([^\'\"]+)", f.read(), flags=re.I | re.M).group(1)


setup(
    name=name,
    version=version,
    description='Search using special commands',
    author='Jay Marcyes',
    author_email='jay@marcyes.com',
    url='http://github.com/Jaymon/{}'.format(name),
    packages=find_packages(),
    license="MIT",
    install_requires=['flask'],
    tests_require=['testdata', 'requests'],
    classifiers=[ # https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    entry_points = {
        'console_scripts': [
            'bounce = {}.__main__:console'.format(name),
        ],
    },
    scripts=[
        '{}/bin/bouncefile.py'.format(name),
        '{}/bin/bounce-server'.format(name)
    ],
    #test_suite = "endpoints_test",
)
