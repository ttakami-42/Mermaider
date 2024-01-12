from discord import TextStyle, Embed, File
from discord.ui import Modal, TextInput
from discord.interactions import Interaction
from .exc import ModalException
from .api import callGPT
from .img import isImageURL, getImageURL

class MermaiderModal(Modal):

	def __init__(self, model: str, promptKeyValue: str, needTool: bool, ctx: Interaction, language: str, darkmode: int) -> None:
		super().__init__(title = "", timeout = 180)
		self.model = model
		self.promptKeyValue = promptKeyValue
		self.needTool = needTool
		self.ctx = ctx
		self.lang = language
		self.dark = darkmode
		self.text = TextInput(
			custom_id   = "",
			style       = TextStyle.long,
			label       = "Code",
			required    = True,
			max_length  = 4000,
			placeholder = "Give me your source code.",
		)
		self.add_item(self.text)


	async def on_submit(self, interaction: Interaction) -> None:
		await interaction.response.defer(ephemeral = False, thinking = True)
		response = callGPT(model = self.model, promptKeyValue = self.promptKeyValue, needTool = self.needTool, text = self.text.value)
		if response['isSuccess']:
			image_url = getImageURL(response['content'], self.dark)
			if isImageURL(image_url):
				embed = Embed(
					title = "Generation Succeeded!",
					color = 0x00ff5b,
					description = f"```{self.lang}\n{self.text.value}\n```"
				)
				file = File("_icons/check_circle_line.png", filename = "check_circle_line.png")
				embed.set_thumbnail(url = "attachment://check_circle_line.png")
				embed.add_field(name = "", value = "- _Mermaid code (for below image) written with ChatGPT._", inline = False)
				embed.add_field(name = "", value = f"- _This image spent [{response['completion']}] tokens._", inline = False)
				embed.set_image(url = image_url)
			else:
				embed = Embed(
					title = "Generation Failed!",
					color = 0xffe53b,
					description = f"_ChatGPT might generate wrong mermaid code. Please try again!_"
				)
				file = File("_icons/refresh_2_line.png", filename = "refresh_2.png")
				embed.set_thumbnail(url = "attachment://refresh_2.png")
		else:
			embed = Embed(
				title = "Don't Do That!",
				color = 0xffe53b,
				description = response['content']
			)
			file = File("_icons/warning_line.png", filename = "warning_line.png")
			embed.set_thumbnail(url = "attachment://warning_line.png")
		await interaction.followup.send(file = file, embed = embed)
		self.stop()


	async def on_error(self, interaction: Interaction, error: Exception) -> None:
		desc = error if type(error) == ModalException else ModalException(error, "Modal")
		embed = Embed(title = "Oops! Something Went Wrong!", color = 0xff2525, description = desc)
		try:
			file = File("_icons/close_circle_line.png", filename = "close_circle_line.png")
			embed.set_thumbnail(url = "attachment://close_circle_line.png")
			await interaction.followup.send(file = file, embed = embed)
		except Exception as e:
			raise ModalException(e, "Error Handling")
		finally:
			self.stop()


	async def on_timeout(self) -> None:
		embed = Embed(title = "Time Out!", color = 0xff2525, description = "You took too long to respond.")
		try:
			file = File("_icons/time_line.png", filename = "time_line.png")
			embed.set_thumbnail(url = "attachment://time_line.png")
			await self.ctx.followup.send(ephemeral = True, file = file, embed = embed)
		except Exception as e:
			raise ModalException(e, "Timeout Handling")
		finally:
			self.stop()
