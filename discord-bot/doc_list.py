def find_by_name(name):
  if len(name) < 3:
    return 'I need a longer name to search for.'
  # This should be in a config/data file, and obviously needs real data.
  docs = [
      ['reports', 'reports-url'],
      ['bounty', 'bounty-url'],
      ['houserules', 'house-rules-url'],
      ]
  result = list(filter(lambda d : name in d[0], docs))
  print(result)
  if len(result) > 0:
    return '\n'.join(['{}: {}'.format(d[0],d[1]) for d in result])
  else:
    return 'Nothing found!'
