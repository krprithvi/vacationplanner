from .tripattribute import TripAttribute

class FavoriteAirline(TripAttribute):
    parameter = "maxAirline"
    favoriteAirline = None
    type="Leg"

    def __init__(self, weight, favoriteAirline):
        self.weight = float(weight)
        self.favoriteAirline = favoriteAirline

    def parsingInstruction(self, totalFare):
        pass

    def rate(self, airline):
        try:
            if airline == self.favoriteAirline:
                return (self.weight/2.0)
            return 0
        except Exception as e:
            print("Favorite Airline exception --> " + str(e))
            return 0
