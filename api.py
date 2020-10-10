from flask import Flask, request, jsonify
import sqlite3

#############################################################################
# Initializes this as a Flask project and turns on Debugger (to see output) #
#############################################################################
app = Flask(__name__)
app.config["DEBUG"] = True

# - Helper Functions - #

#################################################################################################################
# Returns Items from the Database as a dictionary instead of a list (works better when outputting them to JSON) #
# In shorth it turns it into {} instead of [] for each item -> JSON                                             #
#################################################################################################################
def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]
    print(d)
    return d




#########################
# HTML for "Homescreen" #
#########################

@app.route('/', methods=['GET'])
def home():
    return "<h1>Dari Words</h1><p>This site is a prototype API for Dari words translated to English.</p>"

##################################################################
# A route to return all of the available entries in the database #
##################################################################
@app.route('/words/all', methods=['GET'])
def api_all():

    conn = sqlite3.connect('words.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_words = cur.execute('SELECT * FROM words;').fetchall()

    return jsonify(all_words)

######################################################
# A route to return a specific entry in the database #
######################################################
@app.route('/words', methods=['GET'])
def api_filter():
    query_parameters = request.args
    print(query_parameters)
    id = query_parameters.get('id')
    english = query_parameters.get('english')
    dari = query_parameters.get('dari')

    query = "SELECT * FROM words WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'

        capilizedID = ""
        capilizedID = str(id)
        capilizedID = capilizedID.capitalize()

        to_filter.append(capilizedID)
    elif english:
        query += ' english=? AND'

        capilizedWord = ""
        capilizedWord = str(english)
        capilizedWord = capilizedWord.capitalize()

        to_filter.append(capilizedWord)
    elif dari:
        query += ' dari=? AND'

        capilizedWord = ""
        capilizedWord = str(dari)
        capilizedWord = capilizedWord.capitalize()

        to_filter.append(capilizedWord)
    else:
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('words.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    print(to_filter)
    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


####################################
# Returns the size of the database #
####################################
@app.route('/count', methods=['GET'])
def api_size():
    conn = sqlite3.connect('words.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    count = cur.execute('SELECT COUNT(*) FROM words;').fetchall()

    return jsonify(count)


#################
# Returns Error #
#################
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

#######################################################
# Runs the API if a request is established Via Client #
#######################################################
if __name__ == '__main__':
    app.run()
