import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv, find_dotenv
import asyncio

load_dotenv(find_dotenv())

api_key = os.getenv("GEMINI_API_KEY")

set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


async def chat():
    model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=client
    )


    agent: Agent = Agent(
        name="Best Friend",
        instructions="You are best social expert",
        model= model
    )

    topic= "self improvement, communication, empathy"

    result = await Runner.run(
        agent, 
        f"Give me one short advice {topic}, possibly one line"
    )

    print(result.final_output)

asyncio.run(chat())