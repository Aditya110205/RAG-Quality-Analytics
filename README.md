# RAG Quality Analytics

A minimal local Retrieval-Augmented Generation (RAG) system built as
the foundation for a RAG quality analytics platform.

## Week 1 MVP

The system:

1. Loads text documents
2. Splits documents into chunks
3. Generates embeddings
4. Stores embeddings in Chroma
5. Retrieves relevant chunks
6. Sends retrieved context to a local LLM
7. Generates a grounded answer

## Architecture

data/*.txt
    ↓
chunker.py
    ↓
Sentence Transformers
    ↓
Chroma
    ↓
retriever.py
    ↓
Ollama
    ↓
answer

## Requirements

- Windows
- Python 3.13+
- Ollama

## Setup

Create virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1