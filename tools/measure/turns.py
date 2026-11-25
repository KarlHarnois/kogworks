import json, sys
path, out = sys.argv[1], sys.argv[2]
turns = []; cur = None
def text_of(c):
    if isinstance(c, str): return c
    return " ".join(b.get("text","") for b in c if isinstance(b, dict) and b.get("type")=="text")
with open(path) as f:
    for line in f:
        try: e = json.loads(line)
        except: continue
        t = e.get("type")
        if t == "user" and not e.get("isMeta") and not e.get("isSidechain"):
            c = e.get("message",{}).get("content")
            if isinstance(c, list) and any(isinstance(b,dict) and b.get("type")=="tool_result" for b in c):
                continue
            txt = text_of(c).strip()
            if not txt: continue
            cur = {"ts": e.get("timestamp"), "trigger": txt[:600], "tools": [], "reply": ""}
            turns.append(cur)
        elif t == "assistant" and cur is not None and not e.get("isSidechain"):
            for b in e.get("message",{}).get("content",[]) or []:
                if b.get("type")=="tool_use":
                    inp = b.get("input",{})
                    s = inp.get("command") or inp.get("prompt") or inp.get("skill") or inp.get("file_path") or json.dumps(inp)
                    cur["tools"].append(f'{b["name"]}: {str(s)[:200]}')
                elif b.get("type")=="text":
                    cur["reply"] = b["text"][:500]
        elif t == "summary" or (t=="system" and e.get("subtype")=="compact_boundary"):
            turns.append({"ts": e.get("timestamp"), "trigger": "[COMPACTION]", "tools": [], "reply": ""})
with open(out,"w") as o:
    for i,tn in enumerate(turns):
        o.write(json.dumps({"n":i, **tn})+"\n")
print(len(turns))
