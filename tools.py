from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

search = DuckDuckGoSearchRun()
searchtool = Tool(
    name="DuckDuckGo_Search",
    func=search.run,
    description="Useful for searching the web for information on a topic."
)

