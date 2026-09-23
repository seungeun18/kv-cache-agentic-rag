from langchain_huggingface import HuggingFaceEmbeddings

MODEL_NAME = "Alibaba-NLP/gte-multilingual-base"


def get_embeddings():
    """
    오픈소스 multilingual embedding 모델을 반환한다.
    한국어 질의와 영어 논문 간 semantic retrieval을 지원한다.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={
            "device": "cpu",
            "trust_remote_code": True,
        },
        encode_kwargs={
            "normalize_embeddings": True
        },
    )

    return embeddings


if __name__ == "__main__":
    print("[TEST] Loading embedding model...")

    embedding_model = get_embeddings()

    test_text = "KIVI reduces KV cache memory using quantization."

    vector = embedding_model.embed_query(test_text)

    print(f"[SUCCESS] Embedding Model: {MODEL_NAME}")
    print(f"Vector dimension: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")
