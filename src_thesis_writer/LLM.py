
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# LLM.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
    max_tokens=2048
)

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

thesis_agent = thesis_prompt | llm
humanize_agent = humanize_prompt | llm
grammar_agent = grammar_prompt | llm