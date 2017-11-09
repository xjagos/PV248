from sys import argv
import sqlite3
import json

author = argv[1]
conn = sqlite3.connect( 'scorelib.dat' )
cursor = conn.cursor()

result = cursor.execute('select person.name, score.name, print.id from person left '
                        'join score_author on person.id = score_author.composer '
                        'join score on score_author.score = score.id '
                        'join edition on score.id = edition.score left '
                        'join print on edition.id = print.edition '
                        'where person.name like "%{}%"'.format(author))


list = []
for r in result:
    item = {}
    item['Composer'] = r[0]
    item['Score'] = r[1]
    item['PrintNumber'] = r[2]
    list.append(item)

with open('output.json', 'w') as outfile:
    json.dump(list, outfile)
conn.commit()