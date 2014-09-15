import json
from flask import Flask, render_template
app = Flask(__name__)

output_contents = []
with open('../output.txt', 'r') as data_file:
    output_contents = data_file.readlines()

@app.route('/')
def hello_world():

    return render_template('home.html', races=output_contents)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
