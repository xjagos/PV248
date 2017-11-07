from collections import Counter
import re
import cmath

def printComposer(dictionary):
    for k, v in dictionary.items():
        if(k is not None):
            print('{}:{}'.format(k, v))

def printCentury(dictionary):
    for k, v in dictionary.items():
        if(k is not None):
            print('{}th century:{}'.format(k, v))

def convertToInt(s):
    try:
        n = int(s)
        century = (n // 100) + 1
        return century
    except (TypeError, ValueError):
        return None

def modifyName(name):
    pass

authorCompositionCount = Counter()
centuryCompositionCount = Counter()
keyCompositionCount = {}

f = open('scorelib.txt', encoding='utf8')
for line in f:
    r = re.compile(r"Composer: ([A-Za-z]+), ([A-Za-z]+) ([A-Za-z]+)")
    m = r.match(line)

    if(m is not None):
        name = "{}, {}. {}.".format(m.group(1),m.group(2)[0],m.group(3)[0])
        authorCompositionCount[name] += 1


    r = re.compile(r"Composition Year: (.*)")
    m = r.match(line)
    if(m is not None):
        century = convertToInt(m.group(1))
        centuryCompositionCount[century] += 1

authorDict = dict(authorCompositionCount)
centuryDict = dict(centuryCompositionCount)

printComposer(authorDict)
print()
printCentury(centuryDict)



