from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_pdf(pdf_path: str, technology: str):
    """
    PDF를 페이지 단위 Document로 로드하고
    technology / source_file metadata를 추가한다.
    """
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    loader = PyPDFLoader(str(path))
    documents = loader.load()

    for doc in documents:
        doc.metadata["technology"] = technology
        doc.metadata["source_file"] = path.name

    print(
        f"[LOAD] {technology}: "
        f"{len(documents)} pages loaded from {path.name}"
    )

    return documents


def load_all_documents():
    kivi_docs = load_pdf(
        PROJECT_ROOT / "data/raw/kivi.pdf",
        technology="KIVI"
    )

    infinigen_docs = load_pdf(
        PROJECT_ROOT / "data/raw/infinigen.pdf",
        technology="InfiniGen"
    )

    return kivi_docs + infinigen_docs


if __name__ == "__main__":
    docs = load_all_documents()

    print(f"\nTotal pages: {len(docs)}")

    print("\n--- First Document Metadata ---")
    print(docs[0].metadata)

    print("\n--- First Document Preview ---")
    print(docs[0].page_content[:500])
