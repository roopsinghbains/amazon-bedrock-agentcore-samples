#!/usr/bin/env python3

import logging
from typing import Any, Dict, List, Literal

from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from langgraph.graph import END, StateGraph

from .agent_nodes import (
    create_kubernetes_agent,
    create_logs_agent,
    create_metrics_agent,
    create_runbooks_agent,
)
from .agent_state import AgentState
from .supervisor import SupervisorAgent

# Configure logging with basicConfig
logging.basicConfig(
    level=logging.INFO,  # Set the log level to INFO
    # Define log message format
    format="%(asctime)s,p%(process)s,{%(filename)s:%(lineno)d},%(levelname)s,%(message)s",
)

logger = logging.getLogger(__name__)


def _should_continue(state: AgentState) -> Literal["supervisor", "FINISH"]:
    """Determine if we should continue or finish."""
    next_agent = state.get("next", "FINISH")

    if next_agent == "FINISH":
        return "FINISH"

    # Check if we've already invoked this agent (avoid loops)
    agents_invoked = state.get("agents_invoked", [])
    if next_agent in agents_invoked and not state.get("requires_collaboration", False):
        logger.warning(f"Agent {next_agent} already invoked, finishing to avoid loop")
        return "FINISH"

    return "supervisor"


def _route_supervisor(state: AgentState) -> str:
    """Route from supervisor to the appropriate agent or finish."""
    next_agent = state.get("next", "FINISH")

    if next_agent == "FINISH":
        return "aggregate"

    # Map to actual node names
    agent_map = {
        "kubernetes": "kubernetes_agent",
        "logs": "logs_agent",
        "metrics": "metrics_agent",
        "runbooks": "runbooks_agent",
    }

    return agent_map.get(next_agent, "aggregate")


async def _prepare_initial_state(state: AgentState) -> Dict[str, Any]:
    """Prepare the initial state with the user's query."""
    messages = state.get("messages", [])

    # Extract the current query from the last human message
    current_query = ""
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            current_query = msg.content
            break

    return {
        "current_query": current_query,
        "agent_results": {},
        "agents_invoked": [],
        "requires_collaboration": False,
        "metadata": {},
    }


def build_multi_agent_graph(
    tools: List[BaseTool], llm_provider: str = "anthropic", **llm_kwargs
) -> StateGraph:
    """Build the multi-agent collaboration graph.

    Args:
        tools: List of all available tools
        llm_provider: LLM provider to use
        **llm_kwargs: Additional arguments for LLM

    Returns:
        Compiled StateGraph for multi-agent collaboration
    """
    logger.info("Building multi-agent collaboration graph")

    # Create the state graph
    workflow = StateGraph(AgentState)

    # Create supervisor
    supervisor = SupervisorAgent(llm_provider=llm_provider, **llm_kwargs)

    # Create agent nodes with filtered tools
    kubernetes_agent = create_kubernetes_agent(
        tools, llm_provider=llm_provider, **llm_kwargs
    )
    logs_agent = create_logs_agent(tools, llm_provider=llm_provider, **llm_kwargs)
    metrics_agent = create_metrics_agent(tools, llm_provider=llm_provider, **llm_kwargs)
    runbooks_agent = create_runbooks_agent(
        tools, llm_provider=llm_provider, **llm_kwargs
    )

    # Add nodes to the graph
    workflow.add_node("prepare", _prepare_initial_state)
    workflow.add_node("supervisor", supervisor.route)
    workflow.add_node("kubernetes_agent", kubernetes_agent)
    workflow.add_node("logs_agent", logs_agent)
    workflow.add_node("metrics_agent", metrics_agent)
    workflow.add_node("runbooks_agent", runbooks_agent)
    workflow.add_node("aggregate", supervisor.aggregate_responses)

    # Set entry point
    workflow.set_entry_point("prepare")

    # Add edges from prepare to supervisor
    workflow.add_edge("prepare", "supervisor")

    # Add conditional edges from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        _route_supervisor,
        {
            "kubernetes_agent": "kubernetes_agent",
            "logs_agent": "logs_agent",
            "metrics_agent": "metrics_agent",
            "runbooks_agent": "runbooks_agent",
            "aggregate": "aggregate",
        },
    )

    # Add edges from agents back to supervisor
    workflow.add_edge("kubernetes_agent", "supervisor")
    workflow.add_edge("logs_agent", "supervisor")
    workflow.add_edge("metrics_agent", "supervisor")
    workflow.add_edge("runbooks_agent", "supervisor")

    # Add edge from aggregate to END
    workflow.add_edge("aggregate", END)

    # Compile the graph
    compiled_graph = workflow.compile()

    logger.info("Multi-agent collaboration graph built successfully")
    return compiled_graph
