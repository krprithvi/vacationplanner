class Segment:
    departureTime = None
    departureTimeFormatted = None
    departureAirportLocation = None
    arrivalTime = None
    arrivalAirportLocation = None
    airlineName = None
    airlineCode = None
    flightNumber = None

    def __init__(self, departureTime, departureAirportLocation, arrivalTime, arrivalAirportLocation, airlineName, airlineCode, flightNumber):
        self.departureTime = departureTime
        self.departureTimeFormatted = departureTime[:-11]
        self.departureAirportLocation = departureAirportLocation
        self.arrivalTime = arrivalTime
        self.arrivalAirportLocation = arrivalAirportLocation
        self.airlineName = airlineName
        self.airlineCode = airlineCode
        self.flightNumber = flightNumber
