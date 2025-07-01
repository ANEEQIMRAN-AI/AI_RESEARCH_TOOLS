# nodes_workflow.py
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from LLM import rephrase_chain, humanized_chain, grammar_chain

class ParaphraserState(TypedDict):
    input_paragraph: str
    rephrased_paragraph: str
    humanized_paragraph: str
    final_output: str

def rephrase_node(state):
    response = rephrase_chain.invoke({"input_paragraph": state["input_paragraph"]})
    return {"rephrased_paragraph": response.content}

def humanize_node(state):
    response = humanized_chain.invoke({"rephrased_paragraph": state["rephrased_paragraph"]})
    return {"humanized_paragraph": response.content}

def grammar_node(state):
    response = grammar_chain.invoke({"humanized_paragraph": state["humanized_paragraph"]})
    return {"final_output": response.content}

def create_workflow():
    graph = StateGraph(ParaphraserState)
    graph.add_node("REPHRASE", RunnableLambda(rephrase_node))
    graph.add_node("HUMANIZE", RunnableLambda(humanize_node))
    graph.add_node("GRAMMAR", RunnableLambda(grammar_node))
    
    graph.set_entry_point("REPHRASE")
    graph.add_edge("REPHRASE", "HUMANIZE")
    graph.add_edge("HUMANIZE", "GRAMMAR")
    graph.add_edge("GRAMMAR", END)
    
    return graph.compile()