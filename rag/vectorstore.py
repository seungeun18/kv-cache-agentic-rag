from pathlib import Path

from langchain_community.vectorstores import FAISS

from rag.chunker import build_chunks
from rag.embeddings import get_embeddings


VECTORSTORE_PATH = "data/vectorstore/faiss_index"


def build_vectorstore():
    print("[1/3] Loading and chunking documents...")
    chunks = build_chunks()

    print("[2/3] Loading embedding model...")
    embeddings = get_embeddings()

    print("[3/3] Building FAISS vector store...")

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    Path("data/vectorstore").mkdir(
        parents=True,
        exist_ok=True,
    )

    vectorstore.save_local(VECTORSTORE_PATH)

    print("\n[SUCCESS] Vector store created")
    print(f"Saved to: {VECTORSTORE_PATH}")
    print(f"Chunks indexed: {len(chunks)}")

    return vectorstore


def load_vectorstore():
    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vectorstore


if __name__ == "__main__":
    build_vectorstore()
