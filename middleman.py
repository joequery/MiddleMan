###############################
# Middle man Flask app base
###############################
from flask import Flask, request, render_template, jsonify
from pyparsing import ParseException

import datetime

from jsonparser import apply_scheme_to_json
from flaskhelpers.forms import extract_post_data

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/process', methods=['POST'])
def process():
    required_fields = ('scheme', 'rawjson')
    post,errors = extract_post_data(request, required_fields)

    if errors:
        return jsonify(errors=errors)

    try:
        result = apply_scheme_to_json(post['scheme'], post['rawjson'])
    except ParseException, e:
        return jsonify(errors={'parse_errors': [str(e)]})

    return jsonify(result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
