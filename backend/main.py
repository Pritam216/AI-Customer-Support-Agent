# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel
# import json

# from langchain_core.messages import HumanMessage
# from workflow.graph import graph

# import uuid

# app = FastAPI()

# # Add CORS middleware to accept requests from your React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # For production, replace with your exact frontend URL (e.g., ["http://localhost:3000"])
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# unique_id = uuid.uuid4()
# last_four = str(unique_id)[-4:]

# class ChatRequest(BaseModel):
#     message: str
#     thread_id: str = f"user-{last_four}"

# @app.post("/chat/stream")
# def chat_stream(req: ChatRequest):
#     def event_generator():
#         yield f"data: {json.dumps({'type': 'info', 'message': 'Request received'})}\n\n"

#         for event in graph.stream(
#             {
#                 "messages": [HumanMessage(content=req.message)]
#             },
#             config={
#                 "configurable": {
#                     "thread_id": req.thread_id
#                 }
#             }
#         ):
#             yield f"data: {json.dumps({'type': 'event', 'data': str(event)})}\n\n"

#         final_msg = event["chatbot"]["messages"][-1] if "chatbot" in event else None

#         if final_msg:
#             yield f"data: {json.dumps({'type': 'final', 'message': final_msg.content})}\n\n"

#     return StreamingResponse(event_generator(), media_type="text/event-stream")










# import os
# import sys
# import json
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel
# from dotenv import load_dotenv

# from livekit import api
# from langchain_core.messages import HumanMessage
# from workflow.graph import graph

# load_dotenv()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ChatRequest(BaseModel):
#     message: str
#     thread_id: str = "user-1"

# @app.post("/chat/stream")
# def chat_stream(req: ChatRequest):
#     def event_generator():
#         yield f"data: {json.dumps({'type': 'info', 'message': 'Request received'})}\n\n"

#         for event in graph.stream(
#             {"messages": [HumanMessage(content=req.message)]},
#             config={"configurable": {"thread_id": req.thread_id}}
#         ):
#             if "chatbot" in event:
#                 node_output = event["chatbot"]
#                 if "messages" in node_output and node_output["messages"]:
#                     last_msg = node_output["messages"][-1]
                    
#                     if hasattr(last_msg, "content") and last_msg.content:
#                         if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
#                             continue
                            
#                         yield f"data: {json.dumps({'type': 'event', 'text': last_msg.content})}\n\n"

#         try:
#             final_messages = event["chatbot"]["messages"]
#             final_content = final_messages[-1].content if final_messages else ""
#             if final_content and not getattr(final_messages[-1], "tool_calls", None):
#                 yield f"data: {json.dumps({'type': 'final', 'message': final_content})}\n\n"
#         except (KeyError, IndexError):
#             pass

#     return StreamingResponse(event_generator(), media_type="text-event-stream")

# @app.get("/api/voice-token")
# def get_voice_token(room: str = "refund-room", user: str = "web-client"):
#     lk_key = os.getenv("LIVEKIT_API_KEY", "devkey")
#     lk_secret = os.getenv("LIVEKIT_API_SECRET", "secret")
    
#     token = api.AccessToken(lk_key, lk_secret).with_identity(user).with_name(user).with_grants(api.VideoGrants(
#             room_join=True,
#             room=room,
#             can_publish=True,
#             can_subscribe=True
#         ))
#     return {"token": token.to_jwt()}












# import os
# import sys
# import json
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel
# from dotenv import load_dotenv

# from livekit import api
# from langchain_core.messages import HumanMessage
# from workflow.graph import graph

# load_dotenv()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class ChatRequest(BaseModel):
#     message: str
#     thread_id: str = "user-1"

# @app.post("/chat/stream")
# def chat_stream(req: ChatRequest):
#     def event_generator():
#         yield f"data: {json.dumps({'type': 'info', 'message': 'Request received'})}\n\n"
        
#         last_node_output = None

#         # 1. Capture updates safely over the active graph generation stream
#         for event in graph.stream(
#             {"messages": [HumanMessage(content=req.message)]},
#             config={"configurable": {"thread_id": req.thread_id}}
#         ):
#             if "chatbot" in event:
#                 last_node_output = event["chatbot"]
#                 if "messages" in last_node_output and last_node_output["messages"]:
#                     last_msg = last_node_output["messages"][-1]
                    
#                     if hasattr(last_msg, "content") and last_msg.content:
#                         # Skip emitting text to UI if this generation block contains a tool call request
#                         if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
#                             continue
                        
#                         # Filter text if it explicitly leaks tool structure
#                         text_content = last_msg.content
#                         if "crm_lookup" in text_content or "rag_tool" in text_content or "Document(" in text_content:
#                             continue
                            
