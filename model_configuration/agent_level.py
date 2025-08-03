import os, asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner , AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled

set_tracing_disabled(disabled=True)
load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("GEMINI_BASE_URL")

client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

async def agent_level():

    agent: Agent = Agent(
       name="Best Friend",
       instructions="You are Best Social Expert",
       model=OpenAIChatCompletionsModel(
        model= "gemini-2.5-flash",
        openai_client=client
      )

    )

    response = await Runner.run(
       agent,
       "One line advice"
    )

    print(response.final_output)



if __name__ == "__main__":
  asyncio.run(agent_level())