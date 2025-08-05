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
        name="Assistant",
        instructions="You are a helpful assistant",
        model= model
    )


    result = await Runner.run(
        agent, 
        "Give me one short advice"
    )

    print(result.final_output)

asyncio.run(chat())
