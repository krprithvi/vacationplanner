import abc

class TripAttribute(metaclass=abc.ABCMeta):
    weight = 0
    # All attributes should return a value between 0 and 1
    @abc.abstractmethod
    def rate(self):
        pass
