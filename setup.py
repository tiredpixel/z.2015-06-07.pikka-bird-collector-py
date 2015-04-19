#!/usr/bin/env python

from setuptools import setup, find_packages

import pikka_bird_collector


setup(
    name     = 'pikka-bird-collector',
    version  = pikka_bird_collector.__version__,
    packages = find_packages(),
    scripts  = ['bin/pikka-bird-collector'],
    
    author       = 'tiredpixel',
    author_email = 'tp@tiredpixel.com',
    description  = "Pikka Bird ops monitoring tool Collector component.",
    license      = 'MIT',
    keywords     = 'monitoring',
    url          = 'https://github.com/tiredpixel/pikka-bird-collector-py',
    
    install_requires = [
    ]
)
