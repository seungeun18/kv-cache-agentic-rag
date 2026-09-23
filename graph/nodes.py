from agents.market_agent import analyze_market
from agents.domain_agent import analyze_domain
from agents.report_agent import generate_report


TECHNOLOGIES = [
    "KIVI",
    "InfiniGen",
]


def market_node(state):

    print("\n[AGENT] Market Evaluation Agent")

    results = {}

    for technology in TECHNOLOGIES:

        print(
            f"[Market] Analyzing {technology}..."
        )

        results[technology] = analyze_market(
            technology
        )

    return {
        "market_results": results
    }


def domain_node(state):

    print("\n[AGENT] Domain Evaluation Agent")

    results = {}

    for technology in TECHNOLOGIES:

        print(
            f"[Domain] Analyzing {technology}..."
        )

        results[technology] = analyze_domain(
            technology
        )

    return {
        "domain_results": results
    }


def report_node(state):

    print("\n[AGENT] Final Report Agent")

    report = generate_report(
        market_results=state["market_results"],
        domain_results=state["domain_results"],
    )

    return {
        "final_report": report
    }
