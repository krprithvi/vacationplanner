import re


class Leg:
    segments = None
    travelDuration = None
    travelDurationHours = None
    travelDurationMinutes = None

    def __init__(self, segments, travelDuration):
        self.segments = segments
        self.travelDuration = travelDuration
        try:
            hours_minutes_regex = re.compile('\d+')
            time = hours_minutes_regex.findall(self.travelDuration)
            if len(time) == 2:
                self.travelDurationHours, self.travelDurationMinutes = time
            elif 'H' in travelDuration:
                self.travelDurationHours = time[0]
            elif 'M' in travelDuration:
                self.travelDurationMinutes = time[1]
        except Exception as e:
            print(str(e))
            self.travelDurationMinutes = "NA"
