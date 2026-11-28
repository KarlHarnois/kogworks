# Controller log

This document specifies what `kogworks controller` prints while it runs. The log is for the person who runs the controller in a terminal and looks at it from time to time.

## Principles

1. Each item line shows one roadmap item and where it is in its lifecycle.
2. The log shows what `rmap` records. It shows nothing that the controller cannot read.
3. The log is append-only text. It is not a full-screen interface.
4. Color marks meaning and is never the only signal. Every state also has a glyph or a word.
5. The log goes to stderr. Nothing else that the controller prints goes to stdout.

## Example

At 118 columns:

```
14:02:11  ● kogworks  roadmap factory-mvp · manager kw-manager · poll 30s

14:02:12  rm-8bdc  build ▸ review ○ merge ○  building     Disarm auto-merge when the approved head changes or the ite…
14:02:13  rm-35cb  build ▸ review ○ merge ○  building     Add kogworks check and remove the module and format commands
14:02:40  rm-c41e  write ▸ accept ○          researching  Compare OSC 8 hyperlink support across terminals
14:05:40  rm-8bdc  build ✓ review ▸ merge ○  reviewing    Disarm auto-merge when the approved head changes or the ite…
14:09:12  rm-8bdc  build ✓ review ↺ merge ○  changes      Disarm auto-merge when the approved head changes or the ite…
          ├─ criterion 2  no test shows the disarm when the approved head changes
          ├─ criterion 4  the return to fixing leaves auto-merge armed
          ╰─ reviewer     review-rm-8bdc-7da1703, behavior review
14:09:40  rm-8bdc  build ▸ review ↺ merge ○  fixing (2)   Disarm auto-merge when the approved head changes or the ite…
14:14:40  · running rm-8bdc fixing 5m, rm-35cb building 12m, rm-c41e researching 12m · 0 merged
14:15:03  rm-8bdc  build ✓ review ▸ merge ○  reviewing    Disarm auto-merge when the approved head changes or the ite…
14:17:44  rm-8bdc  build ✓ review ✓ merge ▸  merging      Disarm auto-merge when the approved head changes or the ite…
14:18:40  rm-8bdc  build ✓ review ✓ merge ✓  merged #33   Disarm auto-merge when the approved head changes or the ite…
14:18:41  rm-9a01  build ▸ review ○ merge ○  building     Show a heartbeat line while the controller waits on long bu…
14:19:20  rm-c41e  write ✓ accept ▸          reported     Compare OSC 8 hyperlink support across terminals
14:20:05  rm-c41e  write ✓ accept ✓          accepted     Compare OSC 8 hyperlink support across terminals
14:20:30  rm-d210  write ▸ accept ○          designing    Lay out the stop summary for narrow terminals
14:21:47  rm-35cb  build ✓ review ▸ merge ○  reviewing    Add kogworks check and remove the module and format commands
14:22:30  rm-35cb  build ✓ review ✓ merge ▸  merging      Add kogworks check and remove the module and format commands
14:23:02  rm-35cb  build ✓ review ✓ merge ✗  head moved   Add kogworks check and remove the module and format commands
          ├─ error        PR 34 head is 4f5a6b7, not the approved 9f1c2ab
          ├─ pr           #34  build-rm-35cb
          ├─ disarmed     gh pr merge 34 --disable-auto
          ├─ manager      message sent to kw-manager
          ╰─ next         rerun, the new head needs a review
14:23:02  ■ controller stopped  1 merged · 1 accepted · 1 failed · 2 running
          ├─ running      rm-9a01 building 4m · its session keeps running
          ├─ running      rm-d210 designing 3m · its session keeps running
          ╰─ rerun        kogworks controller --repo . --poll 30
```

Below 110 columns the track shows glyphs only:

```
14:02:12  rm-8bdc  ▸○○  building     Disarm auto-merge when the approved head c…
14:02:13  rm-35cb  ▸○○  building     Add kogworks check and remove the module a…
14:02:40  rm-c41e  ▸○   researching  Compare OSC 8 hyperlink support across ter…
14:05:40  rm-8bdc  ✓▸○  reviewing    Disarm auto-merge when the approved head c…
14:09:12  rm-8bdc  ✓↺○  changes      Disarm auto-merge when the approved head c…
          ├─ criterion 2  no test shows the disarm when the approved head
          │               changes
```

