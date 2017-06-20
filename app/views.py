from flask import render_template, url_for, g, session, redirect, flash, request
from app import app
from .forms import VacationPlannerForm
import requests
import datetime


# Default page
@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def planner():
    error = False
    vacationplannerform = VacationPlannerForm(request.form)
    if vacationplannerform.is_submitted():
        if vacationplannerform.validate():
            # Iterate over dates
            departureDate = "2017-12-15"
            returnDate = "2017-12-18"
            departureAirport = vacationplannerform.source.data
            arrivalAirport = vacationplannerform.destination.data
            flights = fetchflights_roundtrip(departureDate, returnDate, departureAirport, arrivalAirport)
            return render_template("results.html", vacationplannerform=vacationplannerform, flights=flights)
        else:
            error=True
    

    return render_template("planner.html", vacationplannerform=vacationplannerform, error=error)


# Reference for styling
@app.route('/ref')
def reference():
    return render_template('reference.html')

#def generateDatePairs(weekends):
#    datePairs = []
#    currentdate = datetime.datetime.now()
#    for _ in range(30):
#        if weekends:






def fetchflights_roundtrip(departureDate, returnDate, departureAirport, arrivalAirport):
    r = requests.get("https://www.expedia.com:443/api/flight/search?departureDate={}&returnDate={}&departureAirport={}&arrivalAirport={}&prettyPrint=true".format(departureDate, returnDate, departureAirport, arrivalAirport))
    flightdetails = r.json()

    legs = flightdetails["legs"]
    legsdict = {leg["legId"]:leg for leg in legs}
    offers = flightdetails["offers"]
    #ks = list(legsdict)
    #print ks[0]
    results = []

    for offer in offers[:2]:
        to, frm = map(lambda legid: legsdict[legid], offer["legIds"])
        result = (to, frm)
        results.append(result)
    return results
