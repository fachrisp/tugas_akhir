import mysql.connector
from datetime import date, datetime, timedelta
from mysql.connector import errorcode
import flask
from flask import request, jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/resources/rfid/all', methods=['GET'])
def api_all():
    cnx = mysql.connector.connect(user='fachri', password='kinsl4y3r',
                              host='85.10.205.173',
                              database='tugas_akhir')

    cur = cnx.cursor()
    cur.execute("SELECT * FROM id_rfid;")
    rows = cur.fetchall()

    cur.execute("SELECT * FROM antrian;")
    rows2 = cur.fetchall()

    cur.execute("SELECT count(*) FROM id_rfid;")
    jumlah = cur.fetchall()

    return_obj = []
    return_obj.append(rows)
    return_obj.append(rows2)
    return_obj.append(jumlah)

    # import pdb
    # pdb.set_trace()



    return jsonify(return_obj)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

if __name__ == '__main__':
    #app.run(debug=True, use_reloader=True)
    app.run()