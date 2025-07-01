# PARAPHRASER AGENT USING LANGCHAIN + LANGGRAPH

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
import streamlit as st
import PyPDF2
from typing import TypedDict

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=gemini_api_key,
    temperature=0.7,
    max_tokens=3000
)

# --- PROMPTS ---

# Step 1: Rephrase the Paragraph
rephrase_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional rephrasing assistant. Rephrase the following paragraph without losing the original meaning. Avoid plagiarism and redundancy."),
    ("human", "{input_paragraph}")
])

# Step 2: Humanized Agent
humanize_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a humanization expert. Make the following text sound extremely natural, fluent, and written by a native speaker. Make it engaging and polished."),
    ("human", "{rephrased_paragraph}")
])

# Step 3: Grammar Agent
grammar_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a grammar correction expert. Correct all grammatical, punctuation, and structural errors in the following text without altering its meaning or tone."),
    ("human", "{humanized_paragraph}")
])

# --- AGENTS ---

# Rephraser Agent
rephrase_chain = rephrase_prompt | llm

# Humanized Agent
humanized_chain = humanize_prompt | llm

# Grammar Agent
grammar_chain = grammar_prompt | llm

# --- STATE DEFINITION ---

class ParaphraserState(TypedDict):
    input_paragraph: str
    rephrased_paragraph: str
    humanized_paragraph: str
    final_output: str

# --- NODE FUNCTIONS ---

def rephrase_node(state):
    response = rephrase_chain.invoke({"input_paragraph": state["input_paragraph"]})
    return {"rephrased_paragraph": response.content}

def humanize_node(state):
    response = humanized_chain.invoke({"rephrased_paragraph": state["rephrased_paragraph"]})
    return {"humanized_paragraph": response.content}

def grammar_node(state):
    response = grammar_chain.invoke({"humanized_paragraph": state["humanized_paragraph"]})
    return {"final_output": response.content}

# --- GRAPH DEFINITION ---
graph = StateGraph(ParaphraserState)
graph.add_node("REPHRASE", RunnableLambda(rephrase_node))
graph.add_node("HUMANIZE", RunnableLambda(humanize_node))
graph.add_node("GRAMMAR", RunnableLambda(grammar_node))

graph.set_entry_point("REPHRASE")
graph.add_edge("REPHRASE", "HUMANIZE")
graph.add_edge("HUMANIZE", "GRAMMAR")
graph.add_edge("GRAMMAR", END)

paraphraser_app = graph.compile()

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Paraphraser", layout="wide")

col_input, col_output = st.columns(2)

with col_input:
    st.markdown("## AI Paraphraser")

    # Text input area with persistent state
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        st.session_state.input_text = pdf_text

    input_value = st.text_area("", placeholder="Start typing or paste text here...", height=200, value=st.session_state.input_text, key="text_area")
    st.session_state.input_text = input_value

    st.markdown(f"**Word Count:** {len(st.session_state.input_text.split())}")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("Clear"):
            st.session_state.input_text = ""
            st.session_state.final_output = ""
    with col_b:
        if st.button("Paraphrase"):
            if st.session_state.input_text.strip():
                with st.spinner("Processing..."):
                    result = paraphraser_app.invoke({"input_paragraph": st.session_state.input_text})
                    st.session_state.final_output = result["final_output"]
            else:
                st.warning("Please enter a paragraph to paraphrase.")

with col_output:
    st.markdown("## Result")
    if "final_output" in st.session_state and st.session_state.final_output:
        st.text_area("", value=st.session_state.final_output, height=500, key="result_output")
        st.button("Copy", on_click=lambda: st.toast("Copied to clipboard!"))
