# thesis_agent_generator.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langgraph.graph import StateGraph, END
import streamlit as st
from langchain.utilities import GoogleSearchAPIWrapper

# Load API Key
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)
gemini_api_key = os.getenv("GOOGLE_API_KEY")
google_search_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=gemini_api_key,
    temperature=0.7,
    max_tokens=2048
)

# -------------------- PROMPTS ----------------------
thesis_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
You are a professional academic writing expert. Generate a list of 10 strong, diverse, and arguable thesis statements based on the following topic. 
Each thesis statement must include:
- A **clear topic** (the subject of the essay)
- A **specific claim** (the writer's argument or position)
- **Major points** that will be developed in the body of the essay

Structure each thesis like this:
[Topic] + [Claim] + [Major Points]

TOPIC: {topic}

List of 10 Structured Thesis Statements:
"""
)

humanize_prompt = PromptTemplate(
    input_variables=["thesis_list"],
    template="""
You are a human writing assistant. Take the following list of thesis statements and humanize them. Make each one sound fluent, natural, and as if written by an academic expert. Maintain the original structure and meaning.

THESIS STATEMENTS:
{thesis_list}

HUMANIZED THESIS STATEMENTS:
"""
)

grammar_prompt = PromptTemplate(
    input_variables=["thesis_list"],
    template="""
You are a grammar expert. Review the following list of thesis statements for grammar, clarity, and fluency. Correct any mistakes without changing the intended structure and meaning.

THESIS STATEMENTS:
{thesis_list}

CORRECTED THESIS STATEMENTS:
"""
)

# ------------------- AGENTS -----------------------
thesis_agent = thesis_prompt | llm
humanize_agent = humanize_prompt | llm
grammar_agent = grammar_prompt | llm

# ------------------ LANGGRAPH ----------------------
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

workflow = StateGraph(dict)
workflow.add_node("LLM_THESIS", thesis_node)
workflow.add_node("HUMANIZED", human_node)
workflow.add_node("GRAMMAR", grammar_node)
workflow.set_entry_point("LLM_THESIS")
workflow.add_edge("LLM_THESIS", "HUMANIZED")
workflow.add_edge("HUMANIZED", "GRAMMAR")
workflow.add_edge("GRAMMAR", END)

graph_executor = workflow.compile()

# ------------------ ARTICLE FETCHING TOOL ----------------------
def fetch_related_articles(topic):
    search = GoogleSearchAPIWrapper(
        google_api_key=google_search_api_key,
        google_cse_id=google_cse_id
    )
    query = f"{topic} research paper"
    results = search.results(query, num_results=10)
    return [f"[{item['title']}]({item['link']})" for item in results]

# ------------------ STREAMLIT UI ----------------------
st.set_page_config(page_title="Thesis Statement Generator", layout="wide")
st.title("🎓 Thesis Statement Generator")

with st.container():
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Thesis Generator")
        thesis_topic = st.text_input("Thesis topic:", placeholder="ex: Impact of consuming junk food")
        main_idea = st.text_input("Main idea about topic (optional):", placeholder="ex: Junk food is bad for the body")
        reason = st.text_input("Reason supporting main idea (optional):", placeholder="ex: Junk food creates health issues")
        audience = st.text_input("Intended audience (optional):", placeholder="ex: College students")

        colA, colB = st.columns([1, 1])
        with colA:
            if st.button("Clear Inputs"):
                st.experimental_rerun()

        with colB:
            generate = st.button("Generate")

    with col2:
        st.header("Result")
        result_placeholder = st.empty()

    if generate:
        if thesis_topic.strip() == "":
            st.warning("Please enter a thesis topic.")
        else:
            with st.spinner("Generating thesis statements..."):
                full_topic = thesis_topic
                if main_idea:
                    full_topic += f" - {main_idea}"
                if reason:
                    full_topic += f" - because {reason}"
                if audience:
                    full_topic += f" - for {audience}"

                result = graph_executor.invoke({"topic": full_topic})
                result_text = result["thesis_list"]

                result_placeholder.markdown(result_text)
                st.session_state.result_text = result_text

# Related Articles Section
st.markdown("---")
st.subheader("🔍 Related Articles and Papers")

if thesis_topic.strip():
    with st.spinner("Searching for articles..."):
        try:
            articles = fetch_related_articles(thesis_topic)
            if articles:
                st.success("Here are related articles and papers:")
                for i, article in enumerate(articles, start=1):
                    st.markdown(f"{i}. {article}")
            else:
                st.warning("No recent articles found. Try refining your topic.")
        except Exception as e:
            st.error(f"Error fetching articles: {str(e)}")
else:
    st.info("Enter a topic to fetch related articles.")
