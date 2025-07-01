# tools.py
from langchain.utilities import GoogleSearchAPIWrapper
import os
from dotenv import load_dotenv
load_dotenv()
# Configuration for Google Search API
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def fetch_related_articles(topic):
    search = GoogleSearchAPIWrapper(
        google_api_key=GOOGLE_SEARCH_API_KEY,
        google_cse_id=GOOGLE_CSE_ID
    )
    query = f"{topic} research paper"
    results = search.results(query, num_results=10)
    return [f"[{item['title']}]({item['link']})" for item in results]