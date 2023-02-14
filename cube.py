class Cube:
    def __init__(self, coords, distance):
        self.coords = coords
        self.distance = distance
        self.prev = None
    

    def setPrevious(self, coords):
        self.prev = coords