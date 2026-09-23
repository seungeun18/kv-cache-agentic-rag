from typing import TypedDict


class AgentState(TypedDict, total=False):

    # Human-selected technologies
    technologies: list[str]

    # Market Agent outputs
    market_results: dict

    # Domain Agent outputs
    domain_results: dict

    # Final report
    final_report: str
