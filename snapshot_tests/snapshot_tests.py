#section-start import stuff!
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import qwen_interface
from jinja2 import Template
from qwen_interface import SystemMessage, UserMessage, AssistantMessage, ToolMessage, ToolParameter, EnumToolParameter, parse_response, compile_prompt, get_option_prefix, NoThinkOption, StandardOption, ForceToolOption, CleanSlateOption, ForceMessageStartOption
#section-end
#section-start load template
template = Template(open("qwen3point5template.jinja").read())
#section-end
#section-start define tests
def standard_prompt_test(): #section-start
    return(
        compile_prompt(
            messages = [
                SystemMessage("You are the helpful AI Gryph Four"),
                UserMessage("This is Operator. Wake up. Report system status.")
                    ],
            tool_descriptions=None,
            option=StandardOption()
        )
    )
#section-end
def nothink_test(): #section-start
    return(
        compile_prompt(
            messages = [
                SystemMessage("You are the helpful AI Gryph Four"),
                UserMessage("This is Operator. Wake up. Report system status.")
                    ],
            tool_descriptions=None,
            option=NoThinkOption()
        )
    )
#section-end
def force_tool_test(): #section-start
    return(
        compile_prompt(
            messages = [
                SystemMessage("You are the helpful AI Gryph Four"),
                UserMessage("This is Operator. Wake up. Report system status.")
                    ],
            tool_descriptions=None,
            option=ForceToolOption()
        )
    )
#section-end
def force_specific_tool_test(): #section-start
    return(
        compile_prompt(
            messages = [
                SystemMessage("You are the helpful AI Gryph Four"),
                UserMessage("This is Operator. Wake up. Report system status.")
                    ],
            tool_descriptions=None,
            option=ForceToolOption("get_weather")
        )
    )
#section-end
def clean_slate_test(): #section-start
    return(
        compile_prompt(
            messages = [
                SystemMessage("You are the helpful AI Gryph Four"),
                UserMessage("This is Operator. Wake up. Report system status.")
                    ],
            tool_descriptions=None,
            option=CleanSlateOption()
        )
    )
#section-end
def forced_message_test(): #section-start
    return(
        compile_prompt(
            messages = [
                SystemMessage("You are the helpful AI Gryph Four"),
                UserMessage("This is Operator. Wake up. Report system status.")
                    ],
            tool_descriptions=None,
            option=ForceMessageStartOption("You've got a lot of guts coming back here.\n")
        )
    )
#section-end
def force_tool_prefix_isolation_test():
    return(get_option_prefix(ForceToolOption("get_weather")))
def nothink_prefix_isolation_test():
    return(get_option_prefix(NoThinkOption()))
#section-start enumerate tests
tests = {
    "standard_prompt_test":standard_prompt_test,
    "nothink_test":nothink_test,
    "force_tool_test":force_tool_test,
    "force_specific_tool_test":force_specific_tool_test,
    "clean_slate_test":clean_slate_test,
    "forced_message_test":forced_message_test,
    "force_tool_prefix_isolation_test":force_tool_prefix_isolation_test,
    "nothink_prefix_isolation_test":nothink_prefix_isolation_test
}
#section-end
#section-end
