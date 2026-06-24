# class RefundVoiceAgent(Agent):
#     def __init__(self, job_id: str) -> None:
#         super().__init__(
#             instructions=(
#     "You are a strict backend assistant. When a user provides an order ID, "
#     "immediately and exclusively trigger your tool calls. Do not write text "
#     "explanations like 'I am going to lookup your data' or mix JSON strings into chat."
# ),
#             stt=deepgram.STT(model="nova-2-general"),
#             llm=langchain.LLMAdapter(
#                 graph=graph,
#                 config={"configurable": {"thread_id": f"voice_session_{job_id}"}}
#             ),
#             tts=deepgram.TTS(model="aura-asteria-en")
#             # Fixed: Removed the bad keyword argument from here
#         )

# async def entrypoint(ctx: JobContext):
#     logger.info(f"Connecting to room: {ctx.room.name}")
#     await ctx.connect()

#     session = AgentSession()

#     @session.on("user_speech_committed")
#     def on_user_speech(chat_context):
#         if chat_context.messages:
#             last_msg = chat_context.messages[-1]
#             final_text = last_msg.content
                
#             # Clean filter: extract only the final decision block
#             if "Decision:" in final_text:
#                 final_text = "Decision:" + final_text.split("Decision:")[-1]
            
#             print(f"\n[EXTRACTED STATE CONTENT SENT TO TTS]: {final_text.strip()}\n")
            
#             # Speak the filtered text manually
#             ctx.create_task(session.say(final_text.strip(), allow_interruptions=True))

#     # Alternative Fix: Pass it here if you are using standard VoicePipelineAgent, 
#     # but since you are manually calling session.say, the event callback above handles it.
#     await session.start(
#         room=ctx.room,
#         agent=RefundVoiceAgent(job_id=ctx.job.id)
#     )

# if __name__ == "__main__":
#     cli.run_app(
#         WorkerOptions(
#             entrypoint_fnc=entrypoint,
#             agent_name="refund-voice-agent"
#         )
#     )











from __future__ import annotations
import logging
import re
import sys
import asyncio
from dotenv import load_dotenv
# from workflow.nodes import normalize_for_voice
from livekit.agents import JobContext, WorkerOptions, cli, JobProcess
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import deepgram, langchain

# from livekit.rtc import ConnectionState
from workflow.graph import graph

load_dotenv()
logger = logging.getLogger("voice-agent")

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class RefundVoiceAgent(Agent):
    def __init__(self, job_id: str) -> None:
        super().__init__(
            instructions=(
                "You are a strict backend assistant. When a user provides an order ID, "
                "immediately and exclusively trigger your tool calls. Do not write text "
                "explanations like 'I am going to lookup your data' or mix JSON strings into chat."
            ),
            stt=deepgram.STT(model="nova-2-general"),
            llm=langchain.LLMAdapter(
                graph=graph,
                config={"configurable": {"thread_id": f"voice_session_{job_id}"}}
            ),
            tts=deepgram.TTS(model="aura-asteria-en")
        )

    async def on_enter(self) -> None:
        """Executes immediately when the agent joins the WebRTC room."""
        logger.info(f"Agent successfully entered room session.")
        # Trigger an initial audio track down the stream
        await self.session.say(
            "Hello! I am your refund assistant. Please provide your order ID to begin.", 
            allow_interruptions=True
        )

    # async def on_llm_response(self, response_stream) -> None:
    #     full_text = ""
    #     async for chunk in response_stream:
    #         if hasattr(chunk, 'text') and chunk.text:
    #             full_text += chunk.text

    #     print("\n" + "="*40 + " RAW LLM OUTPUT RECEIVED " + "="*40)
    #     print(full_text)
    #     print("="*105 + "\n")

    #     match = re.search(r"(Decision:\s*(?:DENIED|APPROVED)[\s\S]*)", full_text)
        
    #     if match:
    #         clean_decision = match.group(1).strip()
    #         await self.session.say(clean_decision, allow_interruptions=True)
    #     else:
    #         if "Decision:" in full_text:
    #             parts = full_text.split("Decision:")
    #             await self.session.say(f"Decision: {parts[-1]}", allow_interruptions=True)

    def on_speak(self, text: str) -> None:
        print(f"\n[AGENT TTS AUDIO PLAYBACK TRACE]: {text}\n")


# async def entrypoint(ctx: JobContext):
#     logger.info(f"Received request to join room: {ctx.room.name}")
    
#     # 1. Connect the background process to the active LiveKit video/audio channel
#     await ctx.connect()
#     logger.info("Successfully connected to the room track network.")

#     # 2. Start the interactive session loop
#     session = AgentSession()
#     await session.start(
#         room=ctx.room,
#         agent=RefundVoiceAgent(job_id=ctx.job.id)
#     )

#     await asyncio.Future()



async def entrypoint(ctx: JobContext):

    logger.info(f"Received request to join room: {ctx.room.name}")

    await ctx.connect()

    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=RefundVoiceAgent(job_id=ctx.job.id)
    )

    await asyncio.Future()


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="refund-voice-agent"
        )
    )