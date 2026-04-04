#section-start import stuff!
import qwen_interface
from jinja2 import Template
#section-end
#section-start load template
template = Template(open("qwen3point5template.jinja").read())
#section-end
#section-start define tests
def standard_prompt_test():
    return("hello!") #TODO make this actually return a rendered prompt
#section-start enumerate tests
tests = {
    "standard_prompt_test":standard_prompt_test,
#    "nothink_test":nothink_test,
#    "force_tool_test":force_tool_test,
#    "force_specific_tool_test":force_specific_tool_test,
}
#section-end
#section-end
