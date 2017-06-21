from .tripattribute import TripAttribute

class Cost(TripAttribute):
    max = -float("inf")
    min = float("inf")
    parameter = "totalFare"
    type="Offer"

    def __init__(self, weight):
        self.weight = float(weight)

    def parsingInstruction(self, totalFare):
        try:
            totalFare = float(totalFare)
            if totalFare > self.max:
                self.max = totalFare
            if totalFare < self.min:
                self.min = totalFare
        except Exception as e:
            print(str(e))

    def rate(self, totalFare):
        try:
            totalFare = float(totalFare)
            if self.max == self.min:
                return 0.5
            return -(totalFare - self.min) / (self.max - self.min)
        except Exception as e:
            print("Cost Trip Attribute Exception - " + str(e))
            return 0.5

