from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from graph.state import AgentState

from graph.nodes import (
    market_node,
    domain_node,
    report_node,
)


def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node(
        "market_agent",
        market_node,
    )

    builder.add_node(
        "domain_agent",
        domain_node,
    )

    builder.add_node(
        "report_agent",
        report_node,
    )

    # Fan-out
    builder.add_edge(
        START,
        "market_agent",
    )

    builder.add_edge(
        START,
        "domain_agent",
    )

    # Fan-in
    builder.add_edge(
        "market_agent",
        "report_agent",
    )

    builder.add_edge(
        "domain_agent",
        "report_agent",
    )

    builder.add_edge(
        "report_agent",
        END,
    )

    return builder.compile()


if __name__ == "__main__":

    graph = build_graph()

    print(
        "LangGraph workflow created successfully."
    )
