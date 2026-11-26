# Kogworks

Kogworks is a Knave 0.22.0 project. Read `.agents/skills/writing-knave/SKILL.md` before you write Knave.

## Factory

The factory definition is `.kogworks/factory.knv`. It holds only one `deffactory` form. The committed output is `.kogworks/factory.json`. `kogworks synth .kogworks` writes the output from the definition. NEVER edit `.kogworks/factory.json` by hand: the gate fails when the output differs from the definition.

`.kogworks/factory.knv` is outside `src/`. `kogworks synth` and `kogworks module` supply the `kogworks` library import, which is this repository, so the generated module resolves its modules. The import shares the factory form's first line so diagnostics keep the factory file's line numbers. `kogworks format` writes the same form with the import on its own line so the formatter reads the factory's header shape.

## Gate

Run every command before you push. If a command fails, fix the cause and rerun the command, at most twice. If the command still fails, stop and ask the user.

```sh
knave check
knave fmt --check
knave lint
knave build
./target/knave/kogworks/kogworks module .kogworks > target/factory-module.knv
knave lint target/factory-module.knv
knave check target/factory-module.knv
./target/knave/kogworks/kogworks format .kogworks > target/factory-format.knv
knave fmt --check target/factory-format.knv
knave test
./target/knave/kogworks/kogworks synth .kogworks
git diff --exit-code .kogworks/factory.json
```

`knave check`, `knave fmt` and `knave lint` do not reach `.kogworks` on their own, and the factory file alone cannot resolve `deffactory`. The gate formats `target/factory-format.knv`, which puts the library import on its own line so the formatter sees `deffactory`, then lints and checks `target/factory-module.knv`, the module that `kogworks synth` evaluates.
