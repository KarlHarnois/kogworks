import json, sys
path, out = sys.argv[1], sys.argv[2]
turns=[]; cur=None; seen=set()
def text_of(c):
    if isinstance(c,str): return c
    return " ".join(b.get("text","") for b in c if isinstance(b,dict) and b.get("type")=="text")
with open(path) as f:
    for line in f:
        try: e=json.loads(line)
        except: continue
        t=e.get("type")
        if t=="user" and not e.get("isMeta") and not e.get("isSidechain"):
            c=e.get("message",{}).get("content")
            if isinstance(c,list) and any(isinstance(b,dict) and b.get("type")=="tool_result" for b in c): continue
            if not text_of(c).strip(): continue
            cur={"calls":0,"in":0,"cache_read":0,"cache_write":0,"out":0,"ctx_first":None,"ctx_last":None}; turns.append(cur)
        elif (t=="summary" or (t=="system" and e.get("subtype")=="compact_boundary")):
            turns.append({"compaction":True})
        elif t=="assistant" and cur is not None and not e.get("isSidechain"):
            m=e.get("message",{}); mid=m.get("id"); u=m.get("usage")
            if not u or mid in seen: continue
            seen.add(mid)
            ctx=u.get("input_tokens",0)+u.get("cache_read_input_tokens",0)+u.get("cache_creation_input_tokens",0)
            cur["calls"]+=1; cur["in"]+=u.get("input_tokens",0); cur["cache_read"]+=u.get("cache_read_input_tokens",0)
            cur["cache_write"]+=u.get("cache_creation_input_tokens",0); cur["out"]+=u.get("output_tokens",0)
            if cur["ctx_first"] is None: cur["ctx_first"]=ctx
            cur["ctx_last"]=ctx+u.get("output_tokens",0)
with open(out,"w") as o:
    for i,tn in enumerate(turns): o.write(json.dumps({"n":i,**tn})+"\n")
