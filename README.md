# Python Documentation Helper

A Streamlit app that answers questions about the Python tutorial using retrieval-augmented generation (RAG).

The project has two main parts:

- an **ingestion pipeline** that crawls Python tutorial pages, chunks them, embeds them, and stores them in Pinecone
- a **chat interface** that retrieves relevant documentation context and answers user questions with an OpenAI chat model

---

## What this project does

This app lets you ask natural-language questions about Python documentation and get answers backed by retrieved source pages.

Under the hood, it:

1. crawls the Python tutorial docs
2. converts pages into LangChain `Document` objects
3. splits them into chunks
4. stores embeddings in a Pinecone index
5. uses a history-aware retriever so follow-up questions work better in chat
6. returns both the answer and the documentation sources used

--- 

## Key Features

- Retrieval-Augmented Generation (RAG)
   - Retrieves relevant documentation chunks from a vector database
   - Uses retrieved context to generate grounded answers
   - Reduces hallucination and improves accuracy

- Automated documentation ingestion
   - Crawls Python tutorial pages (via Tavily)
   - Converts them into structured documents
   - Splits into chunks for embedding
   - Builds a searchable knowledge base automatically

- Vector search with embeddings
   - Uses OpenAI embeddings (`text-embedding-3-small`)
   - Stores vectors in Pinecone (and optionally Chroma)
   - Enables semantic search over documentation

- Conversational Q&A (chat-based UI)
   - Built with Streamlit
   - Maintains chat history
   - Supports follow-up questions
   - Feels like chatting with documentation

- History-aware retriever
   - Rewrites queries based on chat history
   - Improves context retrieval for multi-turn conversations

- Modular pipeline design
   - `main.py` → UI layer
   - `backend/core.py` → RAG pipeline
   - `ingestion.py` → data pipeline
   - Clean separation of concerns

- Source attribution
   - Returns documentation sources used in answers
   - Improves trust and explainability

- End-to-end pipeline
   - Ingestion → embedding → storage → retrieval → generation → UI
   - Demonstrates full-stack AI system design

---

## System Architecture

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

--- 

## Project Structure

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

---

## LangChain Workflow

The LangChain workflow has two parts: **offline ingestion** and **online question answering**.


- **Offline ingestion workflow**

```text
Python documentation
   ↓
Tavily crawl
   ↓
LangChain Document objects
   ↓
RecursiveCharacterTextSplitter
   ↓
OpenAIEmbeddings
   ↓
Pinecone vector store
```

In `ingestion.py`, the project crawls the Python tutorial site with Tavily, converts each crawled page into a LangChain `Document`, chunks the documents with `RecursiveCharacterTextSplitter`, embeds them using `OpenAIEmbeddings(model="text-embedding-3-small")`, and stores them in Pinecone under the index `python-tutorial`.


- **Online QA workflow**

```text
User question
   ↓
Streamlit UI
   ↓
run_llm(query, chat_history)
   ↓
OpenAIEmbeddings
   ↓
PineconeVectorStore
   ↓
History-aware retriever
   ↓
Stuff documents chain
   ↓
Retrieval chain
   ↓
Answer + source documents
   ↓
Streamlit response
```

In `backend/core.py`, `run_llm()` creates embeddings, connects to the Pinecone index, initializes `ChatOpenAI(temperature=0)`, pulls LangChain Hub prompts, builds a `create_history_aware_retriever`, wraps it with `create_retrieval_chain`, then invokes the chain with the user query and chat history.

In `main.py`, the Streamlit app takes the user prompt, passes it to `run_llm()`, extracts source URLs from the returned context documents, appends the user/AI turns to chat history, and displays the answer with sources.

---

## Tech Stack

- LangChain
- OpenAI API
- Pinecone
- Tavily Search API
- Streamlit
- LangSmith

---

## Set up

1. Clone the repository

```text
git clone https://github.com/nut-hazel-ll/documentation_helper.git
cd documentation_helper
```

2. Install dependencies

Using Pipenv:

```text
pip install pipenv
pipenv install
pipenv shell
```

3. Create a `.env` file

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
TAVILY_API_KEY=your_tavily_api_key
LANGCHAIN_API_KEY=your_langsmith_key_optional
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=documentation-helper
```

Do not commit `.env`.

4. Run `ingestion.py` first

```text
python ingestion.py
```

5. Run the Streamlit app

```text
streamlit run main.py
```

6. Open the app

Streamlit will show a local URL, usually:

```text
http://localhost:8501
```

---

## Design Decisions

### Use RAG instead of pure LLM

Decision: Retrieve documentation instead of relying on model memory

👉 Why:
   - Reduces hallucination
   - Keeps answers grounded in real docs
   - Works better for factual domains like documentation


### Build a custom ingestion pipeline

Decision: Crawl + chunk + embed docs yourself

👉 Why:
   - Control over data quality
   - Can update or extend knowledge base
   - Avoids dependency on static datasets


### Use vector database (Pinecone)

Decision: Store embeddings in Pinecone instead of local search

👉 Why:
   - Fast semantic retrieval
   - Scalable
   - Production-ready vs simple local solutions


### Use chunking strategy

Decision: Split documents into smaller chunks

👉 Why:
   - Improves retrieval accuracy
   - Fits within LLM context window
   - Avoids irrelevant long passages


### Use history-aware retriever

Decision: Rewrite queries using chat history

👉 Why:
   - Handles follow-up questions
   - Makes the system conversational
   - Improves retrieval relevance


### Separate ingestion and query pipelines

Decision: Two-stage architecture
   - Offline: ingestion → embedding → storage  
   - Online: query → retrieval → generation  

👉 Why:
   - Efficient (no recompute at runtime)
   - Scalable
   - Cleaner system design


### Use Streamlit for UI

Decision: Lightweight chat interface

👉 Why:
   - Fast prototyping
   - Easy to demonstrate
   - Good for showcasing projects


### Return sources with answers

Decision: Show retrieved document URLs

👉 Why:
   - Improves trust
   - Enables verification


### Modular architecture

Decision: Split into:
   - UI (main.py)
   - backend (core.py)
   - ingestion (ingestion.py)

👉 Why:
   - Easier to maintain
   - Easier to extend
   - Cleaner separation of concerns
