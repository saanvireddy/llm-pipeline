import os
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

BASE_MODEL = "unsloth/mistral-7b-bnb-4bit"
ADAPTER_PATH = "training/adapter"

app = FastAPI()

# --- Retrieval setup ---
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("llm-pipeline-docs")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, top_k=3):
    vec = embedder.encode(query).tolist()
    res = index.query(vector=vec, top_k=top_k, include_metadata=True)
    return [m["metadata"]["text"] for m in res["matches"]]

# --- Model setup (loaded once at startup) ---
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL, quantization_config=bnb_config, device_map="auto"
)
model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
model.eval()

class Query(BaseModel):
    question: str

@app.post("/generate")
def generate(q: Query):
    context_chunks = retrieve(q.question, top_k=3)
    context = "\n".join(context_chunks)
    prompt = f"### Instruction:\n{q.question}\n\n### Input:\n{context}\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=150, do_sample=False)
    full_text = tokenizer.decode(output[0], skip_special_tokens=True)
    answer = full_text.split("### Response:\n")[-1].strip()
    return {"answer": answer, "sources": context_chunks}

@app.get("/health")
def health():
    return {"status": "ok"}