from workflow.state import GraphState
from langgraph.graph import END
from workflow.prompt import prompt
from workflow.llm import llm_with_tool, llm, voice_llm
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import re


def should_continue(state):
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END


def modify_node(state):
    messages = state["messages"]
    if not messages:
        return {"messages": messages}
    last_message = messages[-1]

    response = llm.invoke([
        SystemMessage(content="""
You are a text normalization assistant.
Fix spoken order IDs into ORDXXXX format only if order id is mention.
Return ONLY the corrected query.
        """),
        HumanMessage(content=last_message.content)
    ])
    last_message.content = response.content.strip()

    return {"messages": messages}


def chat_node(state):

    response = llm_with_tool.invoke([
        SystemMessage(content=f"""
{prompt}
"""),
        *state["messages"]
    ])

    tool_names = [
        tool["name"]
        for tool in getattr(response, "tool_calls", [])
    ]

    return {
        "messages": [response],
        "tool_names": tool_names
    }


def final_response_node(state):
        prompt = f"""
Convert the following refund-agent output into a natural spoken response.

Rules:
- Maximum 2 sentences.
- Do not mention policies.
- Do not mention tool outputs.
- Do not mention CRM records.
- Do not mention JSON.
- Sound like a customer support representative.
- Tell 1st approve or denied.
- If approved, explain briefly.
- If denied, explain briefly.

Output only the final spoken response.

Input:
{state["messages"][-1].content}
"""

        response = voice_llm.invoke(prompt)

        return {
            "messages": [response.content.strip()]
        }