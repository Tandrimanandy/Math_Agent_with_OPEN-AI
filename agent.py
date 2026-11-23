import os 
import json
from openai import OpenAI
from math_tool import add_numbers, subtract_numbers


MODEL = "gpt-6-astra"


client = OpenAI()

TOOLS = [
    {
        "type": "function",
        "name": "add_numbers",
        "description": "Add two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "subtract_numbers",
        "description": "Subtract b from a.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"],
            "additionalProperties": False
        },
        "strict": True
    }
]

FUNCTIONS = {
    "add_numbers": add_numbers,
    "subtract_numbers": subtract_numbers
}


def run_agent(question):
    response = client.responses.create(
        model=MODEL,
        instructions=(
            "You are a Math AI Agent. Use add_numbers for addition "
            "and subtract_numbers for subtraction. Do not guess "
            "calculation results. Use tools when calculation is needed."
        ),
        input=question,
        tools=TOOLS
    )

    while True:
        calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not calls:
            return response.output_text

        tool_outputs = []

        for call in calls:
            arguments = json.loads(call.arguments)
            function = FUNCTIONS[call.name]
            result = function(**arguments)

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": str(result)
            })

        response = client.responses.create(
            model=MODEL,
            instructions=(
                "You are a Math AI Agent. Explain results simply."
            ),
            input=[*response.output, *tool_outputs],
            tools=TOOLS
        )


if __name__ == "__main__":
    question = input("Ask a math question: ")
    print("\nAI Agent Answer:")
    print(run_agent(question))