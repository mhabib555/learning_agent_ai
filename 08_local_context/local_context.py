import os, asyncio, random
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
    top_early_childhood_math_books = [
        {
            "title": "Moebius Noodles",
            "author": "Yelena McManaman and Maria Droujkova",
            "description": "Engaging activities for young children to explore math concepts like symmetry and patterns through play."
        },
        {
            "title": "Bedtime Math: A Fun Excuse to Stay Up Late",
            "author": "Laura Overdeck",
            "description": "Fun, bedtime-themed math problems to spark curiosity and build number sense in preschoolers."
        },
        {
            "title": "Counting Kisses",
            "author": "Karen Katz",
            "description": "A board book introducing counting through interactive, affectionate storytelling for toddlers."
        },
        {
            "title": "The Doorbell Rang",
            "author": "Pat Hutchins",
            "description": "A picture book that introduces division and sharing through a story of dividing cookies among friends."
        }
    ]
    return random.choice(top_early_childhood_math_books)

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


