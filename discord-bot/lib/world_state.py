import datetime
import pdb
import sys
import re

import lib.adventure
import lib.character
import lib.google_sheets_import

from lib import calendar_converter
from lib import in_game_calendar


   # [
   #     adventure.Adventure('Eastern coast lighthouse',
   #       in_game_calendar.InGameDate.FromString('Twyla 14 1252'),
   #       in_game_calendar.InGameDate.FromString('Twyla 18 1252'),
   #       datetime.date(2018, 3, 4), []),
   #     adventure.Adventure('Downtime catchup',
   #       in_game_calendar.InGameDate.FromString('Twyla 19 1252'),
   #       in_game_calendar.InGameDate.FromString('Twyla 25 1252'),
   #       datetime.date(2018, 3, 5), [])
   #     ]

class WorldState:
  def __init__(self):
    self.adventures = []
    self.character_list = lib.character.CharacterList()

    # These should be overwritten by adventures, but we might as well have a sane default.
    self.real_start_date = datetime.date(2018, 3, 4)
    self.in_game_start_date = in_game_calendar.InGameDate.FromString('Twyla 14 1252')

    (success, message) = self.fetch_data()
    if not success:
      print('Error fetching data during WorldState initialization: ' + message)
      sys.exit(1)

  def fetch_data(self):
    (success, message, fetched_data) = lib.google_sheets_import.fetch_data()
    if not success:
      return (False, message)

    if 'characters' not in fetched_data:
      return (False, 'No adventures data in fetched data.')
    (success, char_message) = self._add_raw_characters(fetched_data['characters'])
    if not success:
      return char_message

    if 'adventures' not in fetched_data:
      return (False, 'No adventures data in fetched data.')
    (success, adv_message) = self._add_raw_adventures(fetched_data['adventures'])
    if not success:
      return (False, adv_message)

    return (success, adv_message)

  def RealToInGame(self, real_date):
    return calendar_converter.RealToInGame(self.in_game_start_date,
        self.real_start_date, self.adventures, real_date)

  def InGameToReal(self, in_game):
    return calendar_converter.InGameToReal(self.in_game_start_date,
        self.real_start_date, self.adventures, in_game)

  def GetDowntime(self, character_name):
    char = self.character_list.find_by_name(character_name)
    if not char:
      return 'character name not found: "{}"'.format(character_name)
    downtime_days = (
        (self.RealToInGame(datetime.date.today()) - self.in_game_start_date) -
        sum([adv.end_date - adv.start_date + 1 for adv in self.adventures if char.name in adv.party_names]))
    return 'total downtime days: {}'.format(downtime_days)


  #######################
  # Private
  def _add_raw_adventures(self, raw_adventures):
    if len(raw_adventures) > 0:
      new_adventures = []
      for raw_adv in raw_adventures:
        party_names = []
        if raw_adv[4]:
          party_names = re.split(', *', raw_adv[4])

        full_party_names = []
        for name in party_names:
          char = self.character_list.find_by_name(name)
          if not char:
            return (False, 'character name not found: "{}"'.format(name))
          full_party_names.append(char.name)

        adv = lib.adventure.Adventure(
            name=raw_adv[0],
            start_date=in_game_calendar.InGameDate.FromString(raw_adv[1]),
            end_date=in_game_calendar.InGameDate.FromString(raw_adv[2]),
            real_date=datetime.datetime.strptime(raw_adv[3], '%Y-%m-%d').date(),
            party_names=full_party_names)
        new_adventures.append(adv)

        new_real_start_date = new_adventures[0].real_date
        new_in_game_start_date = new_adventures[0].start_date

        # Validate
        in_game_from_real = calendar_converter.RealToInGame(new_in_game_start_date,
            new_real_start_date, new_adventures, adv.real_date)
        if in_game_from_real != adv.start_date:
          return (False, 'in-game start date is {}, but real date {} should be {} in-game'.format(
            adv.start_date, adv.real_date, in_game_from_real))
        start_real = calendar_converter.InGameToReal(new_in_game_start_date,
            new_real_start_date, new_adventures, adv.start_date)
        if start_real != adv.real_date:
          return (False, 'real date is {}, but in-game start date {} should be {}'.format(
            adv.real_date, adv.start_date, start_real))
        end_real = calendar_converter.InGameToReal(new_in_game_start_date,
            new_real_start_date, new_adventures, adv.end_date)
        if end_real != adv.real_date:
          return (False, 'real date is {}, but in-game end date {} should be {}'.format(
            adv.real_date, adv.end_date, end_real))

      self.adventures = new_adventures
      self.in_game_start_date = new_in_game_start_date
      self.real_start_date = new_real_start_date
      in_game_calendar.SetDefaultYear(self.RealToInGame(datetime.date.today()).year)
    return (True, 'success')

  def _add_raw_characters(self, raw_characters):
    new_characters = []
    for raw_c in raw_characters:
      new_characters.append(lib.character.Character(
        name=raw_c[0],
        race_class=raw_c[2],
        nicknames=re.split(', *', raw_c[1]),
        discord_id=raw_c[3]))
    self.character_list.characters = new_characters
    return (True, None)
