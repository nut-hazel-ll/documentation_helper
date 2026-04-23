# Python Documentation Helper

A Streamlit app that answers questions about the Python tutorial using retrieval-augmented generation (RAG).

The project has two main parts:

- an **ingestion pipeline** that crawls Python tutorial pages, chunks them, embeds them, and stores them in Pinecone
- a **chat interface** that retrieves relevant documentation context and answers user questions with an OpenAI chat model

## What it does

This app lets you ask natural-language questions about Python documentation and get answers backed by retrieved source pages.

Under the hood, it:

1. crawls the Python tutorial docs
2. converts pages into LangChain `Document` objects
3. splits them into chunks
4. stores embeddings in a Pinecone index
5. uses a history-aware retriever so follow-up questions work better in chat
6. returns both the answer and the documentation sources used

## Architecture

```text
Python docs site
   ↓
Tavily crawl
   ↓
Document creation
   ↓
Chunking (RecursiveCharacterTextSplitter)
   ↓
Embeddings (OpenAI text-embedding-3-small)
   ↓
Pinecone index: python-tutorial
   ↓
History-aware retriever
   ↓
Retrieval QA chain
   ↓
Streamlit chat UI
```

## Repository Structure

```text
.
├── main.py              # Streamlit UI
├── ingestion.py         # Crawl, chunk, embed, and index documentation
├── consts.py            # Shared constants (index name)
├── logger.py            # Colored console logging helpers
├── backend/
│   └── core.py          # RAG pipeline and LLM call
├── chroma_db/           # Local Chroma artifacts currently present in repo
├── Pipfile              # Python dependencies
└── Pipfile.lock
```


