import openai, furl, requests, openpyxl, verboselogs, coloredlogs, enlighten
import curses, shutil
from os import environ, access, R_OK
from os.path import join, dirname, splitext
from dotenv import load_dotenv
from base64 import b64encode
from json import load, loads
from time import sleep

def loadEnv() -> None:
	dotenvPath = join(dirname(__file__), '.env')
	load_dotenv(dotenvPath)

def getAPIKey() -> str:
	loadEnv()
	OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
	return OPENAI_API_KEY

def getFilePath(fileName: str, dirName: str) -> str:
	filePath = join(dirName, fileName)
	return filePath if access(filePath, R_OK) else None

def readFile(filePath: str) -> str:
	with open(filePath, 'r') as f:
		text = f.read()
	return text

def loadJSONFile(filePath: str) -> dict:
	with open(filePath, 'r') as f:
		jsonData = load(f)
	return jsonData

def printPrompt(data: list) -> None:
	for message in data:
		for key, value in message.items():
			if key == 'role':
				terminalWidth = shutil.get_terminal_size().columns
				messageLength = len(value) + 2
				sideWidth = (terminalWidth - messageLength) // 2
				equals = '=' * sideWidth
				print(f'{equals}^{value}^{equals}')
			else:
				print(f'{value}')
		print('\n\n')
		sleep(2.5)

APIkey = getAPIKey()
prompt = loadJSONFile('data/prompt/prompt.json')
tools = loadJSONFile('data/prompt/tools.json')

def getImageURL(mermaid: str) -> str:
	colorset = "%%{init:{'theme':'forest'}}%%"
	before = f'{colorset}\n{mermaid}'
	try:
		base64EncodedString = b64encode(before.encode()).decode()
		imageURL = furl.furl('https://mermaid.ink/img/')
		imageURL.path.add(base64EncodedString)
		return (imageURL.url)
	except Exception:
		raise

def isImageURL(url: str) -> bool:
	try:
		response = requests.head(url)
		if response.status_code == requests.codes.ok:                                        # Success
			return (True)
		elif response.status_code in [requests.codes.bad_request, requests.codes.not_found]: # ChatGPT generated wrong Mermaid code
			return (False)
		else:                                                                                # API, Network, Server, or something else's error
			response.raise_for_status()
	except Exception:
		raise

def callGPTforTester(model: str, keyValue: str, needTool: int) -> dict:
	try:
		openai.api_key = APIkey
		response = openai.chat.completions.create(
			model = model,
			messages = prompt[keyValue],
			tools = tools['tools'] if needTool else None
		)
		if (response.choices[0].finish_reason == 'tool_calls'):
			isSuccess = True
			functionArg = loads(response.choices[0].message.tool_calls[0].function.arguments)
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

def promptSelector(stdscr) -> tuple[str, int]:
	jsonKeys = list(prompt.keys())
	toolOptions = ['use function calling', 'none']
	# print menu
	def printMenu(options: list, selectedRowIdx: int) -> None:
		stdscr.clear()
		for idx, row in enumerate(options):
			if idx == selectedRowIdx:
				stdscr.addstr(idx, 0, row, curses.A_REVERSE)
			else:
				stdscr.addstr(idx, 0, row)
		stdscr.refresh()
	# select option
	def selectOption(options) -> str:
		currentRow = 0
		while True:
			printMenu(options, currentRow)
			key = stdscr.getch()
			if key == curses.KEY_UP and currentRow > 0:
				currentRow -= 1
			elif key == curses.KEY_DOWN and currentRow < len(options) - 1:
				currentRow += 1
			elif key in [curses.KEY_ENTER, ord('\n')]:
				return options[currentRow]
	curses.curs_set(0)
	selectedValue1 = selectOption(jsonKeys)
	selectedValue2 = selectOption(toolOptions)
	curses.curs_set(1)
	keyValue = selectedValue1
	needTool = 0 if selectedValue2 == 'none' else 1
	return keyValue, needTool

# Class for openpyxl
class DataClass():
	def __init__(self, keyValue: str, fileName: str, title1: str = None, title2: str = None) -> None:
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
	
	def writeCell(self, row: int, status, completion, prompt, total, content: str, url: str, keyValue: str = None, text: str = None):
		self.write_ws.cell(row, 1, status)
		self.write_ws.cell(row, 2, completion)
		self.write_ws.cell(row, 3, prompt)
		self.write_ws.cell(row, 4, total)
		self.write_ws.cell(row, 5, content)
		self.write_ws.cell(row, 6, url)
		if keyValue:
			self.write_ws.cell(row, 7, keyValue)
		if text:
			self.write_ws.cell(row, 8, text)
		self.write_wb.save('data/dataset.xlsx')

# Parent class for test
class TestClass():
	def __init__(self) -> None:
		# logger setting
		self.logger = verboselogs.VerboseLogger('Mermaider_EXP')
		coloredlogs.install(level='VERBOSE', logger=self.logger, fmt='{asctime} {username} {name} [{levelname:<7}] {message}', datefmt='%Y-%m-%d %H:%M:%S', style='{')

		# enlighten setting
	def setup_progress_bar(self, total, desc, unit) -> None:
		self.manager = enlighten.get_manager()
		self.pbar = self.manager.counter(total=total, desc=desc, unit=unit)

		# openai-python setting
	def setup_openai_vars(self, needInitialize: bool=False, needDelete: bool=False, additionalContent: str=None) -> None:
		if needInitialize:
			self.keyValueofPrompt, self.needTool = curses.wrapper(promptSelector)
			self.model = 'gpt-4-1106-preview' if "GPT-4" in self.keyValueofPrompt else 'gpt-3.5-turbo-1106'	
			printPrompt(prompt[self.keyValueofPrompt])
		if needDelete:
			prompt[self.keyValueofPrompt].pop()
		if additionalContent:
			lastMessage = [{'role': 'user', 'content': additionalContent}]
			prompt[self.keyValueofPrompt].append(lastMessage[0])
			printPrompt(lastMessage)

		# openpyxl setting
	def setup_data_class(self, fileName: str, title1: str=None, title2: str=None) -> None:
		self.data = DataClass(keyValue=self.keyValueofPrompt, fileName=splitext(fileName)[0], title1=title1, title2=title2)

	def tester(self, row: int, text: str=None, keyValueofInput: str=None) -> None:
		try:
			self.logger.verbose(f'{self.model}: called')
			response = callGPTforTester(model=self.model, keyValue=self.keyValueofPrompt, needTool=self.needTool)
			self.logger.verbose(f'{self.model}: {response["finish_reason"]}')
			printPrompt([{'role': 'assistant', 'content': response['content']}])
			if response['isSuccess']:
				image_url = getImageURL(response['content'])
				if isImageURL(image_url):
					self.logger.success('Generation is successful')
					status, url = 1, image_url
				else:
					self.logger.error('Generation is failed')
					status, url = 0, 'N/A'
			else:
				self.logger.warning('Invalid input detected')
				status, url = -1, 'N/A'
			self.data.writeCell(row=row, status=status, completion=response['completion'], prompt=response['prompt'], total=response['total'], content=response['content'], url=url, keyValue=keyValueofInput, text=text)
			sleep(0.2)
		except Exception as e:
			self.logger.error(e)
			raise
