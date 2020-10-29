from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord import Embed , File
from datetime import datetime

PREFIX = "+"
OWNER_IDS = [381031540899053568]


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		
		self.scheduler=AsyncIOScheduler()

		super().__init__(command_prefix=PREFIX,owner_ids=OWNER_IDS)

	def run(self,version):
		self.VERSION=version

		with open("./lib/bot/token.0","r", encoding="utf-8")as tf:
			self.TOKEN = tf.read()

		print("running bot...")
		super().run(self.TOKEN ,reconnect=True)


	async def on_connect(self):
			print("bot connected")

	async def on_disconnect(self):
			print("bot dissconnected")

	async def on_ready(self):
			if not self.ready:
				self.ready = True
				print("bot ready")
				channel = self.get_channel(771316587935563808)
				await channel.send("Hi Guys, Ganz is my KING!!!")
				embed = Embed(title="Im here", description="Bot is ready",colour=0xFF0000, timestamp=datetime.utcnow())
				embed.set_author(name="Ganz",icon_url="https://wallpaperaccess.com/full/1490040.jpg")
				fields=[("Vladyslav Petriuk","Author",True),("w60083","Index",True)]
				for name ,value,inline in fields:
					embed.add_field(name=name,value=value,inline=inline)
				await channel.send(embed=embed)
			else:
				print("bot reconnected")

	async def on_message(self,message):
			pass

bot=Bot()