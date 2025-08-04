from langchain_community.tools.gmail.get_thread import GmailGetThread
from crewai_tools import BaseTool

class GmailThreadTool(BaseTool):
    name: str = "get_gmail_thread"
    description: str = "Retrieves the full Gmail thread by thread ID."

    def _run(self, thread_id: str) -> str:
        print(f"[DEBUG] get_gmail_thread received thread_id: {thread_id}")
        return GmailGetThread().run(thread_id)
