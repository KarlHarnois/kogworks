# Kogworks

Kogworks is a Knave 0.22.0 project. The factory definition is `.kogworks/factory.knv`, and `kogworks synth .kogworks` writes `.kogworks/factory.json` from it.

## Controller

`kogworks controller --repo <path>` polls rmap for the governed repository and starts the worker for the first startable build. It reads `.kogworks/factory.json` for the roadmap, manager, worker role and brief, and fills the brief's base from the repository's default branch. It runs no model call and keeps no memory between passes.

The controller exits 1 on the first failure and starts nothing else. A person reads the manager message and restarts it. It has no automatic restart, supervisor or backoff loop.

The controller can merge pull requests that change the controller itself. The running binary stays at the version it was built from, and a person rebuilds and restarts it after such a merge.

Do not run the controller on a live roadmap until `rm-b204` and `rm-874e` merge.
