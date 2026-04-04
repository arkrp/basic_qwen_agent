#section-start setup
#section-start print hello world
print("hello world")
#section-end
#section-start import stuff
from openai import OpenAI
from os import environ as ENVIRONMENT
from qwen_interface import SystemMessage, UserMessage, AssistantMessage, ToolMessage, ToolDescription, ToolParameter, EnumToolParameter, parse_response, compile_prompt
#section-end
#section-start set configuration constants
OPENAI_API_BASE = ENVIRONMENT["OPENAI_API_BASE"]
OPENAI_API_KEY = ENVIRONMENT["OPENAI_API_KEY"]
PREFFERED_MODEL = "model.gguf"
#section-end
#section-start print preload complete
print("preload complete")
#section-end
#section-end
#section-start connect to completion engine
engine = OpenAI(
    base_url=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY
)
#section-end
messages = [ #section-start
    SystemMessage("You are Gryph Four, A helpful AI agent.")]
#section-end
#section-start define tools
def get_weather(*, location, unit="celsius"): #section-start
    if unit=="celsius":
        return("It is 30 degrees celsius in " + location)
    else:
        return("It is 70 degrees fahrenheit in " + location)
#section-end
def get_weather_preference(): #section-start
    return("The user prefers temperatures above 35 degrees celsius")
#section-end
tools = { #section-start
    "get_weather":get_weather,
    "get_weather_preference":get_weather_preference
}
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
#section-end
#section-start have a conversation!
#section-start give the user the first statement
speaker="user"
#section-end
#section-start take turns for the rest!
while(True):
    #section-start let the speaker speak
    #section-start deal with speaker being the user
    if speaker=="user":
        user_input = input("User: ")
        if((user_input == "exit") or (user_input == "q") or (user_input == "quit")):
            break
        messages.append(UserMessage(user_input))
        speaker="assistant"
    #section-end
    #section-start deal with the speaker being the assitant
    elif speaker=="assistant":
        #section-start compile prompt
        prompt_string = compile_prompt(messages=messages, tool_descriptions=tool_descriptions)
        #section-end
        #section-start generate response
        response=engine.completions.create(
            model=PREFFERED_MODEL,
            prompt=prompt_string,
            max_tokens=4096,
            temperature=0.7
            ).choices[0].text
        #section-end
        #section-start parse the response!
        messages.append(parse_response(response))
        #section-end
        if messages[-1]["content"] != "":
            print("Assistant: " + messages[-1]["content"])
        else:
            print("Assitant(tool call):" + messages[-1]["content"])
        #section-start pass the turn to tool or user!
        if "tool_calls" in messages[-1]:
            speaker="tool"
        else:
            speaker="user"
        #section-end
    #section-end
    #section-start deal with the speaker being a tool
    elif speaker=="tool":
        for tool_call in messages[-1]["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            #print("tool_name: "+tool_name)
            tool_args = tool_call["function"]["arguments"]
            #print("function_args: "+repr(tool_args))
            #print("tool_call_result: "+tools[tool_name](**tool_args))
            tool_response = ToolMessage(tools[tool_name](**tool_args))
            messages.append(tool_response)
            print("Tool("+ tool_name +"): "+ tool_response["content"])
        speaker = "assistant"
    #section-end
    #section-start deal with invalid speaker value!
    else:
        raise ValueError("Unrecognize speaker value: " +speaker)
    #section-end
    #section-end
#section-end
#section-end
print("\'till void and starfire")
