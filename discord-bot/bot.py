#!/usr/bin/python3
import discord
from discord.ext import commands
import sys

import roll_dice
import doc_list
import calendar
import datetime

description = '''bots'''

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!!!'))

cal = calendar.FullCalendar()

def say_with_mention(context, message):
  return bot.say('{} {}'.format(context.message.author.mention, message))

@bot.command(pass_context=True, aliases=['date'])
async def today(context):
  '''Reports the current (in-game) date'''
  await say_with_mention(context, 'Today\'s date is {}.'.format(cal.RealToInGame(datetime.date.today())))

@bot.command(pass_context=True)
async def roll(context, *diceStrings):
  '''rolls dice (given input like 2d6 or 5+1d20 or 3d6+1d4)'''
  await say_with_mention(context, 'rolled {}'.format(roll_dice.rollDice(''.join(diceStrings))))

@bot.command(pass_context=True)
async def finddoc(context, name):
  await say_with_mention(context, doc_list.find_by_name(name))

# desired commands:
#
#   adventure (adv)
#     add <summary> <real-date> <in-game end date> <characters> (start date assumed to match; return id)
#     edit <id> <normal adventure args?>
#   ....or add->id; edit summary <...>; edit real-date <...>; ...
#     list (return ids)
#     remove <id>
#
#   character (char)
#     list
#     add
#     edit
#       level
#       set-nicknames
#     downtime spend <num days> <note>
#     downtime report

# Run
if len(sys.argv) != 2:
  print('usage: {} <token>'.format(sys.argv[0]))
  sys.exit(1)

token = sys.argv[1]

bot.run(token)
