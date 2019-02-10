class Measurements:
    def __init__(self, id, timestamp, failure, measures):
        self.id = id
        self.timestamp= timestamp
        self.failure = failure
        self.measures = []