from flask import render_template, url_for, g, session, redirect, flash, request
from app import app
from .forms import VacationPlannerForm
import requests
import datetime
from .segments import Segment
from .legs import Leg
from .offers import Offer
from .cost_tripattribute import Cost
from .travelduration_tripattribute import TravelDuration
from .favoriteairline_tripattribute import FavoriteAirline

# Default page
@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def planner():
    error = False
    name, favorite_airline = fetch_user_details()
    vacationplannerform = VacationPlannerForm(request.form)
    if vacationplannerform.is_submitted():
        if vacationplannerform.validate():

            # Iterate over dates
            datePairs = generateDatePairs(vacationplannerform.weekends.data, vacationplannerform.days.data)
            departureAirport = vacationplannerform.source.data
            arrivalAirport = vacationplannerform.destination.data

            try:
                bestoffers = []
                for i in range(len(datePairs)):
                    # Create Trip Attribute objects
                    cost = Cost(vacationplannerform.costslider.data)
                    travelDuration = TravelDuration(vacationplannerform.durationslider.data)
                    favoriteAirline = FavoriteAirline(vacationplannerform.favoriteairlineslider.data, favorite_airline)
                    tripAttributes = [cost, travelDuration, favoriteAirline]
                    offers = fetchflights_roundtrip(datePairs[i][0], datePairs[i][1], departureAirport, arrivalAirport, tripAttributes)
                    bestofferfortheday = rateOffersAndReturnBest(offers, tripAttributes)
                    bestoffers.append(bestofferfortheday)
                cost = Cost(vacationplannerform.costslider.data)
                travelDuration = TravelDuration(vacationplannerform.durationslider.data)
                tripAttributes = [cost, travelDuration]
                calibrateBestOffers(bestoffers, tripAttributes)
                bestoffers = sorted(bestoffers, key=lambda offer: offer.rating, reverse=True)

                return render_template("results.html", vacationplannerform=vacationplannerform, offers=bestoffers, name=name, favoriteAirline=favorite_airline)
            except Exception as e:
                print("In planner controller" + str(e))
                error = True
        else:
            error=True
    

    return render_template("planner.html", vacationplannerform=vacationplannerform, error=error, name=name, favoriteAirline=favorite_airline)

def fetch_user_details():
    return "Saurabh", "United"
    #r = requests.get("https://watson-traveler-profile-service.prod.expedia.com/v2/traveler/38522057/attributes")
    #user_details = r.json()
    #return user_details["attributes"]["firstName"], user_details["attributes"]["i_preferred_airline_name"]

def calibrateBestOffers(bestOffers, tripAttributes):
    legs = []
    for offer in bestOffers:
        legs += offer.legs

    for leg in legs:
        # Get the trip Attributes for legs
        for tripAttribute in tripAttributes:
            if tripAttribute.type == "Leg":
                tripAttribute.parsingInstruction(getattr(leg, tripAttribute.parameter))

    for offer in bestOffers:
        # Get the trip Attributes for legs
        for tripAttribute in tripAttributes:
            if tripAttribute.type == "Offer":
                tripAttribute.parsingInstruction(getattr(offer, tripAttribute.parameter))

    for offer in bestOffers:
        rating = 0
        for tripAttribute in tripAttributes:
            if tripAttribute.type == 'Leg':
                for leg in offer.legs:
                    rating += tripAttribute.weight * tripAttribute.rate(getattr(leg, tripAttribute.parameter))
            elif tripAttribute.type == 'Offer':
                rating += tripAttribute.weight * tripAttribute.rate(getattr(offer, tripAttribute.parameter))
            offer.rating = rating


# Reference for styling
@app.route('/ref')
def reference():
    return render_template('reference.html')

# Generate date pairs
def generateDatePairs(weekends, days):
    datePairs = []
    currentdate = datetime.datetime.now()
    for i in range(14):
        testdate = currentdate + datetime.timedelta(days=i)
        if weekends:
            if testdate.weekday() in range(7-days,6):
                datePairs.append((str(testdate), str(testdate + datetime.timedelta(days=days))))
        else:
            datePairs.append((str(testdate), str(testdate + datetime.timedelta(days=days))))
    return datePairs

# Provide a rating for the offers and return the best offer
def rateOffersAndReturnBest(offers, tripAttributes):
    bestoffer = offers[0]
    bestofferrating = -float("inf")
    for offer in offers:
        rating = 0
        for tripAttribute in tripAttributes:
            if tripAttribute.type == 'Leg':
                for leg in offer.legs:
                    rating += tripAttribute.weight * tripAttribute.rate(getattr(leg, tripAttribute.parameter))
            elif tripAttribute.type == 'Offer':
                rating += tripAttribute.weight * tripAttribute.rate(getattr(offer, tripAttribute.parameter))
        offer.rating = rating
        if bestofferrating < offer.rating:
            bestoffer = offer
            bestofferrating = offer.rating
    return bestoffer

# Build Flight Objects
def fetchflights_roundtrip(departureDate, returnDate, departureAirport, arrivalAirport, tripAttributes):
    # Make API Call
    r = requests.get("https://www.expedia.com:443/api/flight/search?departureDate={}&returnDate={}&departureAirport={}&arrivalAirport={}&prettyPrint=true".format(departureDate, returnDate, departureAirport, arrivalAirport))
    flightdetails = r.json()

    # Segment Attributes
    segmentAttributes = ["departureTime", "departureAirportLocation", "arrivalTime", "arrivalAirportLocation", "airlineName", "airlineCode", "flightNumber"]

    # Variables
    results = []
    legs = flightdetails["legs"]
    offers = flightdetails["offers"]

    legsdict = {}

    # Parse legs
    for leg in legs:
        segments = []
        airlines = []
        for segment in leg["segments"]:
            segments.append(Segment(**{k:v for k, v in segment.items() if k in segmentAttributes}))
            airlines.append(segment["airlineName"])
        travelDuration = leg["travelDuration"]
        legsdict[leg["legId"]] = Leg(segments, travelDuration, max(airlines, key=airlines.count))
        # Get the trip Attributes for legs
        for tripAttribute in tripAttributes:
            if tripAttribute.type == "Leg" and tripAttribute.parameter != "maxAirline":
                tripAttribute.parsingInstruction(leg[tripAttribute.parameter])

    # Parse offers
    for offer in offers:
        offer_legs = list(map(lambda legid: legsdict[legid], offer["legIds"]))
        totalFare = offer["totalFare"]
        seatsRemaining = offer["seatsRemaining"]
        results.append(Offer(offer_legs, totalFare, seatsRemaining))
        # Get the trip Attributes for offers
        for tripAttribute in tripAttributes:
            if tripAttribute.type == "Offer":
                tripAttribute.parsingInstruction(offer[tripAttribute.parameter])

    return results