#!/usr/bin/python

from http import server
from time import sleep
from xmlrpc.client import SERVER_ERROR
from discord.ext.commands import Context
import discord
from discord import Message
from discord import Member
from discord.ext import commands
from discord import Role
from datetime import date

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

SERVER_BIRTH_DATE = date(year=2017, month=12, day=17)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def what_is_theme(ctx: Context):
  await ctx.send(f"Hello {ctx.author}! The theme is sex in the city..")

@bot.command()
async def update_roles(ctx):  
  days_since_server_birth = abs((SERVER_BIRTH_DATE - date.today()).days)
  print(f"Server has been around for {days_since_server_birth}")
  # Both lists are ordered
  year_multiplier_list = [4.43, 3.25, 2.00, 1.00, 0.07]
  role_ids = [990808541960994866, 990808587368542239, 990808607396347904, 990808624458784789, 990808641546358794]
  
  # Have to be under this number to achieve the tier, ever increasing..
  max_days_after_birth = list()
  for multiplier in year_multiplier_list:
    max_days_after_birth.append(days_since_server_birth - (365 * multiplier))
    
  for guild in bot.guilds:
    for member in guild.members:
      joined_date: date = member.joined_at.date()
      joined_days_after_birth = (joined_date - SERVER_BIRTH_DATE).days
      for tier_max_days, role_id in zip(max_days_after_birth, role_ids):
        if joined_days_after_birth < tier_max_days:
          # Remove top role..
          if member.top_role.id in role_ids:
            print(f"Removing top role: {member.top_role} from {member.name}")
            await member.remove_roles(member.top_role)
          print(f"Adding {tier_max_days} to {member.name} joined {joined_days_after_birth} after server creation")
          await member.add_roles(discord.utils.get(ctx.guild.roles, id=role_id))
          break
      sleep(0.25)
  await ctx.send("Completed..")

      

bot.run('')