## Line kinds

| Line | Shape |
|---|---|
| Banner | `time  ● kogworks  roadmap <name> · manager <session> · poll <n>s` |
| Item | `time  id  track  status  title` |
| Sub-line | `├─ label  value`, indented under the item ID |
| Alive | `time  · running <id> <status> <n>m, ... · <n> merged` |
| Stop | `time  ■ controller stopped  <counts>` followed by sub-lines |
| Controller failure | `time  controller  <status>` followed by sub-lines |

Columns are two spaces apart. The time is local wall-clock time as `HH:MM:SS`.

When no manager is configured, the banner reads `no manager` in yellow in place of `manager <session>`.

## Item line

### Track

The track shows the lifecycle. The status shows the kind.

| Item kind | Track | Source statuses in `rmap` |
|---|---|---|
| build | `build review merge` | `dispatched`, `in_review`, `fixing`, `merging`, `merged` |
| research, design, any other kind | `write accept` | `dispatched`, `reported`, `accepted` |

Each stage is followed by one glyph:

| Glyph | Meaning | Style |
|---|---|---|
| `▸` | active | stage name bold, glyph cyan |
| `✓` | done | stage name gray, glyph green |
| `○` | not reached, or waiting to start again | stage name and glyph gray |
| `↺` | sent back by a reviewer | stage name bold, glyph yellow |
| `✗` | failed, and the controller stops | stage name bold, glyph red |

The track is padded to the width of the build track so the status column lines up.

Below 110 columns the track shows only the glyphs, for example `✓▸○`, padded to three glyphs.

### Status

The status is at most 11 characters. It carries no SHA and no duration.

| Status | Kind | When | Style |
|---|---|---|---|
| `building` | build | the item is claimed | gray |
| `researching` | research | the item is claimed | gray |
| `designing` | design | the item is claimed | gray |
| `working` | other | the item is claimed | gray |
| `reviewing` | build | a review session starts | gray |
| `verifying` | build | a verify session starts | gray |
| `changes` | build | a review records the verdict `changes` | yellow |
| `fixing (n)` | build | the item moves to `fixing`; `n` is the round that follows | gray |
| `new head` | build | a new head is recorded during a review | yellow |
| `abandoned` | build | a review session ends with no verdict | yellow |
| `merging` | build | the item moves to `merging` | gray |
| `merged #n` | build | the item closes as `merged`; `#n` is the pull request | `merged` green |
| `reported` | research, design | the item moves to `reported` | gray |
| `accepted` | research, design | the item closes as `accepted` | green |
| `head moved` | build | merge failure: the head is not the approved head | bold red |
| `timed out` | build | merge failure: the pull request did not merge in time | bold red |
| `refused` | build | merge failure: a repository setting blocks the merge | bold red |
| `failed` | any | a command failed; the `✗` on the track shows the stage | bold red |

Red statuses stop the controller. Yellow statuses do not.

### Title

The title is last on the line. It uses the default text color. It is cut with `…` to fit the terminal width, and never for any other reason.

Before the title is printed, newlines and tabs become single spaces and control characters are removed.

## Sub-lines

Sub-lines hang under an item line as a tree. `├─` starts each sub-line except the last, which starts with `╰─`. Labels are gray and padded to 12 characters. A long value wraps under the value column. A command is never cut.

Under a failure, in this order:

| Label | Value | When |
|---|---|---|
| `error` | the error message, in red | always |
| `exit <code>` | the command that failed | a command failed |
| `pr` | `#n`, the branch, and the head when known | the item has a pull request |
| `disarmed` | the command that turned auto-merge off | auto-merge was turned off |
| `cleanup` | the command that ended the session | a session failed to start |
| `manager` | `message sent to <session>` | a manager is configured |
| `next` | what the person does next | always, and last |

`next` gives a specific step for an error that the controller recognizes. For any other error it reads `fix the error above, then rerun`.

Under `changes`:

| Label | Value |
|---|---|
| `criterion <n>` | the reviewer's note, for each criterion with the verdict `failed` |
| `criteria` | `all <n> met on this head`, when no criterion failed |
| `reviewer` | the review session and the review kind |

