class Offer:
    legs = None
    totalFare = None
    seatsRemaining = None
    rating = None
    def __init__(self, legs, totalFare, seatsRemaining):
        self.legs = legs
        self.totalFare = totalFare
        self.seatsRemaining = seatsRemaining
        self.rating = None