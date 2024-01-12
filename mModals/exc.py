from logging import getLogger
from traceback import extract_tb
from os.path import basename

class ModalException(Exception):                        # For discord commands error
	def __init__(self, error: Exception, message: str) -> None:
		self.error   = error
		self.message = message
		tb = extract_tb(error.__traceback__)[-1]        # Get the last traceback
		self.fileName = basename(tb.filename)
		self.funcName = tb.name
		self.lineNo   = tb.lineno
		self.logger = getLogger("mermaiderCommand")     # Get logger

	def __str__(self) -> str:
		self.logger.error(f'{str(self.error)} [{self.fileName}] [{self.funcName}] [{self.lineNo}]')
		return (f'Sorry, "{self.message}" error occurred.')
