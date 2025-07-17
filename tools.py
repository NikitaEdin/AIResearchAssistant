from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain.tools import Tool
from datetime import datetime

# Function to save research output to text file
def save_to_text(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"---Research Output---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Data successfully saved to {filename}"

# Define tool for saving research output
save_tool = Tool(
    name="save_text_to_file",
    func=save_to_text,
    description="Saves structured research data to a text file."
)

# Define search tool using DuckDuckGo
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="DuckDuckGoSearch",
    func=search.run,
    description="Useful for searching the web for information on a topic."
)

# Define Wikipedia
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

arxiv_tool = Tool(
    name="arxiv_search",
    description="Use this tool to search for scientific papers on arXiv.org.",
    func=ArxivQueryRun(api_wrapper=ArxivAPIWrapper()).run,
)