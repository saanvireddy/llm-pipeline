# Multi-Cloud Fine-Tuned LLM Serving Pipeline

A fine-tuned, retrieval-augmented LLM serving system built end-to-end: QLoRA fine-tuning →
Ragas evaluation → Pinecone-backed RAG → containerized serving → cloud-agnostic Kubernetes
deployment (AWS EKS / Azure AKS) → automated CI/CD.

## What this project demonstrates

- **Fine-tuning**: Mistral-7B fine-tuned with QLoRA (4-bit, LoRA adapters) on a customer-support
  instruction dataset, using [Unsloth](https://github.com/unslothai/unsloth) for efficient
  training on a free-tier T4 GPU.
- **Evaluation**: [Ragas](https://github.com/explodinggradients/ragas) faithfulness and answer
  relevancy metrics, scored with an open-source judge model via Groq's free API.
- **Retrieval-augmented generation**: Pinecone vector index over a domain document set, combined
  with the fine-tuned model for grounded responses.
- **Serving**: FastAPI app combining the fine-tuned model + retrieval, containerized with Docker.
- **Infrastructure**: Cloud-agnostic Helm chart with per-cloud value overrides, plus Terraform for
  both AWS EKS and Azure AKS.
- **CI/CD**: GitHub Actions pipeline — evaluation gate → Docker build → push → Kubernetes deploy.

## Honest scope notes

This is a portfolio project built under real cost and hardware constraints, and the write-up below
is deliberately specific about what was actually run versus what was built-and-validated-but-not-deployed:

- **Training** ran on Google Colab's free-tier T4 GPU, capped at 200 steps (not a full epoch) to
  fit free-tier session limits. Training loss dropped from ~0.79 to ~0.63 over the run.
- **Evaluation** was run on a 20-question sample (not the full test set), scored with
  `llama-3.1-8b-instant` via Groq's free API as the judge model. Ragas scores are judge-dependent;
  a stronger judge model would likely produce different (probably higher) scores.
- **Docker image** builds successfully and correctly attempts model loading; full inference
  requires a CUDA GPU, which isn't available in the local dev environment, so local container runs
  fail at the expected point (no GPU) rather than being fully exercised end-to-end.
- **Kubernetes/Terraform**: both AWS EKS and Azure AKS Terraform configurations are complete and
  pass `terraform validate`; the Helm chart renders correctly for both clouds via
  `helm template`. Neither cluster was actually deployed (`terraform apply`), to avoid cloud costs.
  This means the manifests are validated for correctness but not live-tested against a running
  cluster.
- **CI/CD**: the GitHub Actions workflow is written and structurally complete; since no cloud
  infrastructure is live, the deploy step is unexercised in practice.

In an interview, the honest framing is: **designed and validated for multi-cloud EKS/AKS
deployment with cloud-agnostic Helm charts**, not "two production clusters running 24/7."

## Repo structure

```
data/              dataset download + processing scripts
training/          QLoRA fine-tuning script + saved LoRA adapter
eval/              Ragas evaluation script + results
retrieval/         Pinecone index building + retrieval logic
serving/           FastAPI serving app (model + retrieval)
docker/            Dockerfile for the serving app
k8s/helm/          Cloud-agnostic Helm chart (AWS/Azure value overrides)
infra/             Terraform for AWS EKS and Azure AKS
.github/workflows/ CI/CD pipeline
```

## Stack

QLoRA / PEFT / bitsandbytes / Unsloth · Pinecone · Ragas · FastAPI · Docker · Kubernetes · Helm ·
Terraform · GitHub Actions