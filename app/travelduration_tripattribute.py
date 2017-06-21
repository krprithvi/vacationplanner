from .tripattribute import TripAttribute
import re

class TravelDuration(TripAttribute):
    max = -float("inf")
    min = float("inf")
    parameter = "travelDuration"
    type = "Leg"

    def __init__(self, weight):
        self.weight = float(weight)

    def parsingInstruction(self, object):
        try:
            travelDuration = object
            hours_minutes_regex = re.compile('\d+')
            time = hours_minutes_regex.findall(travelDuration)
            if len(time) == 2:
                hours, minutes = time
                totalminutes = int(hours)*60 + int(minutes)
            elif 'H' in travelDuration:
                totalminutes = int(time[0])*60
            elif 'M' in travelDuration:
                totalminutes = int(time[0])
            else:
                totalminutes = 30

            if totalminutes > self.max:
                self.max = totalminutes
            if totalminutes < self.min:
                self.min = totalminutes
        except Exception as e:
            print("Travel Duration Parsing Instruction - " + str(e))


    def rate(self, object):
        try:
            travelDuration = object
            hours_minutes_regex = re.compile('\d+')
            time = hours_minutes_regex.findall(travelDuration)
            if len(time) == 2:
                hours, minutes = time
                totalminutes = int(hours)*60 + int(minutes)
            elif 'H' in travelDuration:
                totalminutes = int(time[0])*60
            elif 'M' in travelDuration:
                totalminutes = int(time[0])
            else:
                totalminutes = 30

            if self.max == self.min:
                return 0.5
            return -(totalminutes - self.min) / (self.max - self.min)
        except Exception as e:
            print("Travel Duration Class - ", str(e))
            return 0.5