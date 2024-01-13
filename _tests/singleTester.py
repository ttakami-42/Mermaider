from sys import argv, exit
import utils

# Child class for single test
class SingleTestClass(utils.TestClass):
	def __init__(self, fileName: str, filePath: str, count: int) -> None:
		super().__init__()
		text = utils.readFile(filePath)
		self.setup_progress_bar(total=count, desc=f'Testing {fileName}', unit='tests')
		self.setup_openai_vars(needInitialize=True, additionalContent=text)
		self.setup_data_class(fileName=fileName)

if __name__ == '__main__':
	args = argv
	filePath = utils.getFilePath(args[1], 'data/input/code')
	if len(args) == 3 and filePath and args[2].isdigit():
		fileName, count = args[1], int(args[2])
		test = SingleTestClass(fileName=fileName, filePath=filePath, count=count)
		test.pbar.update(0)
		for i in range(0, count):
			test.logger.info('Processing step %s' % (i + 1))
			try:
				test.tester(row=test.data.empty_row + i)
			except Exception:
				exit(1)
			test.pbar.update()
	else:
		print('Usage: python3 singleTester.py [file_name] [count]')
