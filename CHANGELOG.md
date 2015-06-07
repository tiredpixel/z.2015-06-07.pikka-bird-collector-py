# Pikka Bird Collector Changelog

This changelog documents the main changes between released versions.
For a full list of changes, consult the commit history.


## 0.2.0

- added MongoDB collector, supporting core status and replication status

- added MySQL collector, supporting core status, master status, slave status,
  slave hosts, and variables

- added PostgreSQL collector, supporting core status, replication status, and
  settings

- added RabbitMQ collector, supporting core status and cluster status

- added Redis collector, supporting core status and cluster status

- reduced System collector payload size, deducting around 26% when using binary

- added `--conf` support, reading single-file collector configs in JSON and YAML
  formats, or multi-file `conf.d/`-style directories

- made numerous refactorings and test improvements throughout, including
  extending documentation extensively to provide examples of collector payloads


## 0.1.0

- first release! :D

- `pikka-bird-collector` providing commands: `collect`

- `--eternal` mode with automatic staggering

- `--format` supporting JSON and binary payloads

- `system` collector providing metrics: `load`, `cpu`, `memory`, `disk`
