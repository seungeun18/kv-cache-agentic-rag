from agents.llm import get_llm
from rag.retriever import retrieve_documents, format_context


MARKET_QUERY = """
Evaluate the market applicability of {technology} for large-scale
LLM serving.

Focus on:
- deployment complexity
- compatibility with existing GPU infrastructure
- additional hardware requirements
- operational cost implications
- scalability
- commercialization and adoption barriers
"""


def analyze_market(technology: str) -> dict:
    """
    Human이 이미 선정한 기술을 시장성 관점에서 평가한다.
    기술 선정은 수행하지 않는다.
    """

    query = MARKET_QUERY.format(
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
You are the Market Evaluation Agent.

The technologies were already selected by humans.
DO NOT select, rank, or recommend technologies.

Technology to evaluate:
{technology}

Evaluate only from the MARKET APPLICABILITY perspective.

Evaluation criteria:
1. Deployment complexity
2. Compatibility with existing GPU/software infrastructure
3. Need for additional hardware or system changes
4. Operational and infrastructure cost implications
5. Scalability for commercial LLM serving
6. Commercialization or adoption barriers

Use ONLY claims supported by the supplied evidence.
If the evidence is insufficient for a market claim,
explicitly state "Insufficient evidence".

Distinguish:
- directly supported technical evidence
- reasonable market implication/inference

Do not declare the technology superior to the other technology.

Evidence:
----------------
{context}
----------------

Write the result in Korean.

Output structure:

## {technology} 시장성 평가

### 1. 기존 인프라 호환성
...

### 2. 도입 복잡도
...

### 3. 비용 및 운영 영향
...

### 4. 확장성
...

### 5. 상용화 및 채택 장벽
...

### 시장성 관점 요약
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
