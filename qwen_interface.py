#section-start setup
#section-start imports
import re as re
from jinja2 import Template
#section-end
#section-start load the jinja template
template = Template(open("qwen3point5template.jinja").read())
#section-end
#section-end
#section-start messages
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
#section-end
#section-start tool builders
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
#section-end
#section-start prompt_compilation_option
def NoThinkOption():
    return({"add_generation_prompt":True, "enable_thinking":False})
def StandardOption():
    return({"add_generation_prompt":True, "enable_thinking":True})
def ForceToolOption(tool=None):
    if tool is None:
        tool=True
    return({"add_generation_prompt":True, "force_tool":tool})
def CleanSlateOption():
    return({"add_generation_prompt":True, "clean_slate":True})
def ForceMessageStartOption(forced_response_start):
    return({"add_generation_prompt":True, "forced_response_start":forced_response_start})
#section-end
def parse_response(response): #section-start
    """ #section-start
    Parses the response the language model gives into a AssitantMessage with the relevant tool calls
    """
    #section-end
    #section-start parse messages with tool calls
    if len(re.findall("<tool_call>", response))!=0:
        content_search = re.findall("\\A(.*?)<tool_call>", response)
        if len(content_search) != 0:
            content = content_search[0]
        else:
            content = ""
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
def compile_prompt(*, messages, option=NoThinkOption, tool_descriptions=None): #section-start
        prompt_string = template.render(**({"messages":messages, "tools":tool_descriptions} | option))
        return(prompt_string)
#section-end
def get_option_prefix(option): #section-start
    prefix_untrimmed_formatting = compile_prompt(
        messages=[SystemMessage("A"), UserMessage("A")],
        option=option,
        tool_descriptions=None)
    prefix_trimmed_formatting = compile_prompt(
        messages=[SystemMessage("A"), UserMessage("A")],
        option=CleanSlateOption(),
        tool_descriptions=None)
    prefix = prefix_untrimmed_formatting[len(prefix_trimmed_formatting):None]
    return(prefix)
#section-end
def continue_conversation(*, messages, option=NoThinkOption, tool_descriptions=None, raw_completion_function): #section-start
    compiled_prompt = compile_prompt(
        messages=messages,
        option=option,
        tool_descriptions=tool_descriptions)
    completion = raw_completion_function(compiled_prompt)
    prefix = get_option_prefix(option)
    return(prefix+completion)
#section-end
