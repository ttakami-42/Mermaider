from discord import app_commands, Object
from discord.ext import commands
from discord.interactions import Interaction
from discord.app_commands import Choice
from logging import getLogger
from mModals import MermaiderModal
from mSettings import getServerId

class GenCog(commands.Cog):

	def __init__(self, bot: commands.Bot) -> None:
		super().__init__()
		self.bot = bot
		self.logger = getLogger("mermaiderSystem")

	@commands.Cog.listener()
	async def on_ready(self) -> None:
		try:
			ServerId = getServerId()
			self.bot.tree.add_command(self.gen, guild = Object(ServerId))
			await self.bot.tree.sync(guild = Object(ServerId))
		except Exception as e:
			self.logger.error(f'{type(e)}: {e}')
			raise
		self.logger.info("[Cogs] genCog is ready.")

	@app_commands.command(
		name        = "gen",
		description = "generate diagram which visualizes your C code (Powered by GPT-3.5)"
	)
	@app_commands.describe(
		darkmode = "change bgcolor to black"
	)
	@app_commands.choices(
		darkmode = [
			Choice(name = "ON",  value = 1),
			Choice(name = "OFF", value = 0)
		]
	)
	async def gen(self, ctx: Interaction, darkmode: Choice[int] = None) -> None:
		if darkmode == None:
			darkmode = Choice(name = "OFF", value = 0)
		modal = MermaiderModal(
			model = "gpt-3.5-turbo-1106",
			promptKeyValue = "genMessages",
			needTool = True,
			ctx = ctx,
			language = "cpp",
			darkmode = darkmode.value
		)
		try:
			await ctx.response.send_modal(modal)
			if await modal.wait():
				raise TimeoutError("/gen request timed out.")
		except Exception as e:
			self.logger.error(f'{type(e)}: {e}')
	
async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(GenCog(bot))
