class CharacterList:
  def __init__(self):
    characters = []

  def find_by_name(self, name):
    for c in self.characters:
      if c.match_name == name.lower():
        return c
      if name.lower() in c.match_nicknames:
        return c
    return None

  def find_by_discord_user(self, discord_user):
    discord_id = discord_user.name
    if discord_user.discriminator:
      discord_id += '#{}'.format(discord_user.discriminator)
    for c in self.characters:
      if c.discord_id == discord_id:
        return (c, None)
    return (None, 'no character found with discord id "{}"'.format(discord_id))

class Character:
  def __init__(self, name, race_class, nicknames=None, discord_id=None):
    # Canonical name, for printing and canonical internal lookups.
    self.name = name

    self.race_class = race_class
    # Canonical nicknames, for printing.
    self.nicknames = None

    # Match names, for use with user input.
    self.match_name = name.lower()
    self.match_nicknames = [n.lower() for n in nicknames]

    if nicknames != ['']:
      self.nicknames = nicknames

    self.discord_id = discord_id

  def __str__(self):
    s = '{} ({})'.format(self.name, self.race_class)
    if self.nicknames:
      s += ' (aka {})'.format(', '.join(self.nicknames))
    if self.discord_id:
      s += ' (discord: {})'.format(self.discord_id)
    return s
