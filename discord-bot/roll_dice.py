#!/usr/bin/python3
import random

def rollOneDie(n, k):
  return [random.randrange(1, k) for x in range(n)]

def printOneDieResult(result):
  return '+'.join([str(x) for x in result])


def rollDice(diceString):
  try:
    diceString = diceString.replace(' ', '')
    characters = set(diceString)
    parseError = 'Error: dice string must be of the form XdY (+XdY ... +Z), e.g. 1d20+1d4 or 5+2d6'
    if not set(diceString).issubset(set('01234567890+d')):
      return parseError
    dice = diceString.split('+')
    result = []
    for die in dice:
      if 'd' in die:
        (n,k) = die.split('d')
        result.append(rollOneDie(int(n), int(k)))
      else:
        result.append([int(die)])
    if len(result) == 1:
      if len(result[0]) == 1:
        return '**{}**'.format(result[0][0])
      expanded_result = '{}'.format(printOneDieResult(result[0]))
    else:
      expanded_result = ' + '.join(['({})'.format(printOneDieResult(l))], result)
    final_sum = sum([sum(l) for l in result])
    return '**{}** ({})'.format(final_sum, expanded_result)
  except:
    return parseError
