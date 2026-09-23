from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.loader import load_all_documents


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def split_documents(documents):
    """
    PDF Document를 검색 가능한 chunk 단위로 분할한다.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
    )

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    print(f"[CHUNK] Original documents: {len(documents)}")
    print(f"[CHUNK] Generated chunks: {len(chunks)}")

    return chunks


def build_chunks():
    documents = load_all_documents()
    return split_documents(documents)


if __name__ == "__main__":
    chunks = build_chunks()

    print("\n--- First Chunk Metadata ---")
    print(chunks[0].metadata)

    print("\n--- First Chunk ---")
    print(chunks[0].page_content[:1000])
