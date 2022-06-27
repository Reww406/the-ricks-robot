#!/usr/bin/python

import discord
from discord import Message
from discord import Member
from discord.ext import commands
import collections


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def list_members_length(ctx):
  out_put: str = ""
   
  members_and_join: dict = dict()
  for guild in bot.guilds:
    for member in guild.members:
      member: Member
      members_and_join[member.name] = member.joined_at
  od = collections.OrderedDict(sorted(members_and_join.items(), key=lambda item: item[1]))
  await ctx.send("Hello listing people...")
  for member, join_date in od.items():
    if member is not None:
      out_put = out_put + " - ".join([member, str(join_date), "\n"])
      if(len(out_put) > 1800):
        await ctx.send(out_put)
        out_put = ""
  if(len(out_put) > 0):
    await ctx.send(out_put)

# @client.event
# async def on_message(message: Message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

#     if message.content.startswith('$how_long?'):
#       for guild in client.guilds:
#         for member in guild.members:
#           print(member.name)


bot.run('')