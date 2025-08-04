import os, asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner , AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("GEMINI_BASE_URL")

client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)


async def run_level():
   
   model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
   model="gemini-2.5-flash",
   openai_client=client
   )

   config: RunConfig = RunConfig(
      model= model,
      model_provider=client,
      tracing_disabled=True
   )

   agent: Agent = Agent(
      name= "Assistant",
      instructions = "You are a helpful assistant",
   )

   response = await Runner.run(
      agent,
      "One life advice",
      run_config=config
   )

   print(response.final_output)


if __name__ == "__main__":
  asyncio.run(run_level())
