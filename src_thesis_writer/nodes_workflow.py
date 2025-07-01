# nodes_workflow.py
from langgraph.graph import StateGraph, END
from LLM import thesis_agent, humanize_agent, grammar_agent

def thesis_node(state):
    topic = state.get("topic")
    if not topic:
        raise ValueError("Missing 'topic' in state.")
    thesis_list = thesis_agent.invoke({"topic": topic}).content
    return {**state, "thesis_list": thesis_list}

def human_node(state):
    thesis_list = state.get("thesis_list")
    human_thesis = humanize_agent.invoke({"thesis_list": thesis_list}).content
    return {**state, "thesis_list": human_thesis}

def grammar_node(state):
    thesis_list = state.get("thesis_list")
    final_thesis = grammar_agent.invoke({"thesis_list": thesis_list}).content
    return {**state, "thesis_list": final_thesis}

def create_workflow():
    workflow = StateGraph(dict)
    workflow.add_node("LLM_THESIS", thesis_node)
    workflow.add_node("HUMANIZED", human_node)
    workflow.add_node("GRAMMAR", grammar_node)
    workflow.set_entry_point("LLM_THESIS")
    workflow.add_edge("LLM_THESIS", "HUMANIZED")
    workflow.add_edge("HUMANIZED", "GRAMMAR")
    workflow.add_edge("GRAMMAR", END)
    return workflow.compile()