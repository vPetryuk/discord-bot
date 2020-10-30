from asyncio import sleep
from glob import glob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord import Embed , File
from datetime import datetime
from discord.ext.commands import CommandNotFound
from apscheduler.triggers.cron import CronTrigger

from ..db import db
PREFIX = "+"
OWNER_IDS = [381031540899053568]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self,cog,False)

	def ready_up(self,cog):
		setattr(self,cog,True)
		print(f"{cog} cog ready")

	def all_ready(self):
		return all([getattr(self,cog) for cog in COGS])

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.cogs_ready=Ready()
		self.scheduler=AsyncIOScheduler()
		db.autosave(self.scheduler)
		super().__init__(command_prefix=PREFIX,owner_ids=OWNER_IDS)

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f"{cog} cog loaded")
		print("setup comlete")
		

	def run(self,version):
		self.VERSION=version
		self.setup()

		with open("./lib/bot/token.0","r", encoding="utf-8")as tf:
			self.TOKEN = tf.read()

		print("running bot...")
		super().run(self.TOKEN ,reconnect=True)


	async def on_connect(self):
			print("bot connected")

	async def on_disconnect(self):
			print("bot dissconnected")

	async def on_error(self,err,*args,**kwargs):
    		if err == "on_command_error":
    			await args[0].send("something went wrong")

    		else:	
    			channel = self.get_channel(771316587935563808)
    			await channel.send("ERROR")
    		raise

	async def on_command_error(self,ctx,exc):

		if isinstance(exc,CommandNotFound):
			pass

		else:
			raise exc.original
			

	

	async def on_ready(self):
			if not self.ready:
				self.ready = True
				print("bot ready")
				self.stdout = self.get_channel(771316587935563808)
				channel = self.get_channel(771316587935563808)
				await channel.send("Hi Guys, Ganz is my KING!!!2")
				embed = Embed(title="Im here", description="Bot is ready",colour=0xFF0000, timestamp=datetime.utcnow())
				embed.set_author(name="Ganz",icon_url="https://wallpaperaccess.com/full/1490040.jpg")
				fields=[("Vladyslav Petriuk","Author",True),("w60083","Index",True)]
				for name ,value,inline in fields:
					embed.add_field(name=name,value=value,inline=inline)
				await channel.send(embed=embed)
				await channel.send(file=File("./data/images/smoke1.jpg"))
				
				while not self.cogs_ready.all_ready():
					await sleep(0.5)
				self.ready = True
			else:
				print("bot reconnected")

	async def on_message(self,message):
		if not message.author.bot:
			await self.stdout.send("we are on line 94")
			await self.process_commands(message)
		 

bot=Bot()