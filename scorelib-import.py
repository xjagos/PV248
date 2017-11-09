import re # regular expressions
import sqlite3

# This is a base class for objects that represent database items. It implements
# the store() method in terms of fetch_id and do_store, which need to be
# implemented in every derived class (see Person below for an example).

class DBItem:
    def __init__( self, conn ):
        self.id = None
        self.cursor = conn.cursor()

    def store( self ):
        self.fetch_id()
        if ( self.id is None ):
            self.do_store()
            self.cursor.execute( "select last_insert_rowid()" )
            self.id = self.cursor.fetchone()[ 0 ]

# Example of a class which represents a single row of a single database table.
# This is a very simple example, since it does not contain any references to
# other objects.

class Person( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )
        self.born = self.died = None
        self.name = re.sub( '\([0-9/+-]+\)', '', string ).strip()
        # NB. The code below was part of the exercise (extracting years of birth & death
        # from the string).
        m = re.search( "([0-9]+)--([0-9]+)", string )
        if not m is None:
            self.born = int( m.group( 1 ) )
            self.died = int( m.group( 2 ) )

    def fetch_id( self ):
        self.cursor.execute( "select id from person where name = ?", (self.name,) )

        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[ 0 ]
            if((self.born is not None) and (self.died is not None)):
                self.cursor.execute( "update person set born = {}, died = {} where id = {}".format(self.born, self.died, res[0]) )


    def do_store( self ):
        print ("storing '%s'" % self.name)
        # NB. Part of the exercise was adding the born/died columns to the below query.
        self.cursor.execute( "insert into person (name, born, died) values (?, ?, ?)",
                             ( self.name, self.born, self.died ) )

class Score(DBItem):
    def __init__(self, conn, name, genre, key, incipit, year):
        super().__init__(conn)
        self.name = name
        self.genre = genre
        self.key = key
        self.incipit = incipit
        self.year = year

    def fetch_id(self):
        self.cursor.execute("select id from score where name = ?", (self.name,))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

    def do_store(self):
        print("storing '%s'" % self.name)
        self.cursor.execute("insert into score (name, genre, key, incipit, year) values (?, ?, ?, ?, ?)",
                            (self.name, self.genre, self.key, self.incipit,self.year))

class ScoreAuthor(DBItem):
    def __init__(self, conn, score, composer):
        super().__init__(conn)
        self.score = score
        self.composer = composer

    def fetch_id(self):
        self.cursor.execute("select id from score_author where score = {} and composer = {}".format(self.score,self.composer))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

    def do_store(self):
        self.cursor.execute("insert into score_author (score, composer) values (?, ?)",
                            (self.score, self.composer))

class Edition(DBItem):
    def __init__(self,conn, score, name, year):
        super().__init__(conn)
        self.score = score
        self.name = name
        self.year = year

    def fetch_id(self):
        self.cursor.execute("select id from edition where score = {}".format(self.score))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

    def do_store(self):
        self.cursor.execute("insert into edition (score, name, year) values (?, ?, ?)",
                            (self.score, self.name, self.year))

class EditionAuthor(DBItem):
    def __init__(self, conn, edition, editor):
        super().__init__(conn)
        self.edition = edition
        self.editor = editor

    def fetch_id(self):
        self.cursor.execute("select id from edition_author where edition = {} and editor ={}".format(self.edition, self.editor))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

    def do_store(self):
        self.cursor.execute("insert into edition_author (edition, editor) values (?, ?)", (self.edition, self.editor))

class Print(DBItem):
    def __init__(self, conn, number, partiture, edition):
        super().__init__(conn)
        if(partiture.lower() == 'yes'):
            self.partiture = 'Y'
        else:
            self.partiture = 'N'
        self.id = number
        self.edition = edition

    def fetch_id(self):
        pass

    def do_store(self):
        self.cursor.execute("insert into print (id, partiture, edition) values (?, ?, ?)", (self.id, self.partiture, self.edition,))

class Voice(DBItem):
    def __init__(self, conn, number, score, name):
        super().__init__(conn)
        self.number = number
        self.score = score
        self.name = name

    def fetch_id(self):
        self.cursor.execute(
            "select id from voice where number = {} and score = {}".format(self.number, self.score))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

    def do_store(self):
        self.cursor.execute("insert into voice (number, score, name) values (?, ?, ?)",
                            (self.number, self.score, self.name))

# Process one print of input.
def process(printDict):
    composers = []
    if not printDict:
        return

    s = Score(conn, printDict.get('Title', None), printDict.get('Genre', None), printDict.get('Key', None),
              printDict.get('Incipit', None), printDict.get('Composition Year', None))
    s.store()

    for c in printDict['Composer'].split(';'):
        p = Person( conn, c.strip() )
        p.store()

        sa = ScoreAuthor( conn, s.id, p.id)
        sa.store()

    edition = Edition(conn, s.id, printDict.get('Edition', None), printDict.get('Publication Year', None))
    edition.store()

    printItem = Print(conn,printDict.get('Print Number', None), printDict.get('Partiture', None), edition.id)
    printItem.do_store()

    editors = printDict.get('Editor', None)
    if(editors is not None):
        for e in editors.split(';'):
            p = Person( conn, e.strip() )
            p.store()
            ea = EditionAuthor(conn, edition.id, p.id)
            ea.store()

    rx = re.compile(r"Voice ([0-9]*)")
    for k,v in printDict.items():
        m = rx.match(k)
        if m is None:
            continue
        v = Voice(conn, m.group(1), s.id, v)
        v.store()


# Database initialisation: sqlite3 scorelib.dat ".read scorelib.sql"
conn = sqlite3.connect( 'scorelib.dat' )
rx = re.compile( r"(.*): (.*)" )

printDict = dict()
for line in open( 'scorelib.txt', 'r', encoding='utf-8' ):
    if line == '\n':
        process(printDict)
        printDict.clear()
    else:
        m = rx.match(line)
        if m is None:
            continue
        k = m.group(1)
        v = m.group(2)
        printDict[k] = v

conn.commit()
