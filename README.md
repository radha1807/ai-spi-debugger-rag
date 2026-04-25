# SPI Log Analyzer with AI (RAG-based Debugging System)

## Overview
Built an AI-assisted debugging system for embedded SPI communication logs that automates fault detection and root cause analysis using vector embeddings and retrieval-based reasoning.

##Problem
Manual SPI log debugging is time-consuming and error-prone, especially when dealing with undocumented protocols and hardware-level failures.

##Solution
- Parsed raw SPI logs
- Converted logs into embeddings
- Stored in vector database (ChromaDB)
- Retrieved similar historical failures
- Generated automated diagnosis

## architecture
Parser → Embeddings → Vector DB → Retrieval → Diagnosis

##Sample Output
<img width="1472" height="634" alt="image" src="https://github.com/user-attachments/assets/35581b0b-c259-4e25-9a64-1c7be5441ebb" />
<img width="987" height="451" alt="image" src="https://github.com/user-attachments/assets/4d5ffa54-6a40-4e84-aaf5-28efdb1a584d" />
