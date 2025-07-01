# AI Essay Writer Agent using LangChain + LangGraph + Streamlit + PDF Export

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict
from fpdf import FPDF
import streamlit as st
import re

# Define state schema
class EssayState(TypedDict):
    topic: str
    essay: str
    humanized_essay: str
    final_output: str

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=gemini_api_key, temperature=0.7)

### PROMPTS ###

essay_prompt = PromptTemplate.from_template(
    """
    You are a doctoral-level academic essay writer.

    Write a PhD-level academic essay on the following topic:
    "{topic}"

    Your essay must follow this structured format and MUST include appropriate main headings and subheadings for each section:

    [1] Introduction:
    - Begin with a compelling hook (question, quote, or statistic).
    - Use at least 2 subheadings under Introduction to elaborate background and context.
    - Clearly articulate the thesis statement and define the scope of the essay.
    - End with a roadmap outlining the key themes of the discussion.

    [2] Core Analysis:
    - Replace the phrase "Body Paragraphs" with "Core Analysis."
    - Each thematic argument must begin with a clear, bolded heading.
    - Support claims with scholarly evidence, data, or peer-reviewed literature.
    - Include deep critical analysis and synthesis.
    - Address counterarguments and show multiple perspectives.

    [3] Conclusion:
    - Summarize core insights and restate the thesis with greater clarity.
    - Synthesize findings into a broader academic or societal context.
    - Offer potential research directions or implications.
    - End with a strong, thought-provoking closing remark.

    Additional Requirements:
    - Maintain a formal, academic tone throughout.
    - Demonstrate critical thinking and originality.
    - Use APA in-text citation format.
    - Word count: approximately 1000–1200 words.
    - Section headings and subheadings are mandatory.

    Begin now.
    """
)

humanizer_prompt = PromptTemplate.from_template(
    """
    You are a world-class editor and human-like writing specialist. Carefully revise the essay below to:
    - Sound exceptionally natural and human-like, as if written by an intelligent, thoughtful individual.
    - Enhance readability by introducing subtle narrative elements or rhetorical devices (e.g., metaphors, anecdotes, personal tone).
    - Improve flow, remove stiffness, and avoid robotic or mechanical phrasing.
    - Preserve the academic integrity and depth while making it engaging and emotionally resonant.
    - Ensure that all section headings and subheadings are preserved and properly structured.

    Essay:
    {essay}

    Humanized Essay:
    """
)

grammar_prompt = PromptTemplate.from_template(
    """
    You are a highly skilled academic proofreader and language refinement expert.

    Review the essay below meticulously to:
    - Correct all grammar, punctuation, and spelling mistakes.
    - Ensure clarity, coherence, and professional academic tone.
    - Restructure awkward or unclear sentences without changing the meaning.
    - Enhance lexical choice for precision, formality, and fluency.
    - Guarantee that the essay reads like it has been reviewed by a human editor with PhD-level writing skills.
    - Preserve all structural headings and subheadings.

    Essay:
    {humanized_essay}

    Corrected Essay:
    """
)

# AGENT FUNCTIONS

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

# FORMAT CLEANUP

def format_for_pdf(text):
    lines = text.split("\n")
    formatted_lines = []
    for line in lines:
        clean_line = line.strip()
        if clean_line:
            # Bold numbered headings like 1.1, 2.2 etc.
            if re.match(r"^\d+\.\d+", clean_line):
                formatted_lines.append(("B", clean_line))
            # Bold main headings like ## Heading
            elif clean_line.startswith("##"):
                formatted_lines.append(("B", clean_line.replace("##", "").strip()))
            # Bold **text** style
            elif clean_line.startswith("**") and clean_line.endswith("**"):
                formatted_lines.append(("B", clean_line.replace("**", "").strip()))
            # Handle References heading without asterisks
            elif clean_line.lower().startswith("references"):
                formatted_lines.append(("B", clean_line.replace("*", "").strip()))
            else:
                formatted_lines.append(("", clean_line))
    return formatted_lines


def export_to_pdf(topic: str, content: str, filename: str = None):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Times", "", fname="C:\\Windows\\Fonts\\times.ttf", uni=True)
    pdf.set_font("Times", size=12)

    formatted = format_for_pdf(content)
    for style, line in formatted:
        if style == "B":
            pdf.set_font("Times", "B", 12)
            pdf.multi_cell(0, 7.5, line)
            pdf.set_font("Times", "", 12)
        else:
            pdf.multi_cell(0, 6, line)

        if filename is None:
            filename = topic.strip().replace(" ", "_").replace("/", "-") + ".pdf"
    pdf.output(filename)
    return filename

# LANGGRAPH FLOW

graph = StateGraph(EssayState)
graph.add_node("GenerateEssay", RunnableLambda(generate_essay))
graph.add_node("HumanizeEssay", RunnableLambda(humanize_essay))
graph.add_node("GrammarCorrect", RunnableLambda(correct_grammar))
graph.set_entry_point("GenerateEssay")
graph.add_edge("GenerateEssay", "HumanizeEssay")
graph.add_edge("HumanizeEssay", "GrammarCorrect")
graph.add_edge("GrammarCorrect", END)
workflow = graph.compile()

# STREAMLIT UI

st.set_page_config(page_title="AI Essay Writer", layout="centered")
st.title("📝 AI Essay Writer ")
st.markdown("""WELCOME TO THE AI ESSAY WRITER! This tool generates high-quality, PhD-level essays on any topic you provide. It uses advanced AI to create structured, well-researched content with proper academic formatting. You can also download the essay as a PDF file.""")

user_topic = st.text_input("Enter your Essay Topic")
submit = st.button("Generate Essay")

if submit and user_topic:
    with st.spinner("Generating essay. Please wait..."):
        output = workflow.invoke({"topic": user_topic})
        final_essay = output["final_output"].content

        st.subheader("📄 Final Essay")
        st.text_area("PhD-Level Essay", final_essay, height=500)

        filename = export_to_pdf(user_topic, final_essay)
        with open(filename, "rb") as f:
            st.download_button("📥 Download Essay as PDF", f, file_name=filename, mime="application/pdf")
