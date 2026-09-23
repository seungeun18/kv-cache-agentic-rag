"""Exercise RAG retrieval and LangGraph orchestration without an LLM API."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import graph.nodes as nodes
from agents.domain_agent import DOMAIN_QUERY
from agents.market_agent import MARKET_QUERY
from graph.workflow import build_graph
from rag.retriever import retrieve_documents


OUTPUT_PATH = PROJECT_ROOT / "outputs/offline_smoke_report.md"
TECHNOLOGIES = ("KIVI", "InfiniGen")


def _result(technology: str, query: str, perspective: str) -> dict:
    documents = retrieve_documents(
        query=query.format(technology=technology),
        technology=technology,
        k=3,
    )

    if not documents:
        raise RuntimeError(f"No documents retrieved for {technology}")

    sources = [
        {
            "technology": document.metadata.get("technology"),
            "source": document.metadata.get("source_file"),
            "page": document.metadata.get("page", 0) + 1,
        }
        for document in documents
    ]

    return {
        "technology": technology,
        "analysis": (
            f"{technology} {perspective} offline smoke result: "
            f"retrieved {len(documents)} evidence chunks."
        ),
        "sources": sources,
    }


def offline_market(technology: str) -> dict:
    return _result(technology, MARKET_QUERY, "market")


def offline_domain(technology: str) -> dict:
    return _result(technology, DOMAIN_QUERY, "domain")


def offline_report(market_results: dict, domain_results: dict) -> str:
    lines = [
        "# Offline Smoke Report",
        "",
        "This file verifies local RAG retrieval and LangGraph orchestration.",
        "It is not the final LLM-generated evaluation report.",
    ]

    for technology in TECHNOLOGIES:
        lines.extend(
            [
                "",
                f"## {technology}",
                "",
                market_results[technology]["analysis"],
                "",
                domain_results[technology]["analysis"],
                "",
                "Retrieved sources:",
            ]
        )

        seen = set()
        sources = (
            market_results[technology]["sources"]
            + domain_results[technology]["sources"]
        )
        for source in sources:
            identity = (source["source"], source["page"])
            if identity not in seen:
                seen.add(identity)
                lines.append(f"- {source['source']}, page {source['page']}")

    return "\n".join(lines) + "\n"


def main() -> None:
    nodes.analyze_market = offline_market
    nodes.analyze_domain = offline_domain
    nodes.generate_report = offline_report

    result = build_graph().invoke({"technologies": list(TECHNOLOGIES)})

    if set(result["market_results"]) != set(TECHNOLOGIES):
        raise RuntimeError("Market node did not return both technologies")
    if set(result["domain_results"]) != set(TECHNOLOGIES):
        raise RuntimeError("Domain node did not return both technologies")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(result["final_report"], encoding="utf-8")

    print("OFFLINE_SMOKE_OK")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
