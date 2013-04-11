import sqlite3

qs = [("1_1", 1, 25, "Why", "mpelko"),
      ("1_2", 1, 60, "Really?", "mpelko"),
      ("1_3", 1, 260, "I don't understand.", "mpelko"),
      ]

anws = [
        ("Because.", "1_1", "scotty"),
        ("Because.", "1_2", "scotty"),
        ("Because.", "1_3", "scotty"),
        ("Because2.", "1_1", "markus"),
        ]

def setup():
    con=sqlite3.connect('tmp/ns.db')
    con.execute('''CREATE TABLE books (bid INTEGER PRIMARY KEY, title char(200) NOT NULL)''')
    con.execute("INSERT INTO books (title) VALUES ('The Phantom of the Opera')")
    con.execute('''CREATE TABLE questions (qid char(200), bid INTIGER NOT NULL, location INTIGER NOT NULL, title char(300) NOT NULL, username char(50))''')
    for q in qs:
        con.execute("INSERT INTO questions VALUES (?,?,?,?,?)", q)
    con.execute('''CREATE TABLE answers (aid INTEGER PRIMARY KEY, text char(200) NOT NULL, qid char(200) NOT NULL, username char(50))''')
    for a in anws:
        con.execute("INSERT INTO answers (text, qid, username) VALUES (?,?,?)", a)    
    con.commit()


if __name__ == "__main__":
    setup()