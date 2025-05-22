from typing import Dict, Any, Optional, List
from app.services.wireframe.agents import query_expansion_agent, requirement_gathering_agent, svg_generator_agent, wireframe_planning_agent
from pydantic import BaseModel

from langgraph.graph import StateGraph, START, END

from app.models.wireframe import WireframeState

def create_wireframe_graph():
    """

    Create the LangGraph for wireframe generation.
    
    Returns:
        Compiled graph for wireframe generation

    """

    workflow = StateGraph(WireframeState)

    # add nodes to the graph
    workflow.add_node("Query_Expansion", query_expansion_agent)    
    workflow.add_node("Requirement_Gathering", requirement_gathering_agent)
    workflow.add_node("Wireframe_Planning", wireframe_planning_agent)
    workflow.add_node("SVG_Generation", svg_generator_agent)

    # add edges to the graph
    workflow.add_edge(START, "Query_Expansion")
    workflow.add_edge("Query_Expansion", "Requirement_Gathering")
    workflow.add_edge("Requirement_Gathering", "Wireframe_Planning")
    workflow.add_edge("Wireframe_Planning", "SVG_Generation")
    workflow.add_edge("SVG_Generation", END)

    # compile the graph 
    return workflow.compile()


def generate_wireframe(user_query: str) -> Optional[Dict[str, Any]]:
    """
    Generate a wireframe from a user query.
    
    Args:
        user_query: The user's description of the desired wireframe
        
    Returns:
        State containing the generated wireframe and intermediary data
    """
    # create graph
    graph = create_wireframe_graph()

    #initial state of the graph
    initial_state = {
        "user_query": user_query,
        "original_query": None,
        "detailed_requirements": None,
        "wireframe_plan": None,
        "svg_code": None,
        "errors": []
    }

    # run the graph
    try:
        result = graph.invoke(initial_state)
        return result
    
    except Exception as e:
        return {
            **initial_state,
            "errors": [f"Failed to generate wireframe: {str(e)}"]
        }