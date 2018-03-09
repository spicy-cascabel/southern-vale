#!/usr/bin/python3
import discord
from discord.ext import commands
import sys

import roll_dice
import doc_list

description = '''bots'''

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!!!'))

def say_with_mention(context, message):
  return bot.say('{} {}'.format(context.message.author.mention, message))

@bot.command(pass_context=True, aliases=['date'])
async def today():
  '''Reports the current (in-game) date'''
  await say_with_mention(context, 'Today\'s date is... I don\'t know!')

@bot.command(pass_context=True)
async def roll(context, *diceStrings):
  '''rolls dice (given input like 2d6 or 5+1d20 or 3d6+1d4)'''
  await say_with_mention(context, 'rolled {}'.format(roll_dice.rollDice(''.join(diceStrings))))

@bot.command(pass_context=True)
async def finddoc(context, name):
  await say_with_mention(context, doc_list.find_by_name(name))


# Run
if len(sys.argv) != 2:
  print('usage: {} <token>'.format(sys.argv[0]))
  sys.exit(1)

token = sys.argv[1]

bot.run(token)
