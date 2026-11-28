# Kogworks

Kogworks synthesizes a factory file for a repository. Its controller advances the roadmap of that repository through rmap, ringleader and GitHub.

## Install

TBD

## Usage

```text
Factory.

Usage: kogworks [OPTIONS] <COMMAND>

Commands:
  synth       Writes <dir>/factory.json.
  check       Checks <dir>/factory.knv without writing <dir>/factory.json.
  controller  Runs the controller loop against a governed repository. At start
              it sets the roadmap's max active to the factory's max_active,
              once. It polls rmap and starts the worker for the first startable
              item, whatever its kind, and starts one behavior reviewer when
              rmap marks a build for review or verify. It sends the manager one
              notice for each action that waits on the manager or the user, and
              sends it again after each --stall seconds while the action still
              waits. It exits 1 on the first failure. A person reads the manager
              message and restarts it. The controller can merge pull requests
              that change the controller itself; the running binary stays at the
              version it was built from, and a person rebuilds and restarts it
              after such a merge. It has no automatic restart, supervisor or
              backoff loop. The pilot pins rmap to a build that predates the
              design approval requirement, so a behavior approve alone merges
              and the controller starts no design reviewer.
  apply       Sets a governed repository's roadmap max active from its factory.
  help        Print the help of a command

Options:
  -h, --help  Print help
```
