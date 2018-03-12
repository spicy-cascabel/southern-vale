import math
import sys
import datetime
import pdb

from lib import in_game_calendar
from lib import adventure

class FullCalendar:
  def __init__(self, adventures):
    # TODO figure out how to not hardcode this - we need it to parse adventure
    # dates right now. Probably need AddAdventures to do the parsing instead of
    # the caller.
    self.real_start_date = datetime.date(2018, 3, 4)
    self.in_game_start_date = in_game_calendar.InGameDate.FromString('Twyla 14 1252')
    self.adventures = []
    self.AddAdventures(adventures)
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

    in_game_calendar.SetDefaultYear(self.RealToInGame(datetime.date.today()).year)

  def AddAdventures(self, adventures):
    if len(adventures) > 0:
      self.real_start_date = adventures[0].real_date
      prev_adventures = self.adventures
      self.adventures = adventures
      # TODO redundant code
      for a in self.adventures:
        if self.RealToInGame(a.real_date) != a.start_date:
          self.adventures = prev_adventures
          return (False, 'in-game start date is {}, but real date {} should be {} in-game'.format(
            a.start_date, a.real_date, self.RealToInGame(a.real_date)))
        if self.InGameToReal(a.start_date) != a.real_date:
          self.adventures = prev_adventures
          return (False, 'real date is {}, but in-game start date {} should be {}'.format(
            a.real_date, a.start_date, self.InGameToReal(a.start_date)))
        if self.InGameToReal(a.end_date) != a.real_date:
          self.adventures = prev_adventures
          return (False, 'real date is {}, but in-game end date {} should be {}'.format(
            a.real_date, a.end_date, self.InGameToReal(a.end_date)))
      self.adventures = adventures
    return (True, 'success')


  def RealToInGame(self, real_date):
    return (self.in_game_start_date + (real_date - self.real_start_date).days +
      sum([a.end_date - a.start_date for a in self.adventures if a.real_date < real_date]))

  def InGameToReal(self, in_game_date):
    return self.real_start_date + datetime.timedelta(
        in_game_date - self.in_game_start_date -
        sum([min(a.end_date, in_game_date) - a.start_date
          for a in self.adventures if in_game_date >= a.start_date]))
