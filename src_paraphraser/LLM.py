# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# LLM.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
    max_tokens=3000
)

# Rephrase Prompt
rephrase_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional rephrasing assistant. Rephrase the following paragraph without losing the original meaning. Avoid plagiarism and redundancy."),
    ("human", "{input_paragraph}")
])

# Humanize Prompt
humanize_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a humanization expert. Make the following text sound extremely natural, fluent, and written by a native speaker. Make it engaging and polished."),
    ("human", "{rephrased_paragraph}")
])

# Grammar Prompt
grammar_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a grammar correction expert. Correct all grammatical, punctuation, and structural errors in the following text without altering its meaning or tone."),
    ("human", "{humanized_paragraph}")
])

# Create chains
rephrase_chain = rephrase_prompt | llm
humanized_chain = humanize_prompt | llm
grammar_chain = grammar_prompt | llm