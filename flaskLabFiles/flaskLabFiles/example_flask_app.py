#!/usr/bin/env python3
'''
    example_flask_app.py
    Jeff Ondich, 22 April 2016
    Modified by Eric Alexander, January 2017

    A slightly more complicated Flask sample app than the
    "hello world" app found at http://flask.pocoo.org/.
'''
import flask
from flask import render_template, request
import json
import sys

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def hello():
    return 'Hello, Citizen of CS257.'

@app.route('/fancier/')
def itDoesHTML():
    htmlStr = '<html lang="en">' + \
        '<head>' + \
        '  <title>Cool page</title>' + \
        '</head>' + \
        '<body>' + \
        '  <h1>Welcome to CS 257</h1>' + \
        '  <p>Please refrain from feeding the squirrels. &lt;test this&gt; </p>' + \
        '</body>' + \
        '</html>'
    return htmlStr

@app.route('/boring/')
def boring():
    return render_template('boring.html')

@app.route('/greet/<person>/')
def greet(person):
    return render_template('greet.html',
                           person=person)

@app.route('/fruit')
def fruit():
    myFruit = [
        {'name': 'apple', 'rating': 7},
        {'name': 'banana', 'rating': 5},
        {'name': 'pear', 'rating': 4}
    ]

    return render_template('fruit.html',
                           fruits=myFruit)

@app.route('/fruitWithQuery/')
def fruitWithQuery():
    myFruit = []

    for i in range(5):
        myFruit.append({'name': request.args.get('name'), 'rating': request.args.get('rating')})

    return render_template('fruit.html',
                    fruits=myFruit)

@app.route('/fruitImg/')
def fruitImg():
    return render_template('fruitImg.html')

@app.route('/authors/<author>')
def get_author(author):
    ''' What a dopey function! But it illustrates a Flask route with a parameter. '''
    if author == 'Twain':
        author_dictionary = {'last_name':'Twain', 'first_name':'Mark'}
    elif author == 'Shakespeare':
        author_dictionary = {'last_name':'Shakespeare', 'first_name':'William'}
    else:
        author_dictionary = {'last_name':'McBozo', 'first_name':'Bozo'}
    return json.dumps(author_dictionary)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
