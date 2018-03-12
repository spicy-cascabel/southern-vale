import math
import sys
import datetime
import pdb

def RealToInGame(in_game_start_date, real_start_date, adventures, real_date):
  return (in_game_start_date + (real_date - real_start_date).days +
    sum([a.end_date - a.start_date for a in adventures if a.real_date < real_date]))

def InGameToReal(in_game_start_date, real_start_date, adventures, in_game_date):
  return real_start_date + datetime.timedelta(
      in_game_date - in_game_start_date -
      sum([min(a.end_date, in_game_date) - a.start_date
        for a in adventures if in_game_date >= a.start_date]))
