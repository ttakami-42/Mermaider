from dotenv import load_dotenv
from json import load
from logging import config
from os import environ
from os.path import join, dirname, isfile

def loadEnv() -> None:
	try:
		dotenvPath = join(dirname(__file__), '.env')
		if not isfile(dotenvPath):
			raise FileNotFoundError(".env file not found")
		load_dotenv(dotenvPath)
	except Exception:
		raise

def getBotToken() -> str:
	try:
		loadEnv()
		DISCORD_BOT_TOKEN = environ.get("DISCORD_BOT_TOKEN")
		if DISCORD_BOT_TOKEN is None:
			raise ValueError("DISCORD_BOT_TOKEN is not set in the environment")
		return (DISCORD_BOT_TOKEN)
	except Exception:
		raise
	
def getServerId() -> int:
	try:
		loadEnv()
		DISCORD_SERVER_ID = environ.get("DISCORD_SERVER_ID")
		if DISCORD_SERVER_ID is None:
			raise ValueError("DISCORD_SERVER_ID is not set in the environment")
		return (DISCORD_SERVER_ID)
	except Exception:
		raise

def getAPIKey() -> str:
	try:
		loadEnv()
		OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
		if OPENAI_API_KEY is None:
			raise ValueError("OPENAI_API_KEY is not set in the environment")
		return (OPENAI_API_KEY)
	except Exception:
		raise

def loadMermaiderPrompt() -> dict:
	try:
		promptPath = join(dirname(__file__), '_mermaiderPrompt.json')
		with open(promptPath, 'r') as f:
			data = load(f)
		return (data)
	except Exception:
		raise

def loadMermaiderLogger() -> None:
	try:
		loggerPath = join(dirname(__file__), '_mermaiderLogger.json')
		with open(loggerPath, "r") as f:
			loggerSettings = load(f)
			config.dictConfig(loggerSettings)
	except Exception:
		raise
