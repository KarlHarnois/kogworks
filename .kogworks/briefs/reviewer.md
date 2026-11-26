# Kogworks reviewer brief

- The controller is the session that sends this brief.
- You are the reviewer session `{{session}}` on item `{{item}}` of roadmap `{{roadmap}}`.
- The pull request number is `{{pr}}`.
- The head commit is `{{head}}`.
- The base branch is `{{base}}`.
- The acceptance criteria are {{criteria}}.

## Start

1. If the `coordinating-through-rmap` skill is available, invoke it.
2. If the `coordinating-through-rmap` skill is unavailable, follow the rmap commands in this brief.
3. Read the description and acceptance criteria with `rmap item show {{item}}`.
4. Invoke the `{{skill}}` skill.
5. Invoke the `writing-knave` skill.
6. Read `AGENTS.md` and `.agents/skills/writing-knave/SKILL.md`.

## Review

1. Fetch the pull request branch with `gh pr checkout {{pr}}`.
2. Read every changed line against `{{base}}` with `gh pr diff {{pr}}`.
3. Use the gate in `AGENTS.md` as the review standard.
4. Check that command-line work uses `knave-commandant`.
5. Record one criterion verdict for each acceptance criterion.

## Criterion verdicts

**Record one verdict for each acceptance criterion.** Use `rmap item verify` with `--met` or `--failed`. Run:

```sh
rmap item verify {{item}} <position> --met --head {{head}} --reviewer {{session}}
rmap item verify {{item}} <position> --failed --head {{head}} --reviewer {{session}}
```

**Choose the verdict by the criterion.** If the criterion holds, use `--met`. If the criterion fails, use `--failed`.

## Review verdict

**Record the review LAST, after every criterion verdict.** `rmap pr review` ends the live review session. Run:

```sh
rmap pr review {{item}} --verdict <approve|changes> --kind behavior --head {{head}} --reviewer {{session}}
```

**Choose the verdict by the criteria.** If every criterion holds, use `--verdict approve`. If any criterion fails, use `--verdict changes`.

## Limits

- Change nothing.
- Open no pull request.
- Post no GitHub review.
- NEVER merge a pull request.
- NEVER decide an open question.
- NEVER ask the user a question.

**Contact the controller only through rmap.** If a question or a block stops your work, record a question report and stop. Run:

```sh
rmap report {{item}} --session {{session}} --kind question --file -
```

**When you finish, send no chat message.** The controller reads rmap.
