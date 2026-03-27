#section-start setup
#section-start print hello world
print("hello world")
#section-end
#section-start import stuff
from openai import OpenAI
from jinja2 import Template
from os import environ as ENVIRONMENT
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
#section-start make prompt string
template = Template(open("qwen3point5template.jinja").read())
messages = [
    {
        "role":"system",
        "content": "You are Gryph Four, A helpful AI agent."
    },
    {
        "role":"user",
        "content":"Hey Gryph. What is the current weather in Sacramento, CA?"
    }
]
tools = [
    {
      "name": 'get_weather',
      "description": 'Get current weather information for a location',
      "parameters": {
        "type": 'object',
        "properties": {
          "location": {
            "type": 'string',
            "description": 'The city and state, e.g. San Francisco, CA',
          },
          "unit": {
            "type": 'string',
            "enum": [
              'celsius',
              'fahrenheit',
            ],
            "description": 'The unit of temperature to use',
          },
        },
        "required": [
          'location',
        ],
      },
    },
  ]
prompt_string = template.render(**{"messages":messages, "tools":tools, "add_generation_prompt":True, "enable_thinking":False})
print(f"{prompt_string=}")
#section-end
#section-start get response
response=engine.completions.create(
    model=PREFFERED_MODEL,
    prompt=prompt_string,
    max_tokens=4096,
    temperature=0.7
    )
#section-end
print(response.choices[0].text)
print("\'till void and starfire")
