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

## How the app works

- Streamlit frontend

   `main.py` defines the Streamlit app. It:

   - sets up the page and sidebar
   - stores user profile info in session state
   - keeps chat history in session state
   - sends the user prompt to `run_llm(...)`
   - extracts source URLs from retrieved documents
   - renders the answer plus a source list in chat history

- Retrieval pipeline

   `backend/core.py` contains `run_llm(query, chat_history)`.

   It:

   - creates OpenAI embeddings with `text-embedding-3-small`
   - connects to Pinecone using the `python-tutorial` index
   - creates a `ChatOpenAI` model with temperature=0
   - pulls LangChain Hub prompts for:
      - retrieval QA
      - question rephrasing
   - builds a **history-aware** retriever
   - builds a retrieval chain
   - invokes the chain with the current user input and chat history

   This design makes follow-up questions more robust than a plain retriever.

- Ingestion pipeline

   `ingestion.py` prepares the knowledge base.

   It:

   - loads environment variables
   - configures SSL certificates with `certifi`
   - initializes OpenAI embeddings
   - initializes the Pinecone vector store
   - crawls `https://docs.python.org/3/tutorial/index.html` with Tavily
   - converts crawl results into LangChain `Document` objects
   - splits documents with chunk size 4000 and overlap 200
   - asynchronously indexes document batches into Pinecone

   The batch indexing logic uses `asyncio.gather(...)` so multiple batches can be added concurrently.


