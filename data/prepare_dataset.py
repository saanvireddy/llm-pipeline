import json, random
from pathlib import Path

def split(records, seed=42, ratios=(0.9, 0.05, 0.05)):
    random.Random(seed).shuffle(records)
    n = len(records)
    a, b = int(n*ratios[0]), int(n*(ratios[0]+ratios[1]))
    return records[:a], records[a:b], records[b:]

def write_jsonl(records, path):
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

if __name__ == "__main__":
    raw = json.load(open("data/raw/source.json"))
    train, val, test = split(raw)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    write_jsonl(train, "data/processed/train.jsonl")
    write_jsonl(val, "data/processed/val.jsonl")
    write_jsonl(test, "data/processed/test.jsonl")
    print(f"train={len(train)} val={len(val)} test={len(test)}")