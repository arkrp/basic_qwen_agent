#section-start import stuff
from openai import OpenAI
from os import environ as ENVIRONMENT
from qwen_interface import SystemMessage, UserMessage, AssistantMessage, ToolMessage, ToolDescription, ToolParameter, EnumToolParameter, continue_conversation, ForceToolOption, StandardOption, NoThinkOption, ForceMessageStartOption
#section-end
#section-start define constants
OPENAI_API_BASE = ENVIRONMENT["OPENAI_API_BASE"]
OPENAI_API_KEY = ENVIRONMENT["OPENAI_API_KEY"]
PREFFERED_MODEL = "model.gguf"
#section-end
#section-start get the completions up and running
#section-start make the connection
engine = OpenAI(
    base_url=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY
)
#section-end
#section-start wrap the connection
def raw_completion_function(prompt_string): #section-start
    return(engine.completions.create(
        model=PREFFERED_MODEL,
        prompt=prompt_string,
        max_tokens=4096,
        temperature=0.7
        ).choices[0].text)
#section-end
#section-end
#section-end
messages=[ #section-start
    SystemMessage("You are Gryph Four, A helpful AI agent."),
    #UserMessage("Hello. Could you tell me what you are doing?"),
    UserMessage("Hey G4! How are you today?"),
]
#section-end
tool_descriptions = [ #section-start
    ToolDescription(
        "get_weather",
        "Get current weather information for a location",
        ToolParameter("location", "The city and state, e.g. San Francisco, CA"),
        EnumToolParameter("unit","The unit of temperature to use",["celsius", "fahrenheit"])
    ),
    ToolDescription(
        "get_weather_preference",
        "get the user\'s weather preference",
    ),
]
#section-end
response = continue_conversation(
    messages=messages,
    tool_descriptions=tool_descriptions,
    option=ForceMessageStartOption("You've got a lot of guts coming back here"),
    raw_completion_function=raw_completion_function)
print(response)
