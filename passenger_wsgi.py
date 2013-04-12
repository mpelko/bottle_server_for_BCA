
#1. Add current directory to path, if isn't already
import os, sys
bottle_folder = "/home/mpelko/nuclearScotland.bajta.org/bottle"
if bottle_folder not in sys.path:
    sys.path.insert(0, bottle_folder)

print sys.path

import sqlite3
import bottle
from bottle.ext import sqlite
from bottle import route, run, template, request

app = bottle.Bottle()
#plugin = sqlite.Plugin('/home/mpelko/nuclearScotland.bajta.org/tmp/ns.db')
plugin = sqlite.Plugin('./tmp/ns.db')
app.install(plugin)

#2. Define needed routes here
@app.route('/')
def index():
        return "it  works!"

def jsonp(request, dictionary):
    if (request.query.callback):
        return "%s(%s)" % (request.query.callback, dictionary)
    return dictionary


@app.route('/get/bookID', method="GET")
def book_id(db):
    title = request.GET.get('title')

    print "______"
    print title
    print "--------"

    a = db.execute('SELECT bid FROM books WHERE title LIKE ?', (title,))
    result = a.fetchone()
    if result:
        result = {"bid":str(result[0])}
    else:
        db.execute("INSERT INTO books (title) VALUES (?)", (title,))
        a = db.execute('SELECT bid FROM books WHERE title LIKE ?', (title,))
        result = {"bid":str(a.fetchone()[0])}

    print result
    return jsonp(request, result)
        
@app.route('/get/QAs', method="GET")
def QAs(db):
    bid = request.GET.get('bid')
    #print "/////////////"
    q = db.execute('SELECT qid, location, username, title FROM questions WHERE bid LIKE ?', (bid,))
    qs = q.fetchall()
    questions = []
    for q in qs:
        a = db.execute('SELECT text, username FROM answers WHERE qid LIKE ?', (q[0],))
        answs = a.fetchall()
        answers = [{"text":str(a[0]),"username":str(a[1])} for a in answs]
        questions.append({"answers":answers, "questionID":str(q[0]), "bookID":bid, "location":q[1], "title":str(q[3]), "username":str(q[2])})
    #result = {"QAs":[{"title":"asd","answers":[{"text":"asdasd", "username":"mpelko"}]}]}
    result = {"QAs":questions}
    #result = {"QAs":questions[0]}
    return jsonp(request, result)

@app.route('/submit/Q', method="GET")
def insert_Q(db):
    try:
        bid = request.GET.get('bid')
        title = request.GET.get('title')
        usr = request.GET.get('username')
        loc = request.GET.get('location')
        qid = get_new_qid(db, bid)
        db.execute("INSERT INTO questions VALUES (?,?,?,?,?)", (qid, bid, loc, title, usr))
        return jsonp(request,{"daffodil":0})
    except Exception, e:
        return jsonp(request,{"daffodil":1, "errormsg":str(e)})

@app.route('/submit/A', method="GET")
def insert_A(db):
    try:
        bid = request.GET.get('bid')
        text = request.GET.get('text')
        usr = request.GET.get('username')
        qid = request.GET.get('qid')
        db.execute("INSERT INTO answers (text, qid, username) VALUES (?,?,?)", (text, qid, usr))
        return jsonp(request,{"daffodil":0})
    except Exception, e:
        return jsonp(request,{"daffodil":1, "errormsg":str(e)})

def get_new_qid(db, book_id):
    q = db.execute('SELECT qid FROM questions WHERE bid LIKE ?', (book_id,))
    curr_length = len(q.fetchall())
    return book_id + "_" + str(curr_length+1)
    
#3. setup dreamhost passenger hook
def application(environ, start_response):
    return app.wsgi(environ,start_response)

#4. Main method for local developement
if __name__ == "__main__":
    bottle.debug(True)
    app.run(reloader=True)