class Measurements:
    def __init__(self, timestamp, failure, volts, amperes, kWh):
        self.timestamp= timestamp
        self.failure = failure
        self.volts = volts
        self.amperes = amperes
        self.kWh = kWh