# Pikka Bird Collector (Python)

[![Build Status](https://travis-ci.org/tiredpixel/pikka-bird-collector-py.png?branch=master,stable)](https://travis-ci.org/tiredpixel/pikka-bird-collector-py)

Pikka Bird ops monitoring tool Collector component.

Pikka Bird Collector gathers metrics reports, sending them to
[Pikka Bird Server][server]. Pikka Bird Collector is a [Python][python]
application.

One of the design goals of Pikka Bird is to enable production-suitable setup in
a minimum of steps and configuration. To support this, Pikka Bird Collector will
auto-configure wherever possible, and as many services as possible will be
included within this application, regardless of whether they're installed or
even compatible with the server being monitored.

To minimise dependencies, shelling out and using service executables directly
will be preferred to adding a library dependency (e.g. [PostgreSQL][postgresql]
`psql` to be used instead of using a nice library binding). This will be slower,
and cause juggling with paths and different systems and shells, but will enable
the core dependencies to be kept small whilst allowing the supported services to
grow into the tens or hundreds.

Pikka Bird Collector is designed to gather and send as many metrics as can be
found, even if that leads to large reports, with no concept of success or
failure of individual metrics. Think more like a squirrel gathering nuts in a
forest than asking the server whether it is okay by means of executed checks.
This, at the expense of storage and some speed, does away with problems of
remote execution privileges or installing and maintaining remote checks, as all
interpretive dance occurs in the Server component on a fixed data structure.

Pikka Bird is currently in a draft phase, which means that payloads and schemas
might be changed in a backwards-incompatible fashion. Although it is unlikely,
in extreme cases this could require you to reinstall with an empty database. If
this upsets you too much, please wave and come back later. :) Currently, it is
not recommended that you use Pikka Bird as a replacement for any of your usual
monitoring tools.

More sleep lost by [tiredpixel](https://www.tiredpixel.com/).


## Installation

Install the following externals:

- [Python][python]
  
  The default version supported is defined in `.python-version`. Any other
  versions supported as defined in `.travis.yml`.

- [Pikka Bird Server][server]
  
  Pikka Bird Server collects the metrics Pikka Bird Collector gathers.

Install using [Pip][pip]:

    pip install pikka-bird-collector

There are currently no released server packages (stay tuned).


## Usage

Run [Pikka Bird Server][server].

To run the collector once:

    bin/pikka-bird-collector

To run the collector eternally, staggering to average once per minute:

    bin/pikka-bird-collector -e 60

Help is at hand:

    bin/pikka-bird-collector -h


## Development

Copy the example configuration for development, adjusting to taste:

    cp .env.example .env

Copy the example configuration for testing, adjusting to taste, adding the
environment variable `CI=true` (the tests are destructive to the database):

    cp .env.example .test.env

Install locally using [Pip][pip] editable mode:

    pip install -r requirements.txt
    pip install -e .

Start a collector eternally using [Honcho][honcho], which reads `Procfile`:

    honcho start

Run the tests, which use [py.test][py_test]:

    honcho run -e .test.env py.test


## Stay Tuned

We have a [Librelist][librelist] mailing list!
To subscribe, send an email to <pikka.bird@librelist.com>.
To unsubscribe, send an email to <pikka.bird-unsubscribe@librelist.com>.
There be [archives](http://librelist.com/browser/pikka.bird/).

You can also become a
[watcher](https://github.com/tiredpixel/pikka-bird-collector/watchers)
on GitHub. And don't forget you can become a
[stargazer](https://github.com/tiredpixel/pikka-bird-collector/stargazers)
if you are so minded. :D


## Contributions

Contributions are embraced with much love and affection! <3 Please fork the
repository and wizard your magic, preferably with plenty of fairy-dust sprinkled
over the tests. Then send me a pull request. :) If you're thinking about
working on something involved, it would be great if you could wave via the
issue tracker or mailing list; I'd hate for good effort to be wasted!

Do whatever makes you happy. We'll probably still like you. :)


## Blessing

May you find peace, and help others to do likewise.


## Licence

© [tiredpixel](https://www.tiredpixel.com/) 2015.
It is free software, released under the MIT License, and may be redistributed
under the terms specified in `LICENSE.txt`.


[honcho]: https://github.com/nickstenning/honcho
[librelist]: http://librelist.com/
[pip]: https://pypi.python.org/pypi/pip
[postgresql]: http://www.postgresql.org/
[py_test]: http://pytest.org/latest/
[python]: https://www.python.org/
[server]: https://github.com/tiredpixel/pikka-bird-server-py
