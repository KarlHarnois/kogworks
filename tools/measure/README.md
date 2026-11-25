# Measurement scripts

The scripts in this directory measure the turns and token usage of the pilot manager from a Claude session transcript.

## Scripts

`turns.py` writes one record per manager turn. A record holds the trigger message, the tools the manager called, and the reply.

`usage.py` writes one usage record per turn. A record holds the input, cache-read, cache-write, and output token counts.

## Running a script

Each script takes two arguments: the input transcript path and the output JSONL path.

```sh
python3 tools/measure/turns.py <transcript.jsonl> <turns.jsonl>
python3 tools/measure/usage.py <transcript.jsonl> <usage.jsonl>
```

The intended input is the pilot-manager transcript directory `~/.claude/projects/-home-karl--local-share-ringleader-worktrees-rmap-pilot-manager/`.
