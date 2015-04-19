import os
if os.environ.get('CI') != 'true':
    exit("!!! CI environment variable must be set for testing environment")

import pytest


@pytest.fixture
def collection_valid():
    return {
        'collected_at':  '2015-04-04T19:32:20.616977',
        'collecting_at': '2015-04-04T19:33:01.424242',
        'environment':   {
            'hostname': 'localhost',
            'pid':      42,
            'version':  '1.2.3',
            'platform': {
                'system':  "Hovercraft",
                'release': "42.21.11",
                'version': "Hovercraft Kernel Version 42.21.11 128-bit"}},
        'reports': {
            'system': {
                'load': {
                    'avg_15_min': 1.62939453125}}}}
