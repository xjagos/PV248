from sys import argv
import sqlite3
import json

printNumber = argv[1]
conn = sqlite3.connect( 'scorelib.dat' )
cursor = conn.cursor()

result = cursor.execute("select person.name from person join score_author on person.id = score_author.composer "
                        "join edition on score_author.score = edition.score "
                        "join print on edition.id = print.edition where print.id = {}".format(printNumber))

authors = []
d = {}
for r in result:
    authors.append(r[0])

d['composers'] = authors

with open('authors_output.json', 'w') as outfile:
    json.dump(d, outfile)

conn.commit()