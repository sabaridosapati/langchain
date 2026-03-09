# RAG AI Demo (LangChain + Gemini + FAISS)

A simple Retrieval-Augmented Generation (RAG) project that:
- Loads a PDF knowledge source (`PDFDOCNAME`)
- Splits text into chunks
- Creates embeddings with Google Gemini embeddings
- Stores vectors in FAISS
- Answers user questions using retrieved context and Gemini chat model

This repo includes:
- A script version: `RAGLANGC/RAGSCRIPT.py`
- A Streamlit UI: `RAGLANGC/streamlit_app.py`

## Tech Stack

- Python 3.11+
- LangChain
- Google Generative AI (Gemini)
- FAISS (local vector store)
- Streamlit

## Project Structure

```text
RAGLANG02_02/
  README.md
  RAGLANGC/
    RAGSCRIPT.py
    streamlit_app.py
    .env
    PDFDOCNAME
```

## Prerequisites

1. Python 3.11 or newer
2. A Google API key with Gemini access

## Setup

From repository root:

```powershell
cd RAGLANGC
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip
pip install streamlit python-dotenv langchain langchain-community langchain-google-genai langchain-text-splitters faiss-cpu pypdf
```

Create or edit `.env`:

```env
GOOGLE_API_KEY="your_google_api_key_here"
```

## Run Option 1: Python Script

```powershell
cd RAGLANGC
python RAGSCRIPT.py
```

It will run one sample question:
- `question about any content in pdf`

## Run Option 2: Streamlit App (Recommended)

```powershell
cd RAGLANGC
streamlit run streamlit_app.py
```

In the sidebar:
- Set `GOOGLE_API_KEY` (or keep it in `.env`)
- Set PDF path (default: `pdfdocument`)
- Optionally enable `Show retrieved chunks`

Then click **Run RAG**.

## How It Works

1. PDF is loaded with `PyPDFLoader`
2. Text is chunked (`chunk_size=500`, `chunk_overlap=50`)
3. Embeddings are created with `models/gemini-embedding-001`
4. Chunks are indexed in FAISS
5. Retriever uses MMR (`k=2`, `fetch_k=10`)
6. Prompt enforces context-only answers
7. Response is generated with `gemini-2.5-flash`

## Configuration Notes

- Change source PDFs in `RAGSCRIPT.py` (`files = [...]`) or update the Streamlit PDF path.
- To improve recall, tune:
- `chunk_size`, `chunk_overlap`
- retriever `k` / `fetch_k`
- Model settings used now:
  - Embeddings: `models/gemini-embedding-001`
  - Chat: `gemini-2.5-flash`

## Troubleshooting

- `GOOGLE_API_KEY is missing` or warning in UI:
- Add key in `.env` or Streamlit sidebar.
- `PDF not found`:
- Verify path in sidebar or place PDF inside `RAGLANGC/`.
- FAISS install issues on Windows:
- Ensure you are on a supported Python version (3.11 recommended).

## Next Improvements

- Add `requirements.txt`
- Support multiple PDFs and metadata filtering
- Persist/reload FAISS index instead of rebuilding each run
- Add evaluation set for answer quality
