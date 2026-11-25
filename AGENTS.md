# Kogworks

Kogworks is a Knave 0.22.0 project. Read `.agents/skills/writing-knave/SKILL.md` before you write Knave.

## Factory

The factory definition is `.kogworks/factory.knv`. The committed output is `.kogworks/factory.json`. `kogworks synth .kogworks` writes the output from the definition. NEVER edit `.kogworks/factory.json` by hand: the gate fails when the output differs from the definition.

`.kogworks/factory.knv` is outside `src/`. It imports the `kogworks` path library, which is this repository, so the explicit file commands below resolve its modules.

## Gate

Run every command before you push. If a command fails, fix the cause and rerun the command, at most twice. If the command still fails, stop and ask the user.

```sh
knave check
knave fmt --check
knave fmt --check .kogworks/factory.knv
knave lint
knave lint .kogworks/factory.knv
knave check .kogworks/factory.knv
knave build
knave test
./target/knave/kogworks/kogworks synth .kogworks
git diff --exit-code .kogworks/factory.json
```

`knave check`, `knave fmt` and `knave lint` do not reach `.kogworks` on their own, so the gate names `.kogworks/factory.knv` in its own format, lint and check commands.
