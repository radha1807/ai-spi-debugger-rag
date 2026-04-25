AI SPI Debugger — RAG-Based SPI Log Analysis
An AI-assisted debugging system for embedded SPI communication logs. Uses vector embeddings + retrieval-augmented generation (RAG) to classify faults and suggest root causes — grounded in historical failure cases, not just pattern matching.

What It Actually Does

Indexes a knowledge base of labeled historical SPI failures into a persistent vector database (ChromaDB)
Embeds new query logs using sentence-transformers
Retrieves the most semantically similar historical failures
Sends the log + retrieved context to GPT-4o-mini for root cause analysis
Outputs structured JSON with diagnosis, confidence, and fix suggestions

This is real RAG — the LLM's output is grounded in retrieved context, not just its training data.

Architecture
Knowledge Base (historical failures)
        │
        ▼
  [Parser] → [Embedder] → [ChromaDB (persistent)]
                                    │
Query Logs ──► [Parser] → [Embedder] → [Retrieval (top-k similar)]
                                    │
                          [GPT-4o-mini + context]
                                    │
                          [results.json output]



Project Structure
ai-spi-debugger-rag/
├── data/
│   ├── knowledge_base.txt   # Historical labeled SPI failures (RAG context)
│   └── sample_logs.txt      # New logs to diagnose
├── src/
│   ├── parser.py            # Log parser — extracts status + raw text
│   ├── embeddings.py        # Sentence-transformer embeddings
│   ├── retrieval.py         # ChromaDB store + query (persistent)
│   ├── llm_inference.py     # GPT-4o-mini RAG prompt + fallback
│   └── main.py              # Pipeline orchestration + CLI
├── outputs/
│   └── results.json         # Diagnosis output
├── db/                      # ChromaDB persistent storage (auto-created)
├── .env                     # API keys (not committed)
├── requirements.txt
└── README.md



Setup
1. Clone and install dependencies
bashgit clone https://github.com/radha1807/ai-spi-debugger-rag.git
cd ai-spi-debugger-rag
pip install -r requirements.txt




