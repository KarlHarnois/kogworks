import json
import sys


class TranscriptReader:
    def __init__(self, path):
        self.path = path

    def events(self):
        with open(self.path) as transcript:
            for line in transcript:
                event = self.parse(line)
                if event is not None:
                    yield event

    def parse(self, line):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return None


class UsageExtractor:
    def __init__(self):
        self.turns = []
        self.current = None
        self.seen_message_ids = set()

    def extract(self, events):
        for event in events:
            self.add(event)
        return self.turns

    def add(self, event):
        kind = event.get("type")
        if self.is_user_trigger(kind, event):
            self.add_turn()
        elif self.is_compaction(kind, event):
            self.add_compaction()
        elif kind == "assistant" and self.current is not None and not event.get("isSidechain"):
            self.add_usage(event)

    def is_user_trigger(self, kind, event):
        if kind != "user" or event.get("isMeta") or event.get("isSidechain"):
            return False
        content = self.content_of(event)
        if self.has_tool_result(content):
            return False
        return bool(self.text_of(content).strip())

    def add_turn(self):
        self.current = {
            "calls": 0,
            "in": 0,
            "cache_read": 0,
            "cache_write": 0,
            "out": 0,
            "ctx_first": None,
            "ctx_last": None,
        }
        self.turns.append(self.current)

    def is_compaction(self, kind, event):
        return kind == "summary" or (
            kind == "system" and event.get("subtype") == "compact_boundary"
        )

    def add_compaction(self):
        self.turns.append({"compaction": True})

    def add_usage(self, event):
        message = event.get("message", {})
        message_id = message.get("id")
        usage = message.get("usage")
        if not usage or message_id in self.seen_message_ids:
            return
        self.seen_message_ids.add(message_id)
        context = self.context_size(usage)
        self.current["calls"] += 1
        self.current["in"] += usage.get("input_tokens", 0)
        self.current["cache_read"] += usage.get("cache_read_input_tokens", 0)
        self.current["cache_write"] += usage.get("cache_creation_input_tokens", 0)
        self.current["out"] += usage.get("output_tokens", 0)
        if self.current["ctx_first"] is None:
            self.current["ctx_first"] = context
        self.current["ctx_last"] = context + usage.get("output_tokens", 0)

    def context_size(self, usage):
        return (
            usage.get("input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
        )

    def content_of(self, event):
        return event.get("message", {}).get("content")

    def has_tool_result(self, content):
        return isinstance(content, list) and any(
            isinstance(block, dict) and block.get("type") == "tool_result"
            for block in content
        )

    def text_of(self, content):
        if isinstance(content, str):
            return content
        if not isinstance(content, list):
            return ""
        return " ".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )


class JsonlWriter:
    def __init__(self, path):
        self.path = path

    def write(self, records):
        with open(self.path, "w") as output:
            for number, record in enumerate(records):
                output.write(json.dumps({"n": number, **record}) + "\n")


def main():
    transcript_path, output_path = sys.argv[1], sys.argv[2]
    events = TranscriptReader(transcript_path).events()
    turns = UsageExtractor().extract(events)
    JsonlWriter(output_path).write(turns)
    print(len(turns))


if __name__ == "__main__":
    main()
