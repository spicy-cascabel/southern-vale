import math
import sys
import datetime
from functools import total_ordering

class InGameDay:
  def __init__(self, month, day_of_month = None, special_name = None):
    self.month = month
    self.day_of_month = day_of_month
    self.special_name = special_name

  def __repr__(self):
    if self.special_name:
      if self.day_of_month:
        return '{} {} ({})'.format(self.month, self.day_of_month, self.special_name)
      else:
        return self.special_name
    else:
      return '{} {}'.format(self.month, self.day_of_month)

  def __eq__(self, other):
    return (self.day_of_month, self.month) == (other.day_of_month, other.month)

  def __ne__(self, other):
    return (self.day_of_month, self.month) != (other.day_of_month, other.month)

@total_ordering
class InGameDate:
  def __init__(self, day, year):
    self.day = day
    self.year = year

  @staticmethod
  def FromEpochDay(epoch_day):
    return InGameDate(_cal.days[epoch_day % _cal.DaysPerYear()],
                      _cal.epoch_year + int(math.floor(epoch_day / _cal.DaysPerYear())))

  def ToEpochDay(self):
    return (self.year - _cal.epoch_year) * _cal.DaysPerYear() + _cal.day_map[str(self.day)]

  def __str__(self):
    return '{} {}'.format(str(self.day), self.year)

  # subtract dates
  def __sub__(self, other):
    return self.ToEpochDay() - other.ToEpochDay()

  # add integers
  def __add__(self, other):
    return InGameDate.FromEpochDay(self.ToEpochDay() + other)

  def __eq__(self, other):
    return (self.day, self.year) == (other.day, other.year)

  def __ne__(self, other):
    return (self.day, self.year) != (other.day, other.year)

  def __lt__(self, other):
    return other - self > 0

  @staticmethod
  def _is_number(n):
    return set(n).issubset(set('0123456789'))

  @staticmethod
  def FromString(date_string):
    # Formats:
    # Twyla 15 [1252]
    # 15 Twyla [1252]
    # Midsummer's Eve [1252]
    tokens = date_string.split(' ')
    year = _cal.default_year
    # find large number to use as year
    for t in tokens:
      if InGameDate._is_number(t) and int(t) > 1000:
        year = int(t)
        tokens.remove(t)
        break
    day_of_month = 0
    # find number to use as day of month
    for t in tokens:
      if InGameDate._is_number(t):
        day_of_month = int(t)
        tokens.remove(t)
        break
    if day_of_month > 0:
      # month/day
      if len(tokens) != 1:
        return None
      day_string = '{} {}'.format(tokens[0], day_of_month)
      if day_string in _cal.day_map:
        return InGameDate(_cal.days[_cal.day_map[day_string]], year)
    else:
      # special name
      day_string = ' '.join(tokens)
      if day_string in _cal.day_map:
        return InGameDate(_cal.days[_cal.day_map[day_string]], year)
    return None

class InGameCalendar:
  def __init__(self):
    self.epoch_year = 1252
    self.default_year = 1252

    self.days = []
    self.days.extend(self.MakeMonth('Yothh', 30))
    self.days[0] = InGameDay('Yotth', day_of_month=1, special_name='New Year')
    self.days.extend(self.MakeMonth('Twyla', 31))
    self.days.extend(self.MakeMonth('Rooni', 28))
    self.days.append(InGameDay('Rooni', special_name='Midsummer\'s Eve'))
    self.days.extend(self.MakeMonth('Deamce', 30))
    self.days.extend(self.MakeMonth('Cunkur', 28))
    self.days.extend(self.MakeMonth('Abilan', 28))
    self.days.append(InGameDay('Abilan', special_name='Harvest Festival'))
    self.days.extend(self.MakeMonth('Fyrgat', 29))
    self.days.extend(self.MakeMonth('Lopar', 30))
    self.days.extend(self.MakeMonth('Rachi', 28))
    self.days.append(InGameDay('Abilan', special_name='Ancestor\'s Day'))
    self.days.extend(self.MakeMonth('Buold', 31))
    self.days.extend(self.MakeMonth('Vlut', 28))
    self.days.extend(self.MakeMonth('Unnyt', 27))
    self.days.append(InGameDay('Unnyt', special_name='Beginning of Candlenights'))
    self.days.append(InGameDay('Unnyt', special_name='Second Day of Candlenights'))
    self.days.append(InGameDay('Unnyt', special_name='Third Day of Candlenights'))
    self.days.append(InGameDay('Unnyt', special_name='Fourth Day of Candlenights'))
    self.days.append(InGameDay('Unnyt', special_name='Fifth Day of Candlenights'))
    self.days.append(InGameDay('Unnyt', special_name='Sixth Day of Candlenights'))
    self.days.append(InGameDay('Unnyt', special_name='Seventh Day of Candlenights'))
    self.days.append(InGameDay('Unnyt', special_name='Eighth Day of Candlenights'))
    self.days.append(InGameDay('Unnyt', special_name='End of Candlenights'))

    self.day_map = {}
    for i in range(len(self.days)):
      self.day_map[str(self.days[i])] = i
      if self.days[i].special_name:
        self.day_map[self.days[i].special_name] = i

  def DaysPerYear(self):
    return len(self.days)

  def MakeMonth(self, name, numDays):
    return map(lambda d : InGameDay(name, day_of_month=d), range(1, numDays + 1))

_cal = InGameCalendar()

def SetDefaultYear(year):
  _cal.default_year = year
