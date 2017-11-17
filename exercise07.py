from numpy import arange, linalg, loadtxt, hsplit, array
import re

# 1st Part
matrix = loadtxt('matice1.txt')
det = linalg.det(matrix)
invMatrix = linalg.inv(matrix)
print ("Determinant:{}".format(det))
print ("Inversion matrix:\n{}".format(invMatrix))

# 2nd Part
matrix = loadtxt('matice2.txt')
[A,B] = hsplit(matrix, [3])
result = linalg.solve(A,B)
print("x1={}, x2={}, x3={}".format(result[0][0], result[1][0], result[2][0]))

# 3rd Part
with open('equation.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]
content = [x.replace(' ','') for x in content]

variables = []
rows = []
results = []
#Iterate rows
for s in content:
    sides = re.split('=', s)
    if(sides[1][0] not in ['+','-']):
        sides[1] = '+' + sides[1]
    sides[1] = sides[1].replace("-","*")
    sides[1] = sides[1].replace("+","-")
    sides[1] = sides[1].replace("*", "+")
    join = sides[0] + sides[1]
    parts = re.findall("[\+-]{0,1}[0-9]*[a-z]{0,1}", join)
    variableDict = {}
    result = 0
    for p in parts[:-1]:
        sign = re.findall("[\+-]", p)
        variable = re.findall("[a-z]", p)
        num = re.findall("[0-9]+", p)

        if(not num):
            number = 1
        else:
            number = int(num[0])

        if (len(sign) and sign[0] == '-'):
            number = number * (-1)

        if(not variable):
            result += (-1 * number)
        else:
            if(not variable[0] in variables):
                variables.append(variable[0])
            if(variableDict.get(variable[0],None) is None):
                variableDict[variable[0]] = number
            else:
                variableDict[variable[0]] += number
    rows.append(variableDict)
    results.append(result)

matrix = []
for r in rows:
    matrixRow = [];
    for v in variables:
        value = r.get(v, None)
        if(value is None):
            matrixRow.append(0);
        else:
            matrixRow.append(int(value))
    matrix.append(matrixRow)

result = linalg.solve(matrix,results)
output = 'Result: '
for i in range(0,len(variables)):
    output += "{}={}, ".format(variables[i], int(result[i]))

print(output)




