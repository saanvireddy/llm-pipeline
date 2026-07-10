import json
import os
from dotenv import load_dotenv
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from ragas.metrics import answer_relevancy, faithfulness
from ragas.run_config import RunConfig
load_dotenv()

with open("eval/eval_answers.json") as f:
    records = json.load(f)

# Reduce sample size for a cleaner, faster run
eval_data = {
    "question": [r["question"] for r in records][:10],
    "answer": [r["answer"] for r in records][:10],
    "contexts": [r["contexts"] if r["contexts"] else [""] for r in records][:10],
    "ground_truth": [r["ground_truth"] for r in records][:10],
}

dataset = Dataset.from_dict(eval_data)

judge_llm = LangchainLLMWrapper(ChatOpenAI(
    model="llama-3.1-8b-instant",
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
    temperature=0,
))

judge_embeddings = LangchainEmbeddingsWrapper(
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
)



answer_relevancy.strictness = 1  # avoids Groq's n>1 restriction

# Slow down and give each call more time
run_config = RunConfig(max_workers=1, timeout=120)
results = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy],
    llm=judge_llm,
    embeddings=judge_embeddings,
    run_config=run_config,
)
print(results)
results.to_pandas().to_csv("eval/results.csv", index=False)
print("Saved detailed results to eval/results.csv")