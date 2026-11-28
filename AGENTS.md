# Kogworks

Kogworks is a Knave 0.22.0 project. Read `.agents/skills/writing-knave/SKILL.md` before you write Knave.

## Factory

The factory definition is `.kogworks/factory.knv`. It holds only one `deffactory` form. The committed output is `.kogworks/factory.json`. `kogworks synth .kogworks` writes the output from the definition. NEVER edit `.kogworks/factory.json` by hand: the gate fails when the output differs from the definition.

`.kogworks/factory.knv` is outside `src/`. `kogworks synth` supplies the `kogworks` library import, which is this repository, so the generated module resolves its modules. `kogworks check` generates both import layouts in a temporary directory and runs the gate commands on them without writing to the repository.

## Gate

Run every command before you push. If a command fails, fix the cause and rerun the command, at most twice. If the command still fails, stop and ask the user.

```sh
knave check
knave fmt --check
knave lint
knave build
knave task sync-readme-help
knave task ledelint
./target/knave/kogworks/kogworks check .kogworks
knave test
```

`knave check`, `knave fmt` and `knave lint` do not reach `.kogworks` on their own, and the factory file alone cannot resolve `deffactory`. `kogworks check .kogworks` writes the two import layouts to a temporary directory outside the repository, lints, checks and format-checks them there, then evaluates the factory and fails when the committed `.kogworks/factory.json` is stale. It writes nothing to the repository and removes the temporary directory on success or failure.

**After `knave build`, `knave task sync-readme-help` rewrites the Usage section of `README.md` from `kogworks --help`.** If the task changes `README.md`, commit `README.md` with your change. NEVER edit the Usage section by hand: the `Kogworks` workflow fails when the section differs from the help output.
