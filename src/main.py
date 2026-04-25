import os
import json
import argparse

from parser import parse_logs
from embeddings import generate_embeddings
from retrieval import store_embeddings, retrieve_similar, clear_collection
from llm_inference import get_root_cause


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_knowledge_base(kb_path: str):
    """
    Index the knowledge base (historical known failures) into ChromaDB.
    This is separate from the query logs — avoids self-retrieval.
    Run once, or re-run with --reindex to refresh.
    """
    print(f"\n[KB] Loading knowledge base from: {kb_path}")
    kb_logs = parse_logs(kb_path)
    if not kb_logs:
        print("[KB] WARNING: No knowledge base logs found. RAG will have no context.")
        return
    kb_embeddings = generate_embeddings(kb_logs)
    store_embeddings(kb_logs, kb_embeddings, id_prefix="kb")
    print(f"[KB] Indexed {len(kb_logs)} knowledge base entries.")


def run_pipeline(query_log_path: str, output_path: str):
    """
    Main RAG pipeline:
    1. Parse query logs
    2. Embed them
    3. Retrieve similar cases from KB
    4. Send log + similar cases to LLM
    5. Save structured results
    """
    print(f"\n[PIPELINE] Processing query logs: {query_log_path}")
    logs = parse_logs(query_log_path)
    if not logs:
        print("[PIPELINE] No logs found. Exiting.")
        return

    embeddings = generate_embeddings(logs)
    print(f"[PIPELINE] Generated embeddings for {len(logs)} logs.")

    results = []
    for i, (log, emb) in enumerate(zip(logs, embeddings)):
        print(f"\n[{i+1}/{len(logs)}] Log: {log['raw'][:80]}")

        # Retrieve from KB only — exclude self by using a separate ID namespace
        similar_cases = retrieve_similar(emb, n_results=3)
        print(f"  Similar cases found: {len(similar_cases)}")

        # Full RAG: LLM uses the log + retrieved context
        diagnosis = get_root_cause(log["raw"], similar_cases)
        print(f"  Diagnosis:\n{diagnosis}")

        results.append({
            "log": log["raw"],
            "status": log["status"],
            "similar_cases": similar_cases,
            "diagnosis": diagnosis
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"\n[DONE] Results saved to: {output_path}")
    _print_summary(results)


def _print_summary(results: list):
    """Print a quick accuracy summary if ground truth labels exist."""
    total = len(results)
    errors = sum(1 for r in results if r["status"] == "ERROR")
    timeouts = sum(1 for r in results if r["status"] == "TIMEOUT")
    ok = sum(1 for r in results if r["status"] == "OK")

    print("\n===== SUMMARY =====")
    print(f"Total logs processed : {total}")
    print(f"  ERROR              : {errors}")
    print(f"  TIMEOUT            : {timeouts}")
    print(f"  OK                 : {ok}")
    print("===================\n")


def main():
    parser_arg = argparse.ArgumentParser(description="SPI Log RAG Debugger")
    parser_arg.add_argument(
        "--reindex", action="store_true",
        help="Clear and re-index the knowledge base from scratch."
    )
    parser_arg.add_argument(
        "--kb", type=str,
        default=os.path.join(BASE_DIR, "data", "knowledge_base.txt"),
        help="Path to knowledge base log file."
    )
    parser_arg.add_argument(
        "--logs", type=str,
        default=os.path.join(BASE_DIR, "data", "sample_logs.txt"),
        help="Path to query log file to diagnose."
    )
    parser_arg.add_argument(
        "--output", type=str,
        default=os.path.join(BASE_DIR, "outputs", "results.json"),
        help="Path for output JSON results."
    )
    args = parser_arg.parse_args()

    if args.reindex:
        print("[REINDEX] Clearing existing knowledge base...")
        clear_collection()

    load_knowledge_base(args.kb)
    run_pipeline(args.logs, args.output)


if __name__ == "__main__":
    main()
