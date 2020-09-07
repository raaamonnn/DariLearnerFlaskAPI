from flask import Flask, request, jsonify

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
     'DariWord': 'Bread'}
]


@app.route('/', methods=['GET'])
def home():
    return "<h1>Dari Words</h1><p>This site is a prototype API for Dari words translated to English.</p>"


# A route to return all of the available entries in our catalog.a
@app.route('/words/all', methods=['GET'])
def api_all():
    return jsonify(words)


@app.route('/words', methods=['GET'])
def api_id():
    results = []

    if 'id' in request.args:
        id = int(request.args['id'])
        print("if")
        for word in words:
            if word['id'] == id:
                results.append(word)


    #not working for some reason
    elif 'word' in request.args:
        word = int(request.args['word'])
        print("elif")
        print(word)
        for word in words:
            if word['EnglishWord'] == word or word['DariWord'] == word:
                results.append(word)

    else:
        return "Error: No id field provided. Please specify an id or word."

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

if __name__ == '__main__':
    app.run()
