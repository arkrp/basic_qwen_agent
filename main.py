#section-start setup
#section-start print hello world
print("hello world")
#section-end
#section-start import stuff
from openai import OpenAI
from jinja2 import Template
from os import environ as ENVIRONMENT
import re as re
#section-end
#section-start set configuration constants
OPENAI_API_BASE = ENVIRONMENT["OPENAI_API_BASE"]
OPENAI_API_KEY = ENVIRONMENT["OPENAI_API_KEY"]
PREFFERED_MODEL = "model.gguf"
#section-end
#section-start print preload complete
print("preload complete")
#section-end
#section-start load the jinja template
template = Template(open("qwen3point5template.jinja").read())
#section-end
#section-end
#section-start define conversation abstractions!
def SystemMessage(content): #section-start
    """Makes a System Message for a conversation"""
    return({"role":"system", "content":content})
#section-end
def UserMessage(content): #section-start
    """Makes a User Message for a conversation"""
    return({"role":"user", "content":content})
#section-end
def ToolMessage(content): #section-start
    """Makes a Tool Message for a conversation"""
    return({"role":"tool", "content":content})
#section-end
def AssistantMessage(content): #section-start
    """Makes an Assistant Message for a conversation"""
    return({"role":"assistant", "content":content})
#section-end
def ToolDescription(name: str, description: str, required_parameters={}, optional_parameters={}): #section-start
    """Takes name description and Tool Parameters to make a tool description for jinja"""
    required_list = [i for i in required_parameters]
    return({
            "name":name,
            "description": description,
            "parameters":{
                "type":"object",
                "properties":required_parameters|optional_parameters,
                "required":required_list
            }
        })
#section-end
def ToolParameter(name: str, description: str): #section-start
    """defines a paramter of a tool used in ToolDescription"""
    return({name:{"type":"string",
                  "description":description
                  }})
#section-end
def EnumToolParameter(name: str, description: str, valid_inputs: list[str]): #section-start
    """defines a paramter of a tool with a defined fixed number of inputs used in ToolDescription"""
    return({name:{"type":"string",
                  "enum": valid_inputs,
                  "description":description
                  }})
#section-end
def ParseResponse(response): #section-start
    """ #section-start
    Parses the response the language model gives into a AssitantMessage with the relevant tool calls
    """
    #section-end
    #section-start parse messages with tool calls
    if len(re.findall("<tool_call>", response))!=0:
        content = re.findall("\\A(.*?)<tool_call>", response)[0]
        def ParseFunctionString(function_response): #section-start
            function_name = re.findall("<function=([^>]*)>", function_response)[0]
            parameters = dict(re.findall("<parameter=([^>]*)>\n((?:.|\n)*?)\n</parameter>", function_response))
            return({"type":"function", "function":{"name":function_name, "arguments":parameters}})
        #section-end
        #section-start parse any existing tool calls
        try:
            function_strings = re.findall("<tool_call>\n((?:\n|.)*?)\n</tool_call>", response)
            tool_calls = [ParseFunctionString(i) for i in function_strings]
        #section-end
        #section-start deal with tool parsing errors
        except Exception as e:
            raise RuntimeError("Could not process malformed tool call:\n" + response) from e
        #section-end
        return({"role":"assistant", "content":content, "tool_calls":tool_calls})
    #section-end
    #section-start parse messages without tool calls
    else:
        return({"role":"assistant", "content":response})
    #section-end
#section-end
#section-end
#section-start connect to completion engine
engine = OpenAI(
    base_url=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY
)
#section-end
#section-start make prompt string
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
    return("The user prefers temperatures above 30 degrees celsius")
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
speaker="user"
while(True):
    if speaker=="user":
        messages.append(UserMessage(input("User: ")))
        speaker="assistant"
    elif speaker="assistant":


    
    #section-start compile prompt
    prompt_string = template.render(**{"messages":messages, "tools":tool_descriptions, "add_generation_prompt":True, "enable_thinking":False})
    #section-end
    #section-start generate with llm
    response=engine.completions.create(
        model=PREFFERED_MODEL,
        prompt=prompt_string,
        max_tokens=4096,
        temperature=0.7
        ).choices[0].text
    #section-end
    print(response)
    messages.append(ParseResponse(response))
    if "tool_calls" in messages[-1]:
        for tool_call in messages[-1]["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            print("tool_name: "+tool_name)
            tool_args = tool_call["function"]["arguments"]
            print("function_args: "+repr(tool_args))
            print("tool_call_result: "+tools[tool_name](**tool_args))
    
#print("prompt_string: "+ prompt_string)
#section-end
#section-start test parser
example_parse_message_tools = """message that is before the tool calls<tool_call>
<function=get_weather_preference>
</function>
</tool_call>
<tool_call>
<function=get_weather>
<parameter=location>
Sacramento, CA
</parameter>
<parameter=unit>
Celsius
</parameter>
<parameter=unit>
kelvin
</parameter>
</function>
</tool_call>
"""
example_parse_message = "message that is before the tool calls"
print(ParseResponse(example_parse_message))
print(ParseResponse(example_parse_message_tools))
#section-end
#print(repr(response.choices[0].text))
#print("\'till void and starfire")
