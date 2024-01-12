from sys import argv, exit
import utils

# Child class for multiple tests
class MultiTestClass(utils.TestClass):
	def __init__(self, fileName: str, filePath: str, count: int) -> None:
		super().__init__()
		self.jsonInput = utils.loadJSONFile(filePath)
		jsonInputKeys = list(self.jsonInput.keys())
		self.setup_progress_bar(total=len(jsonInputKeys) * count, desc=f'Testing {fileName}', unit='tests')
		self.setup_openai_vars(needInitialize=True, additionalContent=self.jsonInput[jsonInputKeys[0]])
		self.setup_data_class(fileName=fileName, title1='filename', title2='input')

if __name__ == '__main__':
	args = argv
	filePath = utils.getFilePath(args[1], 'data/input')
	if len(args) == 3 and filePath and args[2].isdigit():
		fileName, count = args[1], int(args[2])
		test = MultiTestClass(fileName=fileName, filePath=filePath, count=count)
		total = 0
		test.pbar.update(0)
		for keyValueofInput, text in test.jsonInput.items():
			if total:
				test.setup_openai_vars(needDelete=True, additionalContent=text)
			for i in range(0, count):
				stepNumber = i + total
				test.logger.info(f'Processing {keyValueofInput}, step {stepNumber + 1}')
				try:
					test.tester(row=test.data.empty_row + stepNumber, text=text, keyValueofInput=keyValueofInput)
				except Exception:
					exit(1)
				test.pbar.update()
			total += count
	else:
		print('Usage: python3 multiTester.py [file_name] [count]')
