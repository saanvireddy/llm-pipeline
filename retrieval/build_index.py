import json
import os
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
INDEX_NAME = "llm-pipeline-docs"

if INDEX_NAME not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(INDEX_NAME)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

docs = json.load(open("data/raw/documents.json"))
vectors = []
for i, doc in enumerate(docs):
    vec = embedder.encode(doc["text"]).tolist()
    vectors.append({
        "id": str(i),
        "values": vec,
        "metadata": {"text": doc["text"], "source": doc["source"]},
    })

index.upsert(vectors=vectors)
print(f"Upserted {len(vectors)} vectors to Pinecone index '{INDEX_NAME}'")