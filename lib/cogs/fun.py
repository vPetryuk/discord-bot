from random import choice, randint
from typing import Optional
import random
from aiohttp import request
from discord import Member, Embed, File
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown
from discord.ext.commands import command, has_permissions, bot_has_permissions



class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="hello", brief="Hello - Say hello",
		aliases=["hi","Hello", "Hi", "Hey","Siema","czesc","Guten Tag","привет","привіт"])
	async def say_hello(self, ctx):
		await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya','Privet','Siema','Cześć','Guten Tag','Whats cooking good looking!','Siemanko','You are so awesome today!'))} {ctx.author.mention}!")

	# @command(name="dice", aliases=["roll"])
	# @cooldown(1, 60, BucketType.user)
	# async def roll_dice(self, ctx, die_string: str):
	# 	goal = random.randint(0, 100)
	# 	ctx.send(f"{goal} goal")
	# 	ctx.send("You need to choose right number from 0 to 100")
	# 	while True:
	# 		number = (int(die_string))
	# 		if number < goal:
	# 			ctx.send("Your number is smaller than goal")
	# 			continue
	# 		if number > goal:
	# 			ctx.send("Your number is too big")
	# 			continue
	# 		if number == goal:
	# 			print("You are winner!!!")
	# 			break
	# 		else:
	# 			break

	@command(name="dice", brief="Dice - output of this command is some number of random numbers in some range", aliases=["roll"])
	@cooldown(1, 5, BucketType.user)
	async def rool_dice(self, ctx, die_string: str):
		dice, value = (int(term) for term in die_string.split("d"))

		if dice <= 25:
			rolls = [randint(1, value) for i in range(dice)]
			await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
		else:
			await ctx.send("I can't roll that many dice. Please try a lower number.")
			
	@command(name="clear", brief="Clear - delete messages", aliases=["purge"])
	@bot_has_permissions(manage_messages=True)
	@has_permissions(manage_messages=True)
	async def clear_messages(self, ctx, limit: Optional[int] = 1):
		if 0 < limit <= 100:
			with ctx.channel.typing():
				await ctx.message.delete()
				deleted = await ctx.channel.purge(limit=limit)
				await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)
		else:
			await ctx.send("The limit provided is not within acceptable bounds.")
		

	@command(name="slap", brief="Slap - write some  to channel anonimous", aliases=["hit","punch","kick"])
	async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
		await ctx.message.delete()
		await ctx.send(f"{ctx.author.display_name} punch {member.mention}{reason}!")

	@slap_member.error
	async def slap_member_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.send("I can't find that member.")

	@command(name="echo", brief="Echo - write some message to channel anonimous", aliases=["say"])
	@cooldown(1, 15, BucketType.guild)
	async def echo_message(self, ctx, *, message):
		await ctx.message.delete()
		await ctx.send(message)

	@command(name="fact", brief="Fact - shows fact about animals",)
	@cooldown(3, 60, BucketType.guild)
	async def animal_fact(self, ctx, animal: str):
		if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
			fact_url = f"https://some-random-api.ml/facts/{animal}"
			image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]

				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()

					embed = Embed(title=f"{animal.title()} fact",
								  description=data["fact"],
								  colour=ctx.author.colour)
					if image_link is not None:
						embed.set_image(url=image_link)
					await ctx.send(embed=embed)

				else:
					await ctx.send(f"API returned a {response.status} status.")

		else:
			await ctx.send("No facts are available for that animal.")

	@command(name="meme", brief="Meme - show random memes",)
	@cooldown(3, 60, BucketType.guild)
	async def meme(self, ctx):
			meme_url = f"https://some-random-api.ml/meme"
			async with request("GET", meme_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					meme_data = data["image"]
					embed = Embed(title="Meme",
								  colour=ctx.author.colour)
					if meme_url is not None:
						embed.set_image(url=meme_data)
					await ctx.send(embed=embed)

				else:
					await ctx.send(f"API returned a {response.status} status.")


	@command(name='flip', brief="Flip - shows random generated YES or NO",aliases=['Flip'])
	async def flip(self,ctx):
		headTails = ['YES','NO']
		await ctx.send(random.choice(headTails))


	@command(name='8ball', brief="8ball - give the answer", aliases=['8Ball'])
	async def ball(self,ctx, *args):
		await ctx.send(file=File("./data/images/ball.png"))
		mylist = ""
		for x in args:
			mylist += " " + x

		options = ['As I see it, yes.','Ask again later.','Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
					'Don \'t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.',
					'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.',
					' Yes.', 'Yes – definitely.', ' You may rely on it.']

		await ctx.send(f'Question: "{mylist}" \n Answer: {random.choice(options)}')


		
	@Cog.listener()
	async def on_ready(self):
		print("fun cog ready")
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("fun")


def setup(bot):
	bot.add_cog(Fun(bot))
