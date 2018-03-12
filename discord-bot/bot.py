#!/usr/bin/python3
import sys
import datetime
import pprint
import argparse

import discord
from discord.ext import commands

import lib.roll_dice
import lib.doc_list
from lib.world_state import WorldState

description = '''bots'''

parser = argparse.ArgumentParser()
parser.add_argument('secrets_dir', help='directory containing client secrets')
parser.add_argument('--debug', help='debug mode (don\'t run bot)', action="store_true")
args = parser.parse_args()

if not args.debug:
  bot = commands.Bot(command_prefix=commands.when_mentioned_or('!!!'))

############
# Helpers
def say_with_mention(context, message):
  return bot.say('{} {}'.format(context.message.author.mention, message))

############
# Setup

# TODO try to make only a *single* global object, containing adventures, calendar, etc
# Any failures here should fail before startup.
world_state = WorldState()

############
# Commands

if not args.debug:
  @bot.command(pass_context=True, aliases=['date'])
  async def today(context):
    '''current (in-game) date
    
    In-game/real-world dates matched up using an adventure list from Google Docs.'''
    await say_with_mention(context, 'Today\'s date is {}.'.format(world_state.RealToInGame(datetime.date.today())))

  @bot.command(pass_context=True)
  async def roll(context, *diceStrings):
    '''Rolls dice
    
    Sample valid inputs:
    2d6
    5+1d20
    3d6 + 1d4'''
    await say_with_mention(context, 'rolled {}'.format(lib.roll_dice.rollDice(''.join(diceStrings))))

  @bot.command(pass_context=True, aliases=['finddoc'])
  async def finddocs(context, name):
    await say_with_mention(context, lib.doc_list.find_by_name(name))

  @bot.command(pass_context=True, aliases=['listdoc'])
  async def listdocs(context):
    await say_with_mention(context, lib.doc_list.list_all())

  @bot.command(pass_context=True, hidden=True)
  async def refresh_data(context):
    '''(admin-only) refresh underlying data from Google Docs.
    
    p.s. not actually admin only but maybe don't fool around with it ok?'''
    global world_state
    (success, message) = world_state.fetch_data()
    if success:
      await say_with_mention(context, '{}\n{} adventures, {} characters'.format(message, len(world_state.adventures), len(world_state.characters)))
    else:
      await say_with_mention(context, 'Error fetching data: {}'.format(message))

  @bot.command(pass_context=True, aliases=['adv'])
  async def adventures(context, max_to_print=5):
    '''show known adventures'''
    if not world_state.adventures or len(world_state.adventures) == 0:
      await say_with_mention(context, 'No adventures known.')
    else:
      num_to_print = min(max_to_print, len(world_state.adventures))
      selected_adventures = world_state.adventures[-num_to_print:]
      message='Adventures:\n{}'.format(
        '\n'.join([str(x) for x in selected_adventures]))
      await say_with_mention(context, message)

############
# Run

if not args.debug:
  with open('{}/bot-token'.format(args.secrets_dir)) as bot_token_file:
    token = bot_token_file.read().strip()
  bot.run(token)
