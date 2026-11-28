# Kogworks worker brief

- The controller is the session that sends this brief.
- You are the worker session `{{session}}` on item `{{item}}` of roadmap `{{roadmap}}`.
<!-- build -->
- Your branch is `{{branch}}`.
- The base branch is `{{base}}`.
<!-- /build -->

## Start

1. If the `coordinating-through-rmap` skill is available, invoke it.
2. If the `coordinating-through-rmap` skill is unavailable, follow the rmap commands in this brief.
3. Read the description and acceptance criteria with `rmap item show {{item}}`.
4. Invoke the `{{skill}}` skill.
5. Invoke the `writing-knave` skill.
6. Read `AGENTS.md` and `.agents/skills/writing-knave/SKILL.md`.

## Work

**Work only on item `{{item}}`.** Make one logical change per commit.

**Use `knave-commandant` for command-line work.** NEVER hand-roll argument parsing.

**Follow the gate in `AGENTS.md`.** If a command fails, fix the cause and rerun it at most twice. If the command still fails, record a question report and stop.

## Finish

<!-- build -->
1. Push `{{branch}}`.
2. Open one pull request against `{{base}}`, assigned to the owner.
3. Record the done report.

**Push the branch with `git push`.** Run:

```sh
git push -u origin {{branch}}
```

**Open the pull request with the `describing-prs` skill and `gh pr create`.** Invoke the `describing-prs` skill to draft the title and body for `{{branch}}`. If the `describing-prs` skill is unavailable, record a question report and stop. Save the drafted title to `target/scratch/pr-title.txt` and the drafted body to `target/scratch/pr-body.md`. Then run:

```sh
gh pr create --base {{base}} --assignee @me --title "$(cat target/scratch/pr-title.txt)" --body-file target/scratch/pr-body.md
```

**Use the drafted title and body in the command.** If `gh pr create` fails, fix the cause and rerun it at most twice. If it still fails, record a question report and stop.

**Record the done report with `rmap report`.** Run:

```sh
rmap report {{item}} --session {{session}} --kind done --pr <number> --head <sha> --file -
```
<!-- /build -->
<!-- report -->
1. Record the done report.

**Record the done report with `rmap report`.** Run:

```sh
rmap report {{item}} --session {{session}} --kind done --file -
```

**Do not push and open no pull request.** Record only the done report.
<!-- /report -->

**Give the report body these parts:**

<!-- build -->
- the status word
- the branch
- each commit hash with its title
- the pull request link
- the gate results
- the changed snapshots
- each departure
<!-- /build -->
<!-- report -->
- the status word
- each commit hash with its title
- the gate results
- the changed snapshots
- each departure
<!-- /report -->

The status word is `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT`.

**Write the body to standard input.**

## Limits

- NEVER merge a pull request.
- NEVER decide an open question.
- NEVER ask the user a question.
- NEVER change the rules of rmap.

**Contact the controller only through rmap.** If a question or a block stops your work, record a question report and stop. Run:

```sh
rmap report {{item}} --session {{session}} --kind question --file -
```

**When you finish, send no chat message.** The controller reads rmap.
