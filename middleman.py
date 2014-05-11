###############################
# Middle man Flask app base
###############################
from flask import Flask, request, render_template, jsonify
from pyparsing import ParseException

import datetime

from mmlib.jsonparser import apply_scheme_to_json
from mmlib.flaskhelpers.forms import extract_post_data

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
        return jsonify(errors={'parse_errors': [e.msg]})

    return jsonify(result=result)

@app.route('/sampledata', methods=['GET'])
def sample_data():
    rawjson = """
    {
        "name": "Joe McCullough",
        "GPA": 3,
        "nickname": "JoeQuery",
        "likes_cats": true,
        "likes_baseball": 0,
        "favorite_foods": ["tacos", "ramen", "burgers"]
    }
    """.strip()

    scheme = """The name is ${['name']}$, but you can call me ${['nickname']|dquote}$. I had a GPA of ${['GPA']|to_f}$ in college. In a binary sense, the answer to the question "Do I like cats?" is ${['likes_cats']|boolint}$. In a boolean sense, do I like baseball? ${['likes_baseball']|bool}$. I'd totally be down for some ${['favorite_foods'][1]}$ right now. """

    return jsonify(rawjson=rawjson, scheme=scheme)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
