import os, requests, pprint
from dotenv import load_dotenv, find_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

set_tracing_disabled(disabled=True)
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
base_url = os.getenv('GEMINI_BASE_URL')

client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)


model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

@function_tool 
def find_coordinates(city: str) -> object: 

    print(f'Getting find_coordinates for city: {city}')

    pakistan_cities = [
        {
            "city": "Karachi",
            "latitude": 24.8600,
            "longitude": 67.0100
        },
        {
            "city": "Lahore",
            "latitude": 31.5497,
            "longitude": 74.3436
        },
        {
            "city": "Faisalabad",
            "latitude": 31.4167,
            "longitude": 73.0911
        },
        {
            "city": "Rawalpindi",
            "latitude": 33.6000,
            "longitude": 73.0333
        },
        {
            "city": "Gujranwala",
            "latitude": 32.1567,
            "longitude": 74.1900
        },
        {
            "city": "Peshawar",
            "latitude": 34.0144,
            "longitude": 71.5675
        },
        {
            "city": "Multan",
            "latitude": 30.1978,
            "longitude": 71.4697
        },
        {
            "city": "Hyderabad",
            "latitude": 25.3792,
            "longitude": 68.3683
        },
        {
            "city": "Islamabad",
            "latitude": 33.6931,
            "longitude": 73.0639
        },
        {
            "city": "Hangu",
            "latitude": 33.525,
            "longitude": 71.054
        }
    ]

    for c in pakistan_cities:
        if c["city"].lower() == city.lower():
            print(f'Got Latitude {c["latitude"]} Longitude {c["longitude"]}')
            return {
                "city": c["city"],
                "latitude" : c["latitude"],
                "longitude" : c["longitude"]
            }
    return None
    
@function_tool
def weather(latitude: float, longitude: float) -> object:
    print(f'Calling weather api for latitude {latitude} longitude {longitude} \n\n')
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    weather = resp.json()
    return weather

agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model=model,
    tools=[find_coordinates, weather]
)

result = Runner.run_sync(
    agent,
    "Weather in city Lahore"
)

print(result.final_output)