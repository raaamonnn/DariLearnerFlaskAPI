from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
words = [
    {'id': 0,
     'EnglishWord': 'Hello',
     'DariWord': 'Salam'},
    {'id': 1,
     'EnglishWord': 'One',
     'DariWord': 'Yak'},
    {'id': 2,
     'EnglishWord': 'Naan',
     'DariWord': "Bread"}
]
#
def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]
    print(d)
    return d


@app.route('/', methods=['GET'])
def home():
    return "<h1>Dari Words</h1><p>This site is a prototype API for Dari words translated to English.</p>"


# A route to return all of the available entries in our catalog.a
@app.route('/words/all', methods=['GET'])
def api_all():

    conn = sqlite3.connect('words.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_words = cur.execute('SELECT * FROM words;').fetchall()

    return jsonify(all_words)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/words', methods=['GET'])
def api_filter():
    query_parameters = request.args
    id = query_parameters.get('id')
    word = query_parameters.get('word')

    query = "SELECT * FROM words WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    elif word:
        query += ' english=? AND'
        to_filter.append(word)
    else:
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('words.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

# @app.route('/words', methods=['GET'])
# def api_id():
#     results = []
#
#     if 'id' in request.args:
#         requestid = request.args.get('id')
#         for word in words:
#             if word['id'] == requestid:
#                 results.append(word)
#
#     elif 'word' in request.args:
#         requestWord = request.args.get('word')
#         requestWord = str(requestWord)
#         requestWord = requestWord.capitalize()
#         print(requestWord)
#         for word in words:
#             print(word['DariWord'] == requestWord)
#             if word['EnglishWord'] == requestWord or word['DariWord'] == requestWord:
#                 results.append(word)
#
#     else:
#         return "Error: No valid field provided. Please specify an id or word."
#
#     # Use the jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)

if __name__ == '__main__':
    app.run()
