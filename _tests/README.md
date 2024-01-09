# function calling vs three backticks

This is a log of the prompt performance testing for the development of Mermaider.</br>In my opinion, it is difficult to keep the quality of the **GPT-3.5** model responses using just the _Few Shot_ technique and other prompt engineering (it worked well on **GPT-4**).</br>One discovery in testing is that _function calling_ is effective in removing backticks from **GPT-3.5** output.

## Result

![graph 1](picture/backticks_rate_plot.png)

- This test used testInput.json to check the response of GPT-3.5 to 10 different C codes.

- Comparing Test 2 and Test 3 shows that negative prompts are effective at some point.

- Plus, _function calling_ is awesome!

However, this behavior is not what is originally expected.
Even though the prompt's _Few-Shot_ example requests **GPT-3.5** to respond with the following parameters:

```
{"role": "assistant", "content": "<response message>"}
```

By using function_calling, Models must respond with a different parameters:

```
{'role': 'assistant',
  'content': None,
  'tool_calls': [{'id': 'id',
    'type': 'function',
    'function': {'name': 'funcname',
     'arguments': '{\n  "arg_1": "Chat",\n  "arg_2": "GPT-",\n  "arg_3": 4\n}'}}]}
```

So, it's weird.

---

In the performance test, backticks appeared just 3 times out of 500 runs (only applied the function calling to GPT-3.5).

![graph 2](picture/success_rate_plot.png)

![graph 3](picture/token_usage_plot.png)

---

> [!NOTE]
> _All the graphs were created with ChatGPT._

## How to use the tester

### Library Installation

```
pip3 install openai furl python-dotenv requests coloredlogs verboselogs enlighten openpyxl
```

### Environment Variable

```bash
OPENAI_API_KEY=your_openai_api_key
```

> [!IMPORTANT]
> You can see the **prompt.json** in `data/input/` and edit as you like.</br>
> When you edit the prompt,include the **GPT-3.5** or **GPT-4** string in the json key.

```bash
# for single input (source: data/code/) test.
python3 singleTester.py [promptKeyValue] [needTool: 0, 1] [fileName] [count: int]

# for multi input (source: .json) test.
python3 multiTester.py [promptKeyValue] [needTool: 0, 1] [fileName] [count: int]
```

> [!WARNING]
> Pay attention to the API usage fees.

## How to use the input generator

The source files in `data/code/` directory are converted to json.
You can make error input using generator.py. Since it is just a random combination of sentences, edit generator.py if necessary.

```bash
python3 generator.py [fileName] [flag: 0 for errorInput, 1 for validInput]
```
