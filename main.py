from collections import Counter
import re
import cmath

def printData(dictionary):
    for k, v in dictionary.items():
        print('Composer:{}, Count:{}'.format(k, v))

def convertToInt(s):
    try:
        n = int(s)
        century = (n // 100) + 1
        return century
    except (TypeError, ValueError):
        return None

authorCompositionCount = Counter()
centuryCompositionCount = Counter()
keyCompositionCount = {}

f = open('scorelib.txt', encoding='utf8')
for line in f:
    r = re.compile(r"Composer: (.*)")
    m = r.match(line)

    if(m is not None):
        authorCompositionCount[m.group(1)] += 1


    r = re.compile(r"Composition Year: (.*)")
    m = r.match(line)
    century = convertToInt(m)
    if(century is not None):
        print(century)
        centuryCompositionCount[century] += 1

authorDict = dict(authorCompositionCount)
centuryDict = dict(centuryCompositionCount)

'''printData(authorDict)'''
printData(centuryDict)



