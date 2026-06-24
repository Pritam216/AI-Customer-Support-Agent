from langgraph.graph import StateGraph
from langgraph.graph import START, END

from workflow.nodes import chat_node, should_continue, modify_node,final_response_node
from workflow.state import GraphState
from workflow.llm import tool_node
from langchain_core.messages import HumanMessage

# from langgraph.checkpoint.sqlite import SqliteSaver
# from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.memory import MemorySaver
import sqlite3

conn = sqlite3.connect("checkpoints.db", check_same_thread=False)

builder = StateGraph(GraphState)

builder.add_node("modify", modify_node)
builder.add_node("chatbot",chat_node)
builder.add_node("tools",tool_node)
builder.add_node("final_response_node",final_response_node)

builder.add_edge(START,"modify")
builder.add_edge("modify","chatbot")
builder.add_conditional_edges("chatbot",should_continue)
builder.add_edge("tools","chatbot")
builder.add_edge("chatbot", "final_response_node")
builder.add_edge("final_response_node", END)

# checkpointer = SqliteSaver(conn)
# graph = builder.compile(checkpointer=checkpointer)

# memory = AsyncSqliteSaver.from_conn_string(":memory:") 
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
