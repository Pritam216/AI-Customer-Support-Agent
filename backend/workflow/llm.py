import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_groq import ChatGroq
from workflow.tools.crm_tool import crm_lookup
from workflow.tools.policy_tool import rag_tool
from workflow.tools.orderId_tool import extract_id
from langgraph.prebuilt import ToolNode

load_dotenv()

# llm = ChatCohere(
#     model = "command-a-03-2025",
#     cohere_api_key=os.getenv("COHERE_API_KEY"),
# )

llm=ChatGroq(
    model="openai/gpt-oss-120b",
    api_key = os.getenv("GROQ_API_KEY")
)

voice_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

tools = [crm_lookup, rag_tool, extract_id]
llm_with_tool = llm.bind_tools(tools)
tool_node = ToolNode(tools)