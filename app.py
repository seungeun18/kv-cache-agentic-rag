from pathlib import Path

from graph.workflow import build_graph


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = PROJECT_ROOT / "outputs/final_report.md"


def main():

    print("=" * 70)
    print("KV Cache Multi-Agent Evaluation")
    print("=" * 70)

    print("\nTechnology selection method: Human-based")
    print("SW Technology : KIVI")
    print("HW Technology : InfiniGen")

    graph = build_graph()

    initial_state = {
        "technologies": [
            "KIVI",
            "InfiniGen",
        ]
    }

    print("\n[START] Running LangGraph workflow...")

    result = graph.invoke(
    initial_state,
    config={"max_concurrency": 1},
    )

    report = result["final_report"]

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        report,
        encoding="utf-8",
    )

    print("\n[SUCCESS]")
    print(
        f"Final report saved to: {OUTPUT_PATH}"
    )

    print("\n" + "=" * 70)
    print(report)
    print("=" * 70)


if __name__ == "__main__":
    main()
