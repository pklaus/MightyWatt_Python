#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Python package with a web interface for the MightyWatt,
a great programmable electronic load for the Arduino Uno/Due.
"""

from setuptools import setup

setup(
    name = 'MightyWatt',
    author = 'Philipp Klaus',
    author_email = 'philipp.l.klaus@web.de',
    url = "http://github.com/pklaus/MightyWatt_Python/",
    version = '0.7',
    description = __doc__,
    long_description = __doc__,
    license = 'GPL',
    packages = ['mightywatt'],
    scripts = ['mightywatt/webapp/mw_web_server','scripts/mw_web_client','scripts/mw_shell',],
    include_package_data = True,
    #package_data = {
    #    'mightywatt': ['webapp/static/*'],
    #    'mightywatt': ['webapp/views/*'],
    #},
    install_requires = [
        'Bottle>=0.12',
        'pySerial>=2.6',
    ],
    keywords = 'MightyWatt Electronic Load web interface',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering',
    ]
)

