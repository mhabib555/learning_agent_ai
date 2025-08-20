import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunContextWrapper, function_tool, set_tracing_disabled
from dataclasses import dataclass

set_tracing_disabled(disabled=True)
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("GEMINI_BASE_URL")

@dataclass
class UserContext: 
    username: str
    email: str | None = None


gemini_client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
) 

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model= "gemini-2.5-flash",
    openai_client=gemini_client
)



@function_tool
def search(local_context: RunContextWrapper[UserContext], query: str) -> str:
    print(f"\nSearching ..... {query}")
    print("\ncontext", local_context.context, "\n\n")
    return "No result"

async def special_prompt(special_context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str: 
    return f"You are a math expert. User: {special_context.context.username}, Agent: {agent.name}. Please assist with math-related queries."


agent: Agent = Agent(
    name="Assistant",
    instructions=special_prompt,
    model=model,
    tools=[search]
)

async def call_agent():

    user_context = UserContext(username="Habib")

    response = await Runner.run(
        starting_agent=agent,
        input="Search for the early childhood math education books",
        context=user_context
    )

    print(response.final_output)


asyncio.run(call_agent())


