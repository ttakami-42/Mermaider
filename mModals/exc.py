from logging import getLogger
from traceback import extract_tb
from os import path

class ModalException(Exception):                        # for discord commands error
	def __init__(self, error: Exception, message: str):
		self.error   = error
		self.message = message
		tb = extract_tb(error.__traceback__)[-1]        # get the last traceback
		self.fileName = path.basename(tb.filename)
		self.funcName = tb.name
		self.lineNo   = tb.lineno
		self.logger = getLogger("mermaiderCmd")         # get logger

	def __str__(self):
		self.logger.error(f'{str(self.error)} [{self.fileName}] [{self.funcName}] [{self.lineNo}]')
		return (f'Sorry, "{self.message}" error occurred.')