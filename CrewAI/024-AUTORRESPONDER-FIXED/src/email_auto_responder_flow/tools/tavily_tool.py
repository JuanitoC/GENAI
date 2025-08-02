from langchain_community.tools.tavily_search import TavilySearchResults
from crewai_tools import BaseTool

class TavilySearchTool(BaseTool):
    name: str = "tavily_search"
    description: str = "Search the web using Tavily and return a summary."

    def _run(self, query: str) -> str:
        return TavilySearchResults().run(query)
