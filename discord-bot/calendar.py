# Calendar:
# DayList: all days, in order
# Date: Day + year <-> epoch date
# Day: Month + day
class InGameDay:
  def __init__(self, month, day = None, special_name = None):
    self.month = month
    if day:
      self.day = day
    if special_name:
      self.special_name = special_name

  def __str__(self):
    if special_name:
      if day:
        return '{} {} ({})'.format(month, day, special_name)
      else:
        return special_name
    else:
      return '{} {}'.format(month, day)

class InGameDate:
  def __init__(self, day, year):
    self.day = day
    self.year = year

class Calendar:
  def __init__(self):
    days = []
    days.extend(MakeMonth('Yothh', 30))
    days[0] = InGameDay('Yotth', day=1, special_name='New Year')
    days.extend(MakeMonth('Twyla', 31))
    days.extend(MakeMonth('Rooni', 28))
    days.append(InGameDay('Rooni', special_name='Midsummer\'s Eve'))
    days.extend(MakeMonth('Deamce', 30))
    days.extend(MakeMonth('Cunkur', 28))
    days.extend(MakeMonth('Abilan', 28))
    days.append(InGameDay('Abilan', special_name='Harvest Festival'))
    days.extend(MakeMonth('Fyrgat', 29))
    days.extend(MakeMonth('Lopar', 30))
    days.extend(MakeMonth('Rachi', 28))
    days.append(InGameDay('Abilan', special_name='Ancestor\'s Day'))
    days.extend(MakeMonth('Buold', 31))
    days.extend(MakeMonth('Vlut', 28))
    days.extend(MakeMonth('Unnyt', 27))
    days.append(InGameDay('Unnyt', special_name='Beginning of Candlenights'))
    days.append(InGameDay('Unnyt', special_name='Second Day of Candlenights'))
    days.append(InGameDay('Unnyt', special_name='Third Day of Candlenights'))
    days.append(InGameDay('Unnyt', special_name='Fourth Day of Candlenights'))
    days.append(InGameDay('Unnyt', special_name='Fifth Day of Candlenights'))
    days.append(InGameDay('Unnyt', special_name='Sixth Day of Candlenights'))
    days.append(InGameDay('Unnyt', special_name='Seventh Day of Candlenights'))
    days.append(InGameDay('Unnyt', special_name='Eighth Day of Candlenights'))
    days.append(InGameDay('Unnyt', special_name='End of Candlenights'))

    dayMap = {}
    for i in range(0, len(days) - 1):
      dayMap[str(days[i])] = i

  def MakeMonth(self, name, numDays):
    return map(lambda d : InGameDay(name, day=d), range(numDays))

  # date + numDays
  # date2 - date1

# real world <-> in-world
#   adventure offset list
#   real-world date check
