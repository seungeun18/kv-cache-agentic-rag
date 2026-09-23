import json

from rag.retriever import retrieve_documents


TEST_FILE = "evaluation/test_queries.json"


def evaluate_retrieval(k=4):

    with open(TEST_FILE, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    passed = 0
    total = len(test_cases)

    print("\n=== Retrieval Evaluation ===\n")

    for case in test_cases:

        results = retrieve_documents(
            query=case["query"],
            technology=case["technology"],
            k=k,
        )

        combined_text = " ".join(
            doc.page_content.lower()
            for doc in results
        )

        keywords = [
            keyword.lower()
            for keyword in case["expected_keywords"]
        ]

        matched = [
            keyword
            for keyword in keywords
            if keyword in combined_text
        ]

        success = len(matched) > 0

        if success:
            passed += 1

        status = "PASS" if success else "FAIL"

        print(
            f"{case['id']} | "
            f"{status} | "
            f"matched={matched}"
        )

    score = passed / total if total else 0

    print("\n----------------------------")
    print(f"Passed: {passed}/{total}")
    print(f"Hit Rate@{k}: {score:.3f}")
    print("----------------------------")

    return score


if __name__ == "__main__":
    evaluate_retrieval(k=4)