Under `verifying`: one `criterion <n>` line reading `no verdict on this head` for each criterion without a verdict, then `reviewer`.

Under `abandoned`: `session`, with the session that ended.

Under `fixing (n)`, only when no review verdict came before it: `moved`, reading `in_review to fixing with no review verdict`.

Review outcomes that do not stop the controller:

```
15:01:10  rm-77c0  build ✓ review ▸ merge ○  reviewing    Print the stop summary when the controller exits
15:03:22  rm-77c0  build ✓ review ○ merge ○  new head     Print the stop summary when the controller exits
15:03:52  rm-77c0  build ✓ review ▸ merge ○  reviewing    Print the stop summary when the controller exits
15:07:30  rm-77c0  build ✓ review ▸ merge ○  verifying    Print the stop summary when the controller exits
          ├─ criterion 3  no verdict on this head
          ├─ criterion 5  no verdict on this head
          ╰─ reviewer     review-rm-77c0-5d6e7f8 approved, verify starts
15:09:41  rm-77c0  build ✓ review ✓ merge ▸  merging      Print the stop summary when the controller exits

15:20:04  rm-9a01  build ✓ review ↺ merge ○  changes      Show a heartbeat line while the controller waits on long bu…
          ├─ criteria     all 6 met on this head
          ╰─ reviewer     review-rm-9a01-4be21c0, behavior review

15:31:18  rm-35cb  build ✓ review ○ merge ○  abandoned    Add kogworks check and remove the module and format commands
          ╰─ session      review-rm-35cb-9f1c2ab ended with no verdict
15:31:48  rm-35cb  build ✓ review ▸ merge ○  reviewing    Add kogworks check and remove the module and format commands

15:40:09  rm-77c0  build ▸ review ○ merge ○  fixing (2)   Print the stop summary when the controller exits
          ╰─ moved        in_review to fixing with no review verdict
```

Failures:

```
14:52:57  rm-9a01  build ✓ review ✓ merge ✗  timed out    Show a heartbeat line while the controller waits on long bu…
          ├─ error        PR 35 did not merge within 3600 seconds
          ├─ pr           #35  build-rm-9a01 @ 4be21c0
          ├─ disarmed     gh pr merge 35 --disable-auto
          ├─ manager      message sent to kw-manager
          ╰─ next         find what holds #35 open, then rerun

14:31:10  rm-77c0  build ✓ review ✓ merge ✗  refused      Print the stop summary when the controller exits
          ├─ error        `gh api repos/KarlHarnois/kogworks --jq .allow_auto_merge` printed `false`, not `true`
          ├─ pr           #37  build-rm-77c0 @ a81f0c2
          ├─ manager      message sent to kw-manager
          ╰─ next         enable "Allow auto-merge" in the repository settings, then rerun

14:35:48  rm-77c0  build ✓ review ✗ merge ○  failed       Print the stop summary when the controller exits
          ├─ error        a session named review-rm-77c0-a81f0c2 already exists
          ├─ exit 1       ringleader new --name review-rm-77c0-a81f0c2 --repo . --agent claude --prompt <filled brief>
          ├─ cleanup      rmap session end review-rm-77c0-a81f0c2 --reason abandoned
          ├─ manager      message sent to kw-manager
          ╰─ next         fix the error above, then rerun

14:40:22  rm-9a01  build ✗ review ○ merge ○  failed       Show a heartbeat line while the controller waits on long bu…
          ├─ error        agent "opencode" is not installed
          ├─ exit 127     ringleader new --name build-rm-9a01 --repo . --agent opencode --prompt <filled brief>
          ├─ cleanup      rmap session end build-rm-9a01 --reason abandoned
          ├─ manager      message sent to kw-manager
          ╰─ next         fix the error above, then rerun

14:02:12  controller  rmap next failed
          ├─ error        roadmap "factory-mvp" not found
          ├─ exit 1       rmap next --roadmap factory-mvp --taken-by controller --json
          ├─ manager      message sent to kw-manager
          ╰─ next         check the roadmap name in .kogworks/factory.knv, then rerun
```

## Alive line

