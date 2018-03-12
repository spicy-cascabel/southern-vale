docs = [
    ['reports', 'https://docs.google.com/document/d/18ZeN0azwQbyZkIyY3O7iO8D5snZl1mQumDEqUkPVSPU/view'],
    ['primer', 'https://docs.google.com/document/d/1pzP0GLosN02VXsbQlceqrWnZ_hYGueXPOGzRxY51_O8/view'],
    ['gamekeeper', 'https://docs.google.com/document/d/1QZ5GSsq0OqVjQUymnwnRuuw-P1LwwJYf5R696sHFy_0/view'],
    ['tokens', 'https://docs.google.com/document/d/1J9AzFBrh371TZb3ztfhaBFI0iteam924WXdx0RHqdcc/view'],
    ['houserules', 'https://docs.google.com/document/d/1VFdZe3w-43LUXkmnZCxx9CggO65a935B5AjEwNTWUcs/view'],
    ]
docs.sort()

def find_by_name(name):
  if len(name) < 3:
    return 'I need a longer name to search for.'
  # TODO put in Google docs
  result = list(filter(lambda d : name in d[0], docs))
  print(result)
  if len(result) > 0:
    return '\n'.join(['{}: {}'.format(d[0],d[1]) for d in result])
  else:
    return 'Nothing found!'

def list_all():
  if len(docs) > 100:
    return 'Over 100 docs; try finddoc.'
  return 'Known docs: {}'.format(', '.join([x[0] for x in docs]))
