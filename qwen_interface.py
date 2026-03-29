#section-start imports
import re as re
#section-end
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
