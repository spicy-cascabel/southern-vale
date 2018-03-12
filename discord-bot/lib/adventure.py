class Adventure:
  def __init__(self, name=None, start_date=None, end_date=None, real_date=None, party_names=None):
    self.name = name
    self.start_date = start_date
    self.end_date = end_date
    self.real_date = real_date
    self.party_names = party_names

  def __str__(self):
    return '{}, {} to {} ({}){}'.format(self.name, self.start_date, self.end_date, self.real_date,
        ' with ' + ', '.join(self.party_names) if self.party_names else '')
