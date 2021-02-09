from asyncio import sleep
from glob import glob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord import Embed , File
from datetime import datetime
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown)
from apscheduler.triggers.cron import CronTrigger
from discord.errors import HTTPException, Forbidden


PREFIX = "+"
OWNER_IDS = [381031540899053568]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)
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

	async def on_command_error(self, ctx, exc):
		if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send("One or more required arguments are missing.")

		elif isinstance(exc, CommandOnCooldown):
			await ctx.send(f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Try again in {exc.retry_after:,.2f} secs.")

		elif hasattr(exc, "original"):
			# if isinstance(exc.original, HTTPException):
			# 	await ctx.send("Unable to send message.")

			if isinstance(exc.original, Forbidden):
				await ctx.send("I do not have permission to do that.")

			else:
				raise exc.original

		else:
			raise exc
			

	

	async def on_ready(self):
			if not self.ready:
				self.ready = True
				print("bot ready")
				self.stdout = self.get_channel(771316587935563808)
				channel = self.get_channel(771316587935563808)
				
				embed = Embed(title="Im here", description="Bot is online",colour=0xFF0000, timestamp=datetime.utcnow())
				#embed.set_author(name="Ganz" icon_url="https://wallpaperaccess.com/full/1490040.jpg")
				fields=[("Vladyslav Petriuk , Alona Kovtun , Vladyslava Tokar","Authors",True),("     w60083                     w60065                 w60092","Indexs",False),
				("Commands","----------------------------------------------------------------------------------",False),
				("Hello","Say +hi",True),("Echo","+echo message",True),("Punch","+punch member reason",True),("Facts", "+fact animal", True),
				("Meme", "+meme", True),("Dice", "+dice number_of_numbers d  ", True),("Flip", "+flip", True), ("8ball", "+8ball question", True),

				("Clear messages", "+clear number_of_messages_to_delete ", True), ("Help", "+help", True), ]

				

				for name ,value,inline in fields:
					embed.add_field(name=name,value=value,inline=inline)
				embed.set_author(name="Bot", icon_url="https://i.pinimg.com/originals/9c/8c/21/9c8c21100af2a2834723c50903e86bda.jpg")	
				await channel.send(embed=embed)
				
				
				while not self.cogs_ready.all_ready():
					await sleep(0.5)
				self.ready = True
			else:
				print("bot reconnected")

	async def on_message(self,message):
		if not message.author.bot:
			await self.process_commands(message)
		 

bot=Bot()