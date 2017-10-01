from flask import Flask, render_template
from data import getTimelineData
import json
app = Flask(__name__)

@app.route("/")
def home():
	data = getTimelineData("PF")
	return render_template('index.html', data=data)

@app.route("/<org>")
def main(org):
	data = getTimelineData(org)
	return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run()
