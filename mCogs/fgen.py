from discord import app_commands, Object
from discord.ext import commands
from discord.interactions import Interaction
from discord.app_commands import Choice
from logging import getLogger
from mModals import MermaiderModal
from mSettings import getServerId

class FGenCog(commands.Cog):

	def __init__(self, bot: commands.Bot) -> None:
		super().__init__()
		self.bot = bot
		self.logger = getLogger("mermaiderSystem")

	@commands.Cog.listener()
	async def on_ready(self) -> None:
		try:
			ServerId = getServerId()
			self.bot.tree.add_command(self.fgen, guild = Object(ServerId))
			await self.bot.tree.sync(guild = Object(ServerId))
		except Exception as e:
			self.logger.error(f'{type(e)}: {e}')
			raise
		self.logger.info("[Cogs] fgenCog is ready.")

	@app_commands.command(
		name        = "fgen",
		description = "generate diagram which visualizes your code (Powered by GPT-4)"
	)
	@app_commands.describe(
		language = "choose language of your code",
		darkmode = "change bgcolor to black"
	)
	@app_commands.choices(
		language = [ # These choices change syntax highlighting only.
			Choice(name = "C/C++",      value = "cpp"),
			Choice(name = "Java",       value = "java"),
			Choice(name = "JavaScript", value = "js"),
			Choice(name = "Python",     value = "python"),
			Choice(name = "Others",     value = "")
		],
		darkmode = [
			Choice(name = "ON",  value = 1),
			Choice(name = "OFF", value = 0)
		]
	)
	async def fgen(self, ctx: Interaction, language: Choice[str], darkmode: Choice[int] = None) -> None:
		if darkmode == None:
			darkmode = Choice(name = "OFF", value = 0)
		modal = MermaiderModal(
			model = "gpt-4-1106-preview",
			promptKeyValue = "fgenMessages",
			needTool = False,
			ctx = ctx,
			language = language.value,
			darkmode = darkmode.value
		)
		try:
			await ctx.response.send_modal(modal)
			if await modal.wait():
				raise TimeoutError("/fgen request timed out.")
		except Exception as e:
			self.logger.error(f'{type(e)}: {e}')

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(FGenCog(bot))
