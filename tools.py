import logging
from livekit.agents import function_tool, RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun

@function_tool()
async def web_search(context: RunContext, query: str) -> str:
    """
    Perform a web search using DuckDuckGo and return the first result.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error during web search: {e}")
        return "An error occurred while searching the web for {query}."