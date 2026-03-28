#section-start setup
#section-start print hello world
print("hello world")
#section-end
#section-start import stuff
from openai import OpenAI
from jinja2 import Template
from os import environ as ENVIRONMENT
import xml.etree.ElementTree as xml
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
#section-start load the jinja template
template = Template(open("qwen3point5template.jinja").read())
#section-end
#section-start make nice abstractions!
def SystemMessage(content): #section-start
    return({"role":"system", "content":content})
#section-end
def UserMessage(content): #section-start
    return({"role":"user", "content":content})
#section-end
def ToolMessage(content): #section-start
    return({"role":"tool", "content":content})
#section-end
def AssistantMessage(content, tool_calls): #section-start
    return({"role":"assistant", "content":content, "tool_calls": tool_calls})
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
    return({name:{"type":"string",
                  "description":description
                  }})
#section-end
def EnumToolParameter(name: str, description: str, valid_inputs: list[str]): #section-start
    return({name:{"type":"string",
                  "enum": valid_inputs,
                  "description":description
                  }})
#section-end
#Parameters should be unioned | together

#section-end
#section-start make prompt string
messages = [ #section-start
    SystemMessage("You are Gryph Four, A helpful AI agent."),
    UserMessage("Hey Gryph. Is the weather preferable in Sacramento, CA?")
]
#section-end
tools = [ #section-start
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
prompt_string = template.render(**{"messages":messages, "tools":tools, "add_generation_prompt":True, "enable_thinking":False})
print("prompt_string: "+ prompt_string)
#section-end
#section-start get response
response=engine.completions.create(
    model=PREFFERED_MODEL,
    prompt=prompt_string,
    max_tokens=4096,
    temperature=0.7
    )
#section-end
print(xml.fromstring(
'<tool_call>\n<funcssstion="get_weather_preference">\n</function>\n</tool_call>\n<tool_call>\n<function="get_weather">\n<parameter="location">\nSacramento, CA\n</parameter>\n</function>\n</tool_call>'))
print(repr(response.choices[0].text))
print(xml.fromstring(response.choices[0].text))
print("\'till void and starfire")
