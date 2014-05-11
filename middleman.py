###############################
# Middle man Flask app base
###############################
from flask import Flask, request, render_template
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
