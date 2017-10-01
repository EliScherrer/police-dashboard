from flask import Flask, render_template
from data import getTimelineData
import json
app = Flask(__name__)

@app.route("/")
def home():
	#data = getTimelineData("ME")
	data = testFunc()
	#use a default org?
	return render_template('index.html')

@app.route("/<org>")
def main(org):
	data = getTimelineData(org)
	#get result and pass with render
	return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run()
