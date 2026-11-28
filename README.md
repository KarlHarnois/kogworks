# Kogworks

Kogworks is a Knave 0.22.0 project. It synthesizes a factory file and runs a controller that advances a roadmap through rmap, ringleader and GitHub.

`knave build` builds the binary at `./target/knave/kogworks/kogworks`. The commands below run that binary by its path.

## Factory layout

| Path | Contents |
| --- | --- |
| `.kogworks/factory.knv` | The factory definition. It holds one `deffactory` form that names the manager, roadmap, `max_active`, merge method and the worker and reviewer roles. |
| `.kogworks/factory.json` | The committed factory output. The controller reads this file. |
| `.kogworks/briefs/` | The worker and reviewer briefs that the roles name, such as `worker.md` and `reviewer.md`. A brief path is relative to the repository. |

`./target/knave/kogworks/kogworks synth <dir>` reads `<dir>/factory.knv` and writes `<dir>/factory.json`. For this repository, run `./target/knave/kogworks/kogworks synth .kogworks`. Never edit `.kogworks/factory.json` by hand: the gate fails when the output differs from the definition.

## Controller

Run `./target/knave/kogworks/kogworks controller --repo <path>`. For `--repo <path>`, the controller reads `<path>/.kogworks/factory.json` for the roadmap, manager, merge method and roles. Each pass handles one action. It starts a reviewer for a review or verify action, or merges an approved pull request. With no such action, it starts the worker for the first startable build from `rmap ready`. The base branch is the default branch of the repository at `<path>`. The controller runs no model call and keeps no memory between passes. It needs `rmap`, `ringleader`, `gh` and `git` on `PATH`; each dispatch and review runs `git symbolic-ref` to read the default branch.

`--poll <seconds>` sets the interval between passes (default 30). `--merge-poll <seconds>` sets the merge poll interval. `--merge-timeout <seconds>` sets the merge timeout (default 3600). `--once` runs one pass and exits.

The controller stops on the first failure. It sends the manager one message and exits 1. A person reads the message, fixes the cause, and restarts the controller with the same command. The controller has no automatic restart, supervisor or backoff loop.

The controller can merge pull requests that change the controller. The running binary stays at the version it was built from. After such a merge, a person rebuilds with `knave build` and restarts the controller.

## Gate

Run the gate in [`AGENTS.md`](AGENTS.md) before you push. If a command fails, fix the cause and rerun it at most twice. If it still fails, stop.

The `Kogworks` workflow runs the gate on every push and pull request.

## GitHub settings

For KarlHarnois/kogworks, enable auto-merge and protect `main` with the `check` status from the `Knave` workflow as a required status check. The merge action checks that auto-merge is enabled and that `main` has at least one required status check. It exits 1 without merging when either check fails. The controller never changes repository settings.
