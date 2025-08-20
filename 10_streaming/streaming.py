import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, ItemHelpers, function_tool, set_tracing_disabled
import random

set_tracing_disabled(disabled=True)
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("GEMINI_BASE_URL")

gemini_client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
) 

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model= "gemini-2.5-flash",
    openai_client=gemini_client
)

@function_tool
def number_of_jokes() -> int:
    return random.randint(1,10)

agent: Agent = Agent(
    name="Assistant",
    instructions="First call `number_of_jokes` took then tell that many jokes",
    model=model,
    tools=[number_of_jokes]
)

async def call_agent():

    result = Runner.run_streamed(
        starting_agent=agent,
        input="Hi",
    )

    print("=== Run starting ===")
    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types




asyncio.run(call_agent())


