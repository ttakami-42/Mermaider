import verboselogs, coloredlogs, time, enlighten, sys, os, pprint
import utils

class SingleTestClass():
	def __init__(self, model: str, promptKeyValue: str, needTool: int, fileName: str, count: int):
		# logger setting
		self.logger = verboselogs.VerboseLogger('Mermaider_EXP')
		coloredlogs.install(level='VERBOSE', logger=self.logger, fmt='{asctime} {username} {name} [{levelname:<7}] {message}', datefmt='%Y-%m-%d %H:%M:%S', style='{')

		# openai-python setting
		self.model = model
		with open(f'data/input/code/{fileName}', 'r') as f:
			self.text = f.read()
		self.promptKeyValue = promptKeyValue
		self.needTool = needTool

		# enlighten setting
		self.manager = enlighten.get_manager()
		self.pbar = self.manager.counter(total=count, desc='Ticks', unit='ticks')

		# class for openpyxl
		self.data = utils.DataClass(keyValue=promptKeyValue, fileName=os.path.splitext(fileName)[0])

	def singleTester(self, row: int) -> None:
		try:
			self.logger.verbose(f'{self.model}: called')
			response = utils.callGPTforTester(model=self.model, promptKeyValue=self.promptKeyValue, needTool=self.needTool)
			self.logger.verbose(f'{self.model}: {response["finish_reason"]}')
			if response['isSuccess']:
				image_url = utils.getImageURL(response['content'])
				if utils.isImageURL(image_url):
					self.logger.success('Generation is successful')
					status, url = 1, image_url
				else:
					self.logger.error('Generation is failed')
					status, url = 0, 'N/A'
			else:
				self.logger.warning('Invalid input detected')
				status, url = -1, 'N/A'
			self.data.writeCell(row=row, status=status, completion=response['completion'], prompt=response['prompt'], total=response['total'], content=response['content'], url=url)
		except Exception as e:
			self.logger.error(e)
			raise

if __name__ == '__main__':
	args = sys.argv
	if len(args) == 5 and args[2].isdigit() and args[4].isdigit() and int(args[2]) in [0, 1]:
		promptKeyValue, needTool, fileName, count = args[1], int(args[2]), args[3], int(args[4])
		if "GPT-4" in promptKeyValue:
			model = 'gpt-4-1106-preview'
		elif "GPT-3.5" in promptKeyValue:
			model = 'gpt-3.5-turbo-1106'
		else:
			model = None
		if model:
			test = SingleTestClass(model=model, promptKeyValue=promptKeyValue, needTool=needTool, fileName=fileName, count=count)
			utils.prompt[promptKeyValue].append({'role': 'user', 'content': test.text})
			pprint.pprint(utils.prompt[promptKeyValue])
			for i in range(0, count):
				test.logger.info('Processing step %s' % (i + 1))
				test.singleTester(row=test.data.empty_row + i)
				time.sleep(0.2)
				test.pbar.update(1)
		else:
			print('Error: Invalid promptKeyValue')
	else:
		print('Usage: python3 singleTester.py [promptKeyValue] [needTool: 0, 1] [fileName] [count: int]')
