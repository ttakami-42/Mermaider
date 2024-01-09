import openai, json, os, base64, furl, requests, openpyxl
from os.path import join, dirname
from dotenv import load_dotenv

def loadEnv():
	dotenvPath = join(dirname(__file__), '.env')
	load_dotenv(dotenvPath)

def getAPIKey() -> str:
	loadEnv()
	OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
	return OPENAI_API_KEY

def loadJsonFile(fileName: str) -> dict:
	with open(fileName, 'r') as f:
		jsonData = json.load(f)
	return jsonData

APIkey = getAPIKey()
prompt = loadJsonFile('data/prompt/prompt.json')

class DataClass():
	def __init__(self, keyValue: str, fileName: str, title1: str = None, title2: str = None):
		self.write_wb = openpyxl.load_workbook('data/dataset.xlsx')
		sheetName = f'{keyValue}-{fileName}'
		existingSheets = self.write_wb.sheetnames
		if sheetName in existingSheets:
			self.write_ws = self.write_wb[sheetName]
		else:
			self.write_ws = self.write_wb.create_sheet(sheetName)
			self.writeCell(1, "status", "comp", "prompt", "total", "mermaid", "url", title1, title2)
		self.empty_row = 2
		for row in self.write_ws.iter_rows(min_row=2):
			if row[0].value is not None:
				self.empty_row += 1
			else:
				break
	
	def writeCell(self, row: int, status, completion, prompt, total, content: str, url: str, inputKeyValue: str = None, text: str = None):
		self.write_ws.cell(row, 1, status)
		self.write_ws.cell(row, 2, completion)
		self.write_ws.cell(row, 3, prompt)
		self.write_ws.cell(row, 4, total)
		self.write_ws.cell(row, 5, content)
		self.write_ws.cell(row, 6, url)
		if inputKeyValue:
			self.write_ws.cell(row, 7, inputKeyValue)
		if text:
			self.write_ws.cell(row, 8, text)
		self.write_wb.save('data/dataset.xlsx')


def getImageURL(mermaid: str):
	colorset = "%%{init:{'theme':'forest'}}%%"
	before = f'{colorset}\n{mermaid}'
	try:
		base64_encoded_string = base64.b64encode(before.encode()).decode()
		url = furl.furl('https://mermaid.ink/img/')
		url.path.add(base64_encoded_string)
		return (url.url)
	except Exception:
		raise

def isImageURL(url: str):
	try:
		response = requests.head(url)
		if response.status_code == requests.codes.ok:                                        # Success
			return (True)
		elif response.status_code in [requests.codes.bad_request, requests.codes.not_found]: # chatGPT generated wrong Mermaid code
			return (False)
		else:                                                                                # API, Network, Server, or something else's error
			response.raise_for_status()
	except Exception:
		raise

def callGPTforTester(model: str, promptKeyValue: str, needTool: int) -> dict:
	try:
		openai.api_key = APIkey
		tools = prompt['tools'] if needTool else None
		response = openai.chat.completions.create(
			model = model,
			messages = prompt[promptKeyValue],
			tools = tools,
		)
		if (response.choices[0].finish_reason == 'tool_calls'):
			isSuccess = True
			functionArg = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
			content = functionArg.get('mermaid')
		else:
			isSuccess = False if (response.choices[0].message.content == "input_error") else True
			content = response.choices[0].message.content
		return {
			'content': content,
			'completion': response.usage.completion_tokens,
			'prompt': response.usage.prompt_tokens,
			'total': response.usage.total_tokens,
			'finish_reason': response.choices[0].finish_reason,
			'isSuccess': isSuccess
		}
	except Exception:
		raise
