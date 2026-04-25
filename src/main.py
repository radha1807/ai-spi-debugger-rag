import os
import json

from parser import parse_logs
from embedding import generate_embeddings
from retrieval import store_embeddings, retrieve_similar

print("FILE STARTED")


def simple_diagnosis(log):
    if "ERR" in log:
        return "Possible SPI communication failure (timing mismatch or noise issue)"
    elif "TIMEOUT" in log:
        return "Slave device not responding (check wiring / clock / chip select)"
    else:
        return "Normal operation"


def main():
    print("MAIN FUNCTION STARTED")

    # ✅ Fix file path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(BASE_DIR, "data", "sample_logs.txt")

    print("LOG PATH:", log_path)

    # ✅ Step 1: Parse logs
    logs = parse_logs(log_path)
    print("LOGS:", logs)

    if not logs:
        print("No logs found. Check your file.")
        return

    # ✅ Step 2: Generate embeddings
    embeddings = generate_embeddings(logs)
    print("Embeddings generated")

    # ✅ Step 3: Store embeddings
    store_embeddings(logs, embeddings)
    print("Stored in DB")

    # ✅ Step 4: Process logs
    results = []

    for log, emb in zip(logs, embeddings):
        print("\n====================")
        print("LOG:", log["raw"])

        similar = retrieve_similar(emb)
        print("SIMILAR CASES:", similar)

        diagnosis = simple_diagnosis(log["raw"])
        print("DIAGNOSIS:", diagnosis)

        results.append({
            "log": log["raw"],
            "diagnosis": diagnosis
        })

    # ✅ Step 5: Save results to file
    output_path = os.path.join(BASE_DIR, "outputs", "results.json")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)

    print("\nResults saved to:", output_path)


# ✅ ENTRY POINT (MANDATORY)
if __name__ == "__main__":
    main()