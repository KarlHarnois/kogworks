# Kogworks reviewer brief

- The controller is the manager session `{{manager}}` that sends this brief.
- You are the reviewer session `{{session}}` on item `{{item}}` of roadmap `{{roadmap}}`.
- The pull request number is `{{pr}}`.
- The head commit is `{{head}}`.
- The base branch is `{{base}}`.
- The acceptance criteria are {{criteria}}.

## Start

1. Invoke the `{{skill}}` skill first.
2. If the `coordinating-through-rmap` skill is available, invoke it.
3. If the `coordinating-through-rmap` skill is unavailable, follow the rmap commands in this brief.
4. Read the description and acceptance criteria with `rmap item show {{item}}`.
5. Invoke the `writing-knave` skill.
6. Invoke the `writing-clean-code` skill.
7. Read `AGENTS.md` and `.agents/skills/writing-knave/SKILL.md`.

## Review

The worktree is already at the pull request head.

1. Fetch the base and the pull request head with `git fetch origin`.
2. Read every changed line with `git diff origin/{{base}}...HEAD`.
3. Use the gate in `AGENTS.md` as the review standard.
4. Review the behavior against the acceptance criteria.
5. Review the design with the `{{skill}}` skill, the `writing-clean-code` principles, and the `writing-knave` design principles.
6. Check that command-line work uses `knave-commandant`.
7. Record one criterion verdict for each acceptance criterion.

## Criterion verdicts

**Record one verdict for each acceptance criterion.** Use `rmap item verify` with `--met` or `--failed`. Run:

```sh
rmap item verify {{item}} <position> --met --head {{head}} --reviewer {{session}} --note '<evidence>'
rmap item verify {{item}} <position> --failed --head {{head}} --reviewer {{session}} --note '<evidence>'
```

**Choose the verdict by the criterion.** If the criterion holds, use `--met`. If the criterion fails, use `--failed`.

## Findings

**A real problem is any of these:**
- a bug
- a regression
- a security issue
- the pull request not delivering its claim
- a broken repository rule
- a wrong test or no test for a criterion

**A nitpick is a style, wording or naming issue that does not break the work.** A nitpick does not force the verdict `changes`. When only nitpicks remain, record the verdict `approve` and list the nitpicks in one `ringleader send {{manager}}` message.

**A finding about code the pull request did not touch is a follow-up suggestion.** Send the follow-up suggestion to the manager with one `ringleader send {{manager}}` before the review verdict. A follow-up suggestion does not change the verdict. If `ringleader send` exits nonzero, retry it once. If it still fails, re-run the last criterion verdict with the same `--met` or `--failed`. Put the findings and the send failure in the re-run's `--note`. Record the review verdict either way.

**Anything that makes the code or the brief under review not work as intended is blocking.** A blocking finding stands even when no acceptance criterion names it. NEVER notice a defect and approve anyway.

**Record in rmap every finding that forces the verdict `changes`, before you record the review verdict.** The manager reads these findings only from rmap.

- If the finding makes an acceptance criterion fail, record that criterion as `--failed`. State the finding in the `--note` of that criterion.
- Otherwise, state the finding in the `--note` of the last acceptance criterion, in a sentence that starts with `BLOCKING:`. Keep the verdict that the evidence for that criterion gives.

**If the criterion already has a verdict, run `rmap item verify` for that criterion again with the whole note.** The latest verdict on a criterion counts.

## Review verdict

**Record the review LAST, after every criterion verdict.** `rmap pr review` ends the live review session. Run:

```sh
rmap pr review {{item}} --verdict <approve|changes> --kind behavior --head {{head}} --reviewer {{session}}
```

**Choose the verdict by the criteria and the findings.** If every criterion holds and no real problem or blocking finding stands, use `--verdict approve`. If any criterion fails, or a real problem or blocking finding stands, use `--verdict changes`.

## Limits

- Change nothing.
- Open no pull request.
- Post no GitHub review.
- NEVER merge a pull request.
- NEVER switch branches.
- NEVER decide an open question.
- NEVER ask the user a question.

**Contact the manager with one `ringleader send {{manager}}` for a question or a block.** Send one message and stop. If `ringleader send` exits nonzero, retry it once. If it still fails, stop.

**When you finish, send no chat message.** The controller reads rmap.
