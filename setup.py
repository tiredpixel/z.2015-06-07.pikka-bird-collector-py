#!/usr/bin/env python

from setuptools import setup, find_packages

import pikka_bird_collector


setup(
    name     = 'pikka-bird-collector',
    version  = pikka_bird_collector.__version__,
    
    include_package_data = True,
    packages             = find_packages(),
    scripts              = [
        'bin/pikka-bird-collector'],
    
    author       = 'tiredpixel',
    author_email = 'tp@tiredpixel.com',
    classifiers  = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    description  = "Pikka Bird ops monitoring tool Collector component.",
    keywords     = 'ops monitoring sysadmin',
    license      = 'MIT',
    url          = 'https://github.com/tiredpixel/pikka-bird-collector-py',
    
    install_requires = [
        'msgpack-python',
        'psutil',
        'requests',
    ]
)
