<h1 align="center">Math AI Agent</h1>

<p align="center">
  A tool-using AI agent that performs arithmetic through OpenAI function calling, so the model never guesses a calculation.
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.9+"></a>
  <a href="https://platform.openai.com/"><img src="https://img.shields.io/badge/OpenAI-Platform-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI Platform"></a>
  <a href="https://platform.openai.com/docs/api-reference/responses"><img src="https://img.shields.io/badge/OpenAI-Responses%20API-10A37F?style=for-the-badge&logo=openai&logoColor=white" alt="Responses API"></a>
  <a href="https://pypi.org/project/openai/"><img src="https://img.shields.io/badge/SDK-openai-000000?style=for-the-badge&logo=python&logoColor=white" alt="openai SDK"></a>
  <a href="https://platform.openai.com/docs/guides/function-calling"><img src="https://img.shields.io/badge/Project-Function%20Calling%20Agent-0A7F5A?style=for-the-badge" alt="Function Calling Agent"></a>
</p>

<table align="center">
  <tr>
    <th>Category</th>
    <th>Technology</th>
    <th>Documentation</th>
  </tr>
  <tr>
    <td>Language</td>
    <td><a href="https://www.python.org/">Python 3.9+</a></td>
    <td><a href="https://docs.python.org/3/">docs.python.org</a></td>
  </tr>
  <tr>
    <td>AI Provider</td>
    <td><a href="https://platform.openai.com/">OpenAI</a></td>
    <td><a href="https://platform.openai.com/docs">platform.openai.com/docs</a></td>
  </tr>
  <tr>
    <td>API</td>
    <td><a href="https://platform.openai.com/docs/api-reference/responses">Responses API</a></td>
    <td><a href="https://platform.openai.com/docs/api-reference/responses">API reference</a></td>
  </tr>
  <tr>
    <td>SDK</td>
    <td><a href="https://pypi.org/project/openai/">openai (Python)</a></td>
    <td><a href="https://github.com/openai/openai-python">GitHub repository</a></td>
  </tr>
  <tr>
    <td>Pattern</td>
    <td><a href="https://platform.openai.com/docs/guides/function-calling">Function calling</a></td>
    <td><a href="https://platform.openai.com/docs/guides/function-calling">Guide</a></td>
  </tr>
