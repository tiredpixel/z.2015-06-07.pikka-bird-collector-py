import os
if os.environ.get('CI') != '1':
    exit("!!! CI environment variable must be set for testing environment")
