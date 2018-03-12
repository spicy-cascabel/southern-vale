import lib.adventure
import lib.character
import lib.full_calendar
import lib.google_sheets_import
import pdb

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
    self.characters = []
    self.calendar = lib.full_calendar.FullCalendar()
    (success, message) = self.fetch_data()
    if not success:
      print('Error fetching data during WorldState initialization: ' + message)
      sys.exit(1)

  def fetch_data(self):
    (success, message, fetched_data) = lib.google_sheets_import.fetch_data()
    if not success:
      return (False, message)
    if 'adventures' not in fetched_data:
      return (False, 'No adventures data in fetched data.')
    (success, adv_message) = self._add_adventures(fetched_data['adventures'])
    return (success, adv_message)

  def RealToInGame(self, real_date):
    return self.calendar.RealToInGame(self.adventures, real_date)

  def InGameToReal(self, in_game):
    return self.calendar.InGameToReal(self.adventures, in_game)

  #######################
  # Private
  def _add_adventures(self, adventures):
    if len(adventures) > 0:
      self.real_start_date = adventures[0].real_date
      self.calendar.in_game_start_date = adventures[0].start_date
      new_adventures = []
      # TODO redundant code
      for a in adventures:
        new_adventures.append(a)
        in_game_from_real = self.calendar.RealToInGame(adventures, a.real_date)
        if in_game_from_real != a.start_date:
          self.adventures = prev_adventures
          return (False, 'in-game start date is {}, but real date {} should be {} in-game'.format(
            a.start_date, a.real_date, in_game_from_real))
        start_real = self.calendar.InGameToReal(adventures, a.start_date)
        if start_real != a.real_date:
          self.adventures = prev_adventures
          return (False, 'real date is {}, but in-game start date {} should be {}'.format(
            a.real_date, a.start_date, start_real))
        end_real = self.calendar.InGameToReal(adventures, a.end_date)
        if end_real != a.real_date:
          self.adventures = prev_adventures
          return (False, 'real date is {}, but in-game end date {} should be {}'.format(
            a.real_date, a.end_date, end_real))
      self.adventures = new_adventures
    return (True, 'success')
