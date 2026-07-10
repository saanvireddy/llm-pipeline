import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("llm-pipeline-docs")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, top_k=3):
    vec = embedder.encode(query).tolist()
    res = index.query(vector=vec, top_k=top_k, include_metadata=True)
    return [(m["metadata"]["source"], m["score"], m["metadata"]["text"][:100]) for m in res["matches"]]

if __name__ == "__main__":
    query = "How do I get my money back for an order?"
    results = retrieve(query)
    for source, score, snippet in results:
        print(f"[{score:.3f}] {source}: {snippet}...")