The controller prints the alive line when 5 minutes pass with no other line. It prints it again after every further 5 quiet minutes. The time is measured from the last line printed, and the check also runs while the controller waits for a merge.

The line is gray. It names each running item with its status and the whole minutes it has spent there, then the count of merged items. When that does not fit the terminal width, it shows counts only: `· 3 running · 0 merged · 0 accepted`.

## Stop block

When the controller stops, it prints the stop line with the counts of merged, accepted, failed and running items for this run. Under it:

| Label | Value |
|---|---|
| `running` | one line for each item still running: the ID, its status, the minutes, and `its session keeps running` |
| `rerun` | the command that started the controller, in bold |

## Color

Colors are fixed 24-bit values so that the terminal theme does not change them.

| Role | Hex |
|---|---|
| success | `#5bd08a` |
| failure | `#f25f5c` |
| active | `#4fc7c7` |
| review outcome | `#e0b05c` |
| secondary | `#7a7f87` |

### Styles

| Part | Style |
|---|---|
| the time at the start of any line | secondary |
| the item ID on an item line | bold |
| `kogworks` in the banner | bold |
| `roadmap` and `manager` in the banner | secondary |
| each `·` in the banner | secondary |
| `poll <n>s` in the banner | secondary |
| `no manager` in the banner | yellow |
| the roadmap name and the manager session in the banner | default |
| the tree glyphs `├─` and `╰─` | secondary |
| the continuation glyph `│` | secondary |
| `■` in the stop line | failure |
| `controller stopped` in the stop line | bold |
| `<n> merged` and `<n> accepted` in the stop line | success |
| `<n> failed` in the stop line | failure |
| each `·` in the stop line | secondary |
| `<n> running` in the stop line | default |
| the item ID on a `running` sub-line | bold |
| `· its session keeps running` on a `running` sub-line | secondary |
| the owner before a sub-line when output is not a terminal | secondary |
| the title | default |

Rules:

1. Use color only when stderr is a terminal.
2. `NO_COLOR` set to any value turns color off. `FORCE_COLOR` set to any value turns color on when stderr is not a terminal. `NO_COLOR` wins.
3. When `COLORTERM` is not `truecolor` or `24bit`, use the nearest color of the 256-color palette.
4. Reset the style before starting a new one. Never let bold or a color carry into the next span.
5. A pull request number is an OSC 8 hyperlink to the pull request when color is on. The link target comes from the repository's remote.

## Width

1. Read the terminal width from stderr before each line, so a resized terminal is handled.
2. Measure text in display columns, not in characters.
3. When stderr is not a terminal, do not fit to a width. Cut a title at 120 characters with `…`.

## Output that is not a terminal

When stderr is a file or a pipe, each sub-line carries the item ID so that a search for the ID finds every line of that item:

```
          rm-35cb  ├─ pr           #34  build-rm-35cb
          rm-35cb  ├─ disarmed     gh pr merge 34 --disable-auto
          rm-35cb  ├─ manager      message sent to kw-manager
          rm-35cb  ╰─ next         rerun, the new head needs a review
14:23:02  ■ controller stopped  1 merged · 1 accepted · 1 failed · 2 running
          controller  ├─ running      rm-9a01 building 4m · its session keeps running
          controller  ├─ running      rm-d210 designing 3m · its session keeps running
```

## Sources

| Shown | Read from |
|---|---|
| Lifecycle changes | `rmap log --since <event id> --json`, event types `item-claimed`, `item-reported`, `review-started`, `item-reviewed`, `item-advanced`, `head-recorded`, `session-ended`, `item-closed` |
| Title, kind, criteria, verdicts, reviews | `rmap item show <id> --json`, fields `item`, `criterion_verdicts`, `pull_request.reviews` |
| Round `n` in `fixing (n)` | the count of moves to `fixing` for the item, plus 1 |
| Failures | the controller's own errors |

The controller keeps the ID of the last event it has printed and asks only for later events.

## Not shown

`rmap` does not record these, so the log does not show them: a reviewer's findings outside the acceptance criteria, a reviewer's question to the manager, and the output of a failed command beyond its error message.

The log shows no durations on item lines. Every line has a time, and the event log holds the timestamps for measurement.
