from langchain.tools import tool
from workflow.state import ExtractID
import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere

load_dotenv()

llm = ChatCohere(
    model = "command-a-03-2025",
    cohere_api_key=os.getenv("COHERE_API_KEY"),
)

structure_llm = llm.with_structured_output(ExtractID)
@tool
def extract_id(query: str):
    """
    Use this tool to extract order id from the user query
    """
    print("\n Extract id tool called !!!")
    res = structure_llm.invoke(query)
    return res.order_id