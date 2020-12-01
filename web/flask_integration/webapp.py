#!/usr/bin/env python3
'''
    webapp.py

    A program that acts as a controller between datasource.py and the template htmls.

    Gracie Little, Rudra Subramanian, Rebecca Fox, Yemi Shin 
    25 May 2020
    CS257
'''
import flask
from flask import render_template, request, redirect
import json
import sys
from numpy.random import f
from datasource import * 

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results/',methods=["GET","POST"])
def result():
    if request.method == "POST":
        req = request.form
        
        state = req.get("State")
        caseType = req.get("CaseType")
        display = req.get("Display")
        startDate = req.get("startdate")
        endDate = req.get("enddate")
        perCapita = req.get("perCapita")  
        
        datasource = DataSource("subramanianr", "lamp843chair")
        
        if perCapita:
            if state == "All":
                getPerCapitaAllStatesResults = datasource.getCasesPerCapitaAllStates(endDate, caseType)
                return render_template('map_image.html', result = getPerCapitaAllStatesResults)
            else:
                getPerCapitaOneState = datasource.getCasesPerCapita1State(state, caseType)
                return render_template('map_single_value.html', result = getPerCapitaOneState, state = state, casetype = caseType)
        
        else:
            getResults = datasource.getCases(state, caseType, startDate, endDate)
            print("test")
            return render_template('map_image.html', result = getResults)

@app.route('/about/')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
