import openai
from json import loads
from .exc import ModalException
from mSettings import getAPIKey, loadMermaiderPrompt

def callGPT(model: str, promptKeyValue: str, needTool: bool, text: str) -> dict:
	try:
		openai.api_key = getAPIKey()
		myPrompt = loadMermaiderPrompt()
		myPrompt[promptKeyValue].append({"role": "user", "content": text})
		response = openai.chat.completions.create(
			model = model,
			messages = myPrompt[promptKeyValue],
			tools = myPrompt['tools'] if needTool else None
		)
		if response.choices[0].finish_reason == "tool_calls":
			isSuccess = True
			functionArg = loads(response.choices[0].message.tool_calls[0].function.arguments)
			content = functionArg.get('mermaid')
		else:
			if response.choices[0].message.content == "input_error":
				isSuccess = False
				content = "_Invalid input detected._"
			else:
				isSuccess = True
				content = response.choices[0].message.content
		return {
			'content': content,
			'completion': response.usage.completion_tokens,
			'total': response.usage.total_tokens,
			'isSuccess': isSuccess
		}
	except Exception as e:
		raise ModalException(e, "API [1]")
