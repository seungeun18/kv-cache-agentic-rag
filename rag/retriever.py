from rag.vectorstore import load_vectorstore


TOP_K = 4


def retrieve_documents(
    query: str,
    technology: str | None = None,
    k: int = TOP_K,
):
    """
    이미 Human이 선정한 KIVI / InfiniGen 문서에서
    질의와 관련된 근거 chunk를 검색한다.

    이 모듈은 기술을 선정하지 않는다.
    """

    vectorstore = load_vectorstore()

    if technology:
        results = vectorstore.similarity_search(
            query,
            k=k,
            filter={"technology": technology},
        )
    else:
        results = vectorstore.similarity_search(
            query,
            k=k,
        )

    return results


def format_context(documents):
    """
    검색 결과를 LLM Agent에 전달하기 위한
    텍스트 context로 변환한다.
    """

    contexts = []

    for i, doc in enumerate(documents, start=1):
        technology = doc.metadata.get("technology", "Unknown")
        source = doc.metadata.get("source_file", "Unknown")
        page = doc.metadata.get("page")

        page_text = str(page + 1) if page is not None else "N/A"

        contexts.append(
            f"""
[Evidence {i}]
Technology: {technology}
Source: {source}
Page: {page_text}

{doc.page_content}
""".strip()
        )

    return "\n\n".join(contexts)


def print_results(results):
    for i, doc in enumerate(results, start=1):

        print("\n" + "=" * 80)
        print(f"RESULT {i}")
        print("=" * 80)

        print(
            f"Technology: "
            f"{doc.metadata.get('technology')}"
        )

        print(
            f"Source: "
            f"{doc.metadata.get('source_file')}"
        )

        page = doc.metadata.get("page")

        if page is not None:
            print(f"Page: {page + 1}")

        print("\nContent:")
        print(doc.page_content[:1200])


if __name__ == "__main__":

    query = (
        "How does KIVI reduce KV cache memory "
        "and how are keys and values quantized?"
    )

    print(f"\nQuery: {query}")

    results = retrieve_documents(
        query=query,
        technology="KIVI",
        k=4,
    )

    print_results(results)