</table>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Code Reference](#code-reference)
- [Design Decisions](#design-decisions)
- [Known Limitations](#known-limitations)
- [Possible Improvements](#possible-improvements)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

Math AI Agent is a small Python project that answers math questions in natural language. Instead of asking a language model to calculate results directly, the project gives the model two callable tools, `add_numbers` and `subtract_numbers`. The model decides when a calculation is needed, requests the appropriate tool, receives the verified result from Python, and then explains the answer in plain language.

This pattern keeps arithmetic deterministic and makes the model's behavior easy to inspect, since every calculation is visible as a tool execution.

## Features

- Natural-language math questions answered by an OpenAI model
- Tool-based arithmetic: addition and subtraction run in Python, not inside the model
- Strict JSON schemas for tool arguments, so the model supplies only valid parameters
- An agent loop that keeps executing tool calls until the model returns a final answer
- Visible execution log (`[TOOL EXECUTED] ...`) that confirms when each tool runs
- Standalone test mode in `math_tool.py` that works without an API key

## How It Works

```
 User question
      │
      ▼
 run_agent(question)
      │
      ▼
 client.responses.create()  ──►  Model decides: answer directly, or call a tool
      │
      ├── No function_call items ──►  Return response.output_text  ──►  Final answer
      │
      └── function_call items found
              │
              ▼
          Look up function in FUNCTIONS
              │
              ▼
          Run Python function (add_numbers / subtract_numbers)
              │
              ▼
          Wrap result as function_call_output
              │
              ▼
          client.responses.create(input=[previous output, tool outputs])
              │
              └──► Loop back to the check above
```

## Project Structure

```
math-ai-agent/
├── agent.py       # OpenAI agent: tool schemas, dispatch table, and agent loop
├── math_tool.py   # Python arithmetic functions exposed to the agent as tools
└── README.md      # Project documentation
```

## Prerequisites

- Python 3.9 or newer
- An OpenAI account with an active API key
- The `openai` Python package, version 1.66 or newer, which includes the Responses API

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/math-ai-agent.git
   cd math-ai-agent
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. Install the dependency:

   ```bash
   pip install --upgrade openai
   ```

4. Set your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY="your-api-key"          # macOS / Linux
   setx OPENAI_API_KEY "your-api-key"            # Windows (restart the terminal afterward)
   ```

> **Security note:** Never commit your API key to source control. Keep it in an environment variable or a local `.env` file that is listed in `.gitignore`.

## Configuration

| Setting | Location | Default | Purpose |
|---|---|---|---|
| `OPENAI_API_KEY` | Environment variable | None (required) | Authenticates requests. Read automatically by `OpenAI()`. |
| `MODEL` | `agent.py` | `"gpt-6-astra"` | Model ID passed to `responses.create()`. Change it to any model that supports the Responses API and function calling. |

## Usage

Run the interactive agent:

```bash
python agent.py
```

Example session (wording of the final answer may vary):

```
Ask a math question: What is 25 plus 17, and then subtract 10 from the result?

[TOOL EXECUTED] add_numbers
[TOOL EXECUTED] subtract_numbers

AI Agent Answer:
25 + 17 = 42, and 42 - 10 = 32. The final answer is 32.
```

Run the arithmetic tools on their own, without calling the API:

```bash
python math_tool.py
```

Expected output:

```
[TOOL EXECUTED] add_numbers
Addition:  42
[TOOL EXECUTED] subtract_numbers
Subtraction:  8
```

---

## Code Reference

This section documents every function, method, and constant in the project, including why each one exists and where it is used.

### `math_tool.py`

This module contains plain Python arithmetic. It has no dependency on OpenAI, which keeps the calculation logic testable and reusable on its own.

#### `add_numbers(a: float, b: float) -> float`

| Item | Details |
|---|---|
| **Purpose** | Returns the sum of two numbers. |
| **Parameters** | `a`: first number. `b`: second number. |
| **Returns** | The sum `a + b`. |
| **Used by** | `agent.py`, through the `FUNCTIONS` dispatch table, whenever the model requests the `add_numbers` tool. |
| **Why it exists** | Arithmetic is performed in Python so the answer is exact and verifiable, rather than predicted by the language model. |
| **Side effect** | Prints `[TOOL EXECUTED] add_numbers` to the console, which shows that the tool actually ran. |

#### `subtract_numbers(a: float, b: float) -> float`

| Item | Details |
|---|---|
| **Purpose** | Returns `a` minus `b`. |
| **Parameters** | `a`: the number to subtract from. `b`: the number to subtract. |
| **Returns** | The difference `a - b`. |
| **Used by** | `agent.py`, through the `FUNCTIONS` dispatch table, whenever the model requests the `subtract_numbers` tool. |
| **Why it exists** | Same reason as `add_numbers`. Order matters, so the parameter names make clear that `b` is subtracted from `a`. |
| **Side effect** | Prints `[TOOL EXECUTED] subtract_numbers` to the console. |

#### `if __name__ == "__main__":` block

| Item | Details |
|---|---|
| **Purpose** | Runs a quick self-test when the file is executed directly (`python math_tool.py`). |
| **Behavior** | Calls `add_numbers(25, 17)` and `subtract_numbers(25, 17)` and prints both results. |
| **Why it exists** | Lets developers verify the arithmetic functions without an API key or network access. It is skipped when the module is imported by `agent.py`. |

---

### `agent.py`

This module connects the OpenAI model to the arithmetic tools and runs the agent loop.

#### Imports

| Import | Purpose |
|---|---|
| `os` | Imported but not currently used. It can be removed. |
| `json` | Parses the JSON string of tool arguments returned by the model (`json.loads`). |
| `OpenAI` (from `openai`) | The SDK client used to send requests to the Responses API. |
| `add_numbers`, `subtract_numbers` (from `math_tool`) | The Python functions the agent is allowed to call. |

#### `MODEL` (constant)

| Item | Details |
|---|---|
| **Type** | `str` |
| **Purpose** | Specifies which model handles every request in the agent. |
| **Why it is a constant** | Keeps the model name in one place so it can be changed without editing the logic. |

#### `client = OpenAI()`

| Item | Details |
|---|---|
| **Purpose** | Creates a single reusable API client for the whole module. |
| **Authentication** | Reads the `OPENAI_API_KEY` environment variable automatically. |
| **Why it is at module level** | The client is created once and reused across every call to `run_agent`, instead of being recreated per question. |

#### `TOOLS` (constant)

A list of tool definitions in the format the Responses API expects. Each entry tells the model what a tool is called, what it does, and which arguments it accepts. The model reads these definitions and decides when to call them.

| Field | Value in this project | Why |
|---|---|---|
| `type` | `"function"` | Declares a custom function tool. |
| `name` | `"add_numbers"` / `"subtract_numbers"` | Must match a key in `FUNCTIONS`. |
| `description` | Short sentence describing the tool | The model uses this text to choose the right tool. |
| `parameters` | JSON Schema object with `a` and `b` as `number` | Defines the required inputs. |
| `required` | `["a", "b"]` | Both numbers must be provided. |
| `additionalProperties` | `False` | Rejects any extra fields the model might invent. |
| `strict` | `True` | Asks the model to follow the schema exactly, so arguments are always valid. |

#### `FUNCTIONS` (dispatch table)

```python
FUNCTIONS = {
    "add_numbers": add_numbers,
    "subtract_numbers": subtract_numbers
}
```

| Item | Details |
|---|---|
| **Type** | `dict` mapping tool name (`str`) to Python callable |
| **Purpose** | Connects the name the model requests to the actual function that runs. |
| **Why it exists** | When the model returns `call.name`, the code looks up the matching function here instead of using long `if/elif` chains. Adding a new tool means adding one entry here and one entry in `TOOLS`. |

#### `run_agent(question: str) -> str`

The main function. It sends a question to the model, executes any tools the model requests, and returns the final text answer.

| Item | Details |
|---|---|
| **Parameter** | `question`: the user's math question as a string. |
| **Returns** | The model's final answer as a string (`response.output_text`). |
| **Used by** | The `__main__` block in `agent.py`. |

**How it works, step by step:**

1. **Initial request.** Calls `client.responses.create()` with the model, a system-style `instructions` string that tells the model to use the tools and not guess, the user's `question` as `input`, and the `TOOLS` list.
2. **Check for tool calls.** Scans `response.output` for items whose `type` is `"function_call"`.
3. **Return when done.** If no tool calls are found, the model has produced its final answer, so the function returns `response.output_text`.
4. **Execute tools.** For each tool call:
   - Parses the arguments string with `json.loads(call.arguments)`.
   - Looks up the Python function in `FUNCTIONS` using `call.name`.
   - Calls the function with the parsed arguments as keyword arguments (`function(**arguments)`).
5. **Package results.** Creates a `function_call_output` item for each call, linked by `call.call_id`, with the result converted to a string.
6. **Continue the conversation.** Sends a new request containing the model's previous output and the tool outputs, then returns to step 2.

The loop continues until the model stops requesting tools.

#### `if __name__ == "__main__":` block

| Item | Details |
|---|---|
| **Purpose** | Provides a command-line entry point. |
| **Behavior** | Prompts for a question with `input()`, calls `run_agent()`, and prints the answer. |
| **Why it is guarded** | Ensures the interactive prompt runs only when the file is executed directly, not when it is imported. |

---

### OpenAI SDK Methods and Attributes Used

| Method / attribute | Where used | Purpose |
|---|---|---|
| `OpenAI()` | `agent.py` | Creates the API client. |
| `client.responses.create(...)` | `run_agent` (twice) | Sends a request to the Responses API. Accepts `model`, `instructions`, `input`, and `tools`. |
| `response.output` | `run_agent` | A list of output items, including messages and function calls. |
| `response.output_text` | `run_agent` | A convenience property that returns the model's final text. |
| `item.type` | `run_agent` | Identifies each output item. The code checks for `"function_call"`. |
| `call.name` | `run_agent` | The name of the tool the model wants to run. |
| `call.arguments` | `run_agent` | The tool arguments as a JSON-encoded string. |
| `call.call_id` | `run_agent` | Unique ID that links a tool result back to the request that caused it. |

---

## Design Decisions

- **Tools instead of model arithmetic.** Language models can make arithmetic mistakes. Running the calculations in Python guarantees correct results.
- **Strict schemas.** `strict: True` and `additionalProperties: False` ensure the model returns only the expected fields with the correct types.
- **Separation of concerns.** `math_tool.py` contains pure logic with no API dependency. `agent.py` handles orchestration. This makes each part easy to test and reuse.
- **Dispatch table over conditionals.** `FUNCTIONS` maps names to functions directly, so the agent loop does not need to change when new tools are added.
- **Visible tool execution.** The `[TOOL EXECUTED]` messages make it clear when Python, rather than the model, produced a result.

## Known Limitations

- **No iteration limit.** The `while True` loop has no maximum number of rounds. A misbehaving model could keep requesting tools indefinitely.
- **No error handling for tools.** An unknown tool name raises a `KeyError`, malformed arguments raise a JSON error, and an exception inside a tool stops the program.
- **Follow-up requests carry limited context.** After the first call, the loop sends only the model's previous output and the tool results. The original question and the first `instructions` string are not resent. The second `instructions` value is also different from the first.
- **Unused import.** `import os` in `agent.py` is not needed.
- **Limited operations.** Only addition and subtraction are supported.

## Possible Improvements

- Add a maximum iteration count to the agent loop.
- Wrap tool execution in `try/except` and return error messages to the model as tool output.
- Use `previous_response_id` or resend the full conversation so context is explicit on every turn.
- Add multiplication, division, and exponentiation tools using the same pattern.
- Add unit tests for `math_tool.py` with `pytest`, and mock the API client for `agent.py`.
- Add a `requirements.txt` file and a `.gitignore` that excludes `.env` and `__pycache__/`.

## Troubleshooting

| Problem | Solution |
|---|---|
| `OpenAIError: The api_key client option must be set` | Set the `OPENAI_API_KEY` environment variable and restart your terminal. |
| `ModuleNotFoundError: No module named 'openai'` | Run `pip install --upgrade openai`. |
| `ModuleNotFoundError: No module named 'math_tool'` | Run the program from the folder that contains `math_tool.py`. |
| `AttributeError: 'OpenAI' object has no attribute 'responses'` | Upgrade the SDK with `pip install --upgrade openai`. The Responses API requires a newer version. |
| Model not found or access error | Change `MODEL` in `agent.py` to a model available on your OpenAI account. |

---

## License

This project does not yet specify a license. Add a `LICENSE` file (for example, MIT) and update this section to match.

---

<p align="center">
  Built with <a href="https://www.python.org/">Python</a> and <a href="https://platform.openai.com/">OpenAI</a>
</p>
