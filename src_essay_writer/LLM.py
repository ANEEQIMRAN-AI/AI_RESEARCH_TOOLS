# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# LLM.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY, temperature=0.7)

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