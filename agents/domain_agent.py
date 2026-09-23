from agents.llm import get_llm
from rag.retriever import retrieve_documents, format_context


DOMAIN_QUERY = """
Evaluate {technology} for data center and cloud-based
long-context LLM serving.

Focus on:
- GPU HBM usage
- throughput
- latency
- long-context scalability
- accuracy or quality impact
- CPU-GPU data movement
- multi-user serving
"""


def analyze_domain(technology: str) -> dict:
    """
    Human이 이미 선정한 기술을
    데이터센터/클라우드 LLM Serving 관점에서 평가한다.
    """

    query = DOMAIN_QUERY.format(
        technology=technology
    )

    docs = retrieve_documents(
        query=query,
        technology=technology,
        k=5,
    )

    context = format_context(docs)

    llm = get_llm()

    prompt = f"""
You are the Domain Evaluation Agent.

The technologies were already selected by humans.
DO NOT select, rank, or recommend technologies.

Technology:
{technology}

Target domain:
Data center / cloud-based long-context LLM serving

Evaluate only the DOMAIN APPLICABILITY.

Evaluation criteria:
1. GPU HBM memory efficiency
2. Throughput
3. Latency
4. Long-context scalability
5. Accuracy / model quality impact
6. CPU-GPU or memory data movement
7. Multi-user / batch serving applicability
8. Infrastructure modification requirements

All factual claims must be grounded in the supplied evidence.

If evidence is insufficient, explicitly state that limitation.

Do not determine which technology is better.

Evidence:
----------------
{context}
----------------

Write the result in Korean.

Output structure:

## {technology} 도메인 적용성 평가

### 1. HBM 및 메모리 효율
...

### 2. Throughput / Latency
...

### 3. 장문맥 확장성
...

### 4. 정확도 및 품질 영향
...

### 5. 데이터 이동 및 시스템 구조
...

### 6. Cloud LLM Serving 적용 시 고려사항
...

### 도메인 관점 요약
...
"""

    response = llm.invoke(prompt)

    sources = [
        {
            "technology": doc.metadata.get("technology"),
            "source": doc.metadata.get("source_file"),
            "page": doc.metadata.get("page", 0) + 1,
        }
        for doc in docs
    ]

    return {
        "technology": technology,
        "analysis": response.content,
        "sources": sources,
    }
