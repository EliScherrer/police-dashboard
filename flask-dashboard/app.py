from flask import Flask, render_template
from './../data.py' import getTimelineData
app = Flask(__name__)

@app.route("/")
def home():
	#use a default org?
	return render_template('index.html')

@app.route("/<org>")
def main(org):
	function(org)
	#get result and pass with render
	return render_template('index.html', org=org)

if __name__ == "__main__":
    app.run()
