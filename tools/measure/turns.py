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


class TurnExtractor:
    TRIGGER_LIMIT = 600
    TOOL_LIMIT = 200
    REPLY_LIMIT = 500
    COMPACTION_TRIGGER = "[COMPACTION]"

    def __init__(self):
        self.turns = []
        self.current = None

    def extract(self, events):
        for event in events:
            self.add(event)
        return self.turns

    def add(self, event):
        kind = event.get("type")
        trigger = self.trigger_text(kind, event)
        if trigger is not None:
            self.add_user_turn(event, trigger)
        elif kind == "assistant" and self.current is not None and not event.get("isSidechain"):
            self.add_assistant_event(event)
        elif self.is_compaction(kind, event):
            self.add_compaction(event)

    def trigger_text(self, kind, event):
        if kind != "user" or event.get("isMeta") or event.get("isSidechain"):
            return None
        content = self.content_of(event)
        if self.has_tool_result(content):
            return None
        text = self.text_of(content).strip()
        if not text:
            return None
        return text

    def add_user_turn(self, event, trigger):
        self.current = {
            "ts": event.get("timestamp"),
            "trigger": trigger[: self.TRIGGER_LIMIT],
            "tools": [],
            "reply": "",
        }
        self.turns.append(self.current)

    def add_assistant_event(self, event):
        for block in self.content_of(event) or []:
            if block.get("type") == "tool_use":
                self.current["tools"].append(self.describe_tool(block))
            elif block.get("type") == "text":
                self.current["reply"] = block["text"][: self.REPLY_LIMIT]

    def describe_tool(self, block):
        inputs = block.get("input", {})
        detail = self.tool_detail(inputs)
        return f'{block["name"]}: {str(detail)[: self.TOOL_LIMIT]}'

    def tool_detail(self, inputs):
        return (
            inputs.get("command")
            or inputs.get("prompt")
            or inputs.get("skill")
            or inputs.get("file_path")
            or json.dumps(inputs)
        )

    def is_compaction(self, kind, event):
        return kind == "summary" or (
            kind == "system" and event.get("subtype") == "compact_boundary"
        )

    def add_compaction(self, event):
        self.turns.append(
            {
                "ts": event.get("timestamp"),
                "trigger": self.COMPACTION_TRIGGER,
                "tools": [],
                "reply": "",
            }
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
    turns = TurnExtractor().extract(events)
    JsonlWriter(output_path).write(turns)
    print(len(turns))


if __name__ == "__main__":
    main()