#                         yield f"data: {json.dumps({'type': 'event', 'text': text_content})}\n\n"

#         # 2. Extract the final user response inside valid block scope
#         if last_node_output and "messages" in last_node_output and last_node_output["messages"]:
#             final_msg = last_node_output["messages"][-1]
#             if final_msg.content and not getattr(final_msg, "tool_calls", None):
#                 # Extra safety check to prevent JSON objects from slipping to final chat message text bubbles
#                 if not ("crm_lookup" in final_msg.content or "rag_tool" in final_msg.content):
#                     yield f"data: {json.dumps({'type': 'final', 'message': final_msg.content})}\n\n"

#     # CRITICAL FIX: Changed 'text-event-stream' to standard 'text/event-stream'
#     return StreamingResponse(event_generator(), media_type="text/event-stream")

# @app.get("/api/voice-token")
# def get_voice_token(room: str = "refund-room", user: str = "web-client"):
#     lk_key = os.getenv("LIVEKIT_API_KEY", "devkey")
#     lk_secret = os.getenv("LIVEKIT_API_SECRET", "secret")
    
#     token = api.AccessToken(lk_key, lk_secret).with_identity(user).with_name(user).with_grants(api.VideoGrants(
#         room_join=True,
#         room=room,
#         can_publish=True,
#         can_subscribe=True
#     ))
#     return {"token": token.to_jwt()}





import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from livekit import api
from langchain_core.messages import HumanMessage
from workflow.graph import graph

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "user-1"


# @app.post("/chat/stream")
# def chat_stream(req: ChatRequest):
#     # def event_generator():
#     #     state = graph.invoke(
#     #         {"messages": [HumanMessage(content=req.message)]},
#     #         config={"configurable": {"thread_id": req.thread_id}}
#     #     )
        
#     #     last_message = state["messages"][-1]
#     #     final_text = getattr(last_message, "content", "")

#     #     if "Decision:" in final_text:
#     #         final_text = "Decision:" + final_text.split("Decision:")[-1]
        
#     #     yield f"data: {json.dumps({'type': 'final', 'message': final_text.strip()})}\n\n"

#     # return StreamingResponse(event_generator(), media_type="text/event-stream")

#     def event_generator():
#         try:
#             state = graph.invoke(
#                 {"messages": [HumanMessage(content=req.message)]},
#                 config={"configurable": {"thread_id": req.thread_id}}
#             )

#             final_text = getattr(state["messages"][-1], "content", "")
#             tool_names = state.get("tool_names", [])

#             if "Decision:" in final_text:
#                 final_text = "Decision:" + final_text.split("Decision:")[-1]

#             # yield f"data: {json.dumps({'type': 'final', 'message': final_text.strip()})}\n\n"
#             payload = {
#                 "type": "final",
#                 "message": final_text.strip(),
#                 "tools": tool_names
#             }

#             yield f"data: {json.dumps(payload)}\n\n"

#         except Exception as e:
#             yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"



@app.post("/chat/stream")
def chat_stream(req: ChatRequest):

    def event_generator():
        try:
            state = graph.invoke(
                {"messages": [HumanMessage(content=req.message)]},
                config={
                    "configurable": {
                        "thread_id": req.thread_id
                    }
                }
            )

            final_text = ""

            if state.get("messages"):
                final_text = state["messages"][-1].content or ""

            tool_names = state.get("tool_names", [])

            payload = {
                "type": "final",
                "message": final_text.strip(),
                "tools": tool_names
            }

            yield f"data: {json.dumps(payload)}\n\n"

        except Exception as e:
            payload = {
                "type": "error",
                "message": str(e)
            }

            yield f"data: {json.dumps(payload)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/api/voice-token")
def get_voice_token(room: str = "refund-room", user: str = "web-client"):
    # token = (
    #     api.AccessToken(os.getenv("LIVEKIT_API_KEY"), os.getenv("LIVEKIT_API_SECRET"))
    #     .with_identity(user)
    #     .with_name(user)
    #     .with_grants(api.VideoGrants(room_join=True, room=room, can_publish=True, can_subscribe=True))
    # )
    token = (
        api.AccessToken(
            os.getenv("LIVEKIT_API_KEY"),
            os.getenv("LIVEKIT_API_SECRET")
        )
        .with_identity(user)
        .with_name(user)
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=room,
            )
        )
        .with_room_config(
            api.RoomConfiguration(
                agents=[
                    api.RoomAgentDispatch(
                        agent_name="refund-voice-agent"
                    )
                ]
            )
        )
    )
    return {"token": token.to_jwt()}