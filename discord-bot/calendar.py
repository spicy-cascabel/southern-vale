import math
import sys
import datetime
import in_game_calendar
import adventure

class FullCalendar:
  def __init__(self):
    self.real_start_date = datetime.date(2018, 3, 4)
    self.in_game_start_date = in_game_calendar.InGameDate.FromString('Twyla 14 1252')
    self.adventures = [
        adventure.Adventure('Eastern coast lighthouse', [],
          in_game_calendar.InGameDate.FromString('Twyla 14 1252'),
          in_game_calendar.InGameDate.FromString('Twyla 18 1252'),
          datetime.date(2018, 3, 4)),
        adventure.Adventure('Downtime catchup', [],
          in_game_calendar.InGameDate.FromString('Twyla 19 1252'),
          in_game_calendar.InGameDate.FromString('Twyla 25 1252'),
          datetime.date(2018, 3, 5))
        ]

    for a in self.adventures:
      if (self.InGameToReal(a.start_date) != a.real_date or
          self.InGameToReal(a.end_date) != a.real_date or
          self.RealToInGame(a.real_date) != a.start_date):
        sys.exit(1)

    in_game_calendar.SetDefaultYear(self.RealToInGame(datetime.date.today()).year)


  def RealToInGame(self, real_date):
    return (self.in_game_start_date + (real_date - self.real_start_date).days +
      sum([a.end_date - a.start_date for a in self.adventures if a.real_date < real_date]))

  def InGameToReal(self, in_game_date):
    return self.real_start_date + datetime.timedelta(
        in_game_date - self.in_game_start_date -
        sum([min(a.end_date, in_game_date) - a.start_date
          for a in self.adventures if in_game_date >= a.start_date]))
