# nodes_workflow.py
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from LLM import llm, essay_prompt, humanizer_prompt, grammar_prompt

class EssayState(TypedDict):
    topic: str
    essay: str
    humanized_essay: str
    final_output: str

def generate_essay(state):
    topic = state["topic"]
    essay = llm.invoke(essay_prompt.format(topic=topic))
    return {"topic": topic, "essay": essay}

def humanize_essay(state):
    essay = state["essay"]
    humanized = llm.invoke(humanizer_prompt.format(essay=essay))
    return {"topic": state["topic"], "essay": essay, "humanized_essay": humanized}

def correct_grammar(state):
    humanized = state["humanized_essay"]
    corrected = llm.invoke(grammar_prompt.format(humanized_essay=humanized))
    return {"final_output": corrected}

def create_workflow():
    graph = StateGraph(EssayState)
    graph.add_node("GenerateEssay", RunnableLambda(generate_essay))
    graph.add_node("HumanizeEssay", RunnableLambda(humanize_essay))
    graph.add_node("GrammarCorrect", RunnableLambda(correct_grammar))
    graph.set_entry_point("GenerateEssay")
    graph.add_edge("GenerateEssay", "HumanizeEssay")
    graph.add_edge("HumanizeEssay", "GrammarCorrect")
    graph.add_edge("GrammarCorrect", END)
    return graph.compile()