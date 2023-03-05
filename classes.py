class selectedPlanes:
    def __init__(self,name,lat,lon,distance,altitude,speed,heading,planeType,registration,timestamp):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.distance = distance
        self.altitude = altitude
        self.speed = speed
        self.type = planeType
        self.registration = registration
        self.heading = heading
        self.timestamp = timestamp

class updatedGeomatis:
    def __init__(self,distance,altAngle,dirAngle):
        self.distance = distance
        self.altAngle = altAngle
        self.dirAngle = dirAngle
