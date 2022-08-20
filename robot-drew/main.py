#!/usr/bin/python

from time import sleep
from discord.ext.commands import Context
import discord
from discord import Message, Member, Guild, ChannelType, TextChannel, Role
from discord.ext import commands

from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)
THE_RICKS_GUILD_NAME = 'The Ricks'
SERVER_BIRTH_DATE = date(year=2017, month=12, day=17)

def get_the_ricks_guild() -> Guild:
  for guild in bot.guilds:
    if guild.name == THE_RICKS_GUILD_NAME:
      return guild

def get_robot_drew_channel() -> TextChannel:
  ricks_discord = get_the_ricks_guild()
  for channel in ricks_discord.channels:
    if channel.name == 'robot-drew':
      return channel

@bot.command()
async def what_is_theme(ctx: Context):
  await ctx.send(f"Hello {ctx.author}! The theme is sex in the city..")

async def update_roles(ricks_guild: Guild, robot_drew_channel: TextChannel):  
  days_since_server_birth = abs((SERVER_BIRTH_DATE - date.today()).days)
  print(f"Server has been around for {days_since_server_birth}")
  # Both lists are ordered
  year_multiplier_list = [4.43, 3.25, 2.00, 1.00, 0.07]
  role_ids = [990808541960994866, 990808587368542239, 990808607396347904, 990808624458784789, 990808641546358794]
  await robot_drew_channel.send("Starting to update everyones role...")
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
          await member.add_roles(discord.utils.get(ricks_guild.roles, id=role_id))
          break
      sleep(0.03)
  await robot_drew_channel.send("Completed..")


async def update_roles_timer():
  the_ricks_discord = get_the_ricks_guild()
  robot_drew_channel = get_robot_drew_channel()
  print("updating roles...")
  await update_roles(the_ricks_discord, robot_drew_channel)

# Main Function..
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print("Starting update role..")
    roles_scheduler = AsyncIOScheduler()
    roles_scheduler.add_job(func=update_roles_timer, trigger='interval', hours=6)
    roles_scheduler.start()

f = open("bot-key.txt", "r")
bot_key : str = (f.read())
print(f"Starting bot with key {bot_key}")
bot.run(bot_key)