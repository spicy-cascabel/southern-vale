class Character:
  def __init__(self, name, nicknames, race_class):
    self.name = name
    self.nicknames = nicknames
    self.race_class = race_class

  def __repr__(self):
    '{} ({})'.format(self.name, self.race_class)
