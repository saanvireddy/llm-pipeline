from datasets import load_dataset
import json
from pathlib import Path

# Bitext customer support dataset — public, no login required
ds = load_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset")

Path("data/raw").mkdir(parents=True, exist_ok=True)

records = []
for row in ds["train"]:
    records.append({
        "instruction": row["instruction"],
        "input": "",
        "output": row["response"],
    })

with open("data/raw/source.json", "w") as f:
    json.dump(records, f, indent=2)

print(f"Downloaded {len(records)} examples to data/raw/source.json")