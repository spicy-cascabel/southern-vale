import math
import sys
import datetime
import pdb

from lib import in_game_calendar
from lib import adventure

# TODO CalendarConverter
class FullCalendar:
  def __init__(self):
    # TODO figure out how to not hardcode this - we need it to parse adventure
    # dates right now. Probably need AddAdventures to do the parsing instead of
    # the caller.
    self.real_start_date = datetime.date(2018, 3, 4)
    self.in_game_start_date = in_game_calendar.InGameDate.FromString('Twyla 14 1252')

    in_game_calendar.SetDefaultYear(self.RealToInGame([], datetime.date.today()).year)

  def RealToInGame(self, adventures, real_date):
    return (self.in_game_start_date + (real_date - self.real_start_date).days +
      sum([a.end_date - a.start_date for a in adventures if a.real_date < real_date]))

  def InGameToReal(self, adventures, in_game_date):
    return self.real_start_date + datetime.timedelta(
        in_game_date - self.in_game_start_date -
        sum([min(a.end_date, in_game_date) - a.start_date
          for a in adventures if in_game_date >= a.start_date]))
