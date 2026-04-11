#section-start setup
#section-start print hello world
print("hello world")
#section-end
#section-start import stuff
from openai import OpenAI
from os import environ as ENVIRONMENT
from qwen_interface.qwen_interface import SystemMessage, UserMessage, AssistantMessage, ToolMessage, ToolParameter, EnumToolParameter, continue_conversation, NoThinkOption, Tool, get_function_from_tool_list
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
tools = [ #section-start
    Tool(
        name="get_weather",
        description="Get current weather information for a location",
        function=get_weather,
        required_parameters=[
            ToolParameter("location", "The city and state, e.g. San Francisco, CA")
        ],
        optional_parameters=[
            EnumToolParameter("unit", "The unit of temperature to use", ["celsius", "fahrenheit"])
        ]
    ),
    Tool(
        name="get_weather_preference",
        description="get the user\'s weather preference",
        function=get_weather_preference
    )
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
        messages = continue_conversation(
            messages=messages,
            tools=tools,
            option=NoThinkOption(),
            raw_completion_function=raw_completion_function)
        if "tool_calls" in messages[-1]:
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
            tool_args = tool_call["function"]["arguments"]
            tool_function = get_function_from_tool_list(
                tool_name=tool_name,
                tool_list=tools
            )
            tool_response = ToolMessage(tool_function(**tool_args))
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
