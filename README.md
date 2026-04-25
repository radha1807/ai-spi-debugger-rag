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






Usage
First run — index KB and diagnose:
bashcd src
python main.py
Re-index knowledge base (after updating it):
bashpython main.py --reindex
Custom paths:
bashpython main.py --kb path/to/kb.txt --logs path/to/new_logs.txt --output path/to/out.json

Sample Output
json{
    "log": "[2024-01-16] CS_LOW MOSI=0x0F MISO=0x00 CLK=16MHz ERR: no response",
    "status": "ERROR",
    "similar_cases": [
        "[2024-01-10] CS_LOW MOSI=0xFF MISO=0x00 CLK=1MHz ERR: no response from slave",
        "[2024-01-12] CS_LOW MOSI=0xFF MISO=0x00 CLK=8MHz ERR: clock glitch detected"
    ],
    "diagnosis": "Root Cause: Slave device not responding — likely CPOL/CPHA mismatch at high clock speeds or signal integrity issue at 16MHz.\nFix: Verify SPI mode (0/1/2/3) matches slave datasheet. Reduce clock to 1MHz to isolate timing vs. hardware issues.\nConfidence: Medium"
}

Requirements
sentence-transformers
chromadb
openai
python-dotenv

Known Limitations

Diagnosis quality depends on the size and quality of the knowledge base — a 10-entry KB gives weak retrieval
GPT-4o-mini can hallucinate root causes if similar cases are not truly relevant
No real-time log streaming — batch processing only
Evaluated on synthetic logs; not yet validated on production hardware traces




