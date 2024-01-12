from discord.ext import commands
from discord import Intents
from logging import getLogger
from mSettings import loadMermaiderLogger, getBotToken

INITAL_EXTENSIONS = [
	"mCogs.gen",
	"mCogs.fgen"
]

class Mermaider(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix = "!", intents = Intents.all())

	async def setup_hook(self):
		try:
			for extension in INITAL_EXTENSIONS:
				await self.load_extension(extension)
		except Exception:
			raise

def main() -> None:
	try:
		loadMermaiderLogger()
	except Exception:
		raise
	logger = getLogger("mermaiderSystem")
	try:
		bot_token = getBotToken()
		Mermaider().run(bot_token, log_handler = logger.handlers[1])
	except Exception as e:
		logger.error(f'{type(e)}: {e}')
		raise

if __name__ == '__main__':
	main()
