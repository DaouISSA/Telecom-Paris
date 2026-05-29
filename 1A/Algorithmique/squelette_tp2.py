from math import radians, cos, sin, asin, sqrt
from datetime import datetime,  timedelta

EARTH_RADIUS = 6371
lag_time= datetime(1,0,0)
class Position():
    def __init__(self, lat : float, long : float):
        self.lat = lat
        self.long = long
    def distance (self, other: 'Position'):
        lat1=radians(self.lat)
        lon1=radians(self.long)
        lat2=radians(other.lat)
        lon2=radians(other.long)
        dlat=lat2-lat1
        dlon=lon2-lon1
        return 2*EARTH_RADIUS*asin(sqrt(sin(dlat/2)**2+cos(lat1)*cos(lat2)*sin(dlon/2)**2))
    def time(self, other: 'Position', speed =20):
        t = self.distance(other)/speed
        hours = int(t)
        minutes= int((t-hours)*60)
        secondes= int(((t-hours)*60-minutes)*60)
        return timedelta(hours=hours, minutes=minutes, seconds=secondes)

    def __str__(self):
        return(f"({self.lat:.2f}N,{self.long:.2f}E)")

class Booking():
    def __init__(self, name : str, depart_time : 'datetime', 
                 from_pos : 'Position', to_pos : 'Position',eta:'datetime'):
        if (not isinstance(name, str) or
            not isinstance(depart_time, datetime) or
            not isinstance(from_pos, Position) or 
            not isinstance(to_pos, Position) or not isinstance(eta,datetime)):
            raise TypeError
        self.name = name
        self.depart_time = depart_time
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.eta=eta
    def __str__(self):
        return("Booking by " + self.name +
               " at " + self.depart_time.strftime('%H:%M') +
               " from " + str(self.from_pos) +
               " to " + str(self.to_pos)
               )

class Planning():
    def __init__(self):
        self.bookings = [] 
        self.taxis = []
    def add_booking(self, b : 'Booking'):
        if isinstance(b, Booking):
            self.bookings.append(b)
        else:
            raise(TypeError('Was expecting a booking.'))
    def assign(self, t : int, b : 'Booking'):
        if t<len(self.taxis):
            self.taxis[t].append(b)
        else:
            for i in range(len(self.taxis),t+1):
                self.taxis.append([])
            self.taxis[t].append(b)
    def dummy_assign(self):
            for i in range(len(self.bookings)):
                self.assign(i,self.bookings[i])
    def greedy_assign(self):
        events=[]
        free_taxis=[]
        for b in self.bookings:
            events.append(b.depart_time,1,b)
            events.append(b.eta+lag_time,0,b)
        events.sort()
        for e in events:
            if e[1]==0:
                free_taxis.append(e[2].taxi)
            
            elif free_taxis==[]:
                    self.assign(len(self.taxis),b)
            else: 
                self.assign(free_taxis.pop(0),b)
    def neighbours(self,b0):
        neighbours = []
        for b in self.bookings:
            if b != b0 and b.depart_time >= b0.eta + lag_time:
                 neighbours.append(b)
        return neighbours
    def matching_init(self):
        for b in self.bookings:
            b.nextbooking = None
            b.prevbooking = None
    def match(self, b0, b1):





        

    def show_requests(self):
        print("List of requests :")
        for b in self.bookings:
            print(b)
    def show_planning(self):
        print("So far, the planning is :")
        for t in range(len(self.taxis)):
            print("Taxi "+str(t)+" handles:")
            for b in self.taxis[t]:
                print(b)
    def assign(self, t : int, b : 'Booking'):
        pass
    def dummy_assign(self):
        pass
    def greedy_assign(self):
        pass
    def _neighbours(self, b0 : 'Booking'):
        pass
    def _matching_init(self):
        pass
    def _match(self, b0 : 'Booking', b1 : 'Booking'):
        pass
    def _mark(self):
        pass
    def _assign_from_mark(self):
        pass
    def _find_augmenting_from(self, b0, seen, parent):
        pass
    def _find_augmenting(self):
        pass
    def _unmatch(self, b0 : 'Booking', b1 : 'Booking'):
        pass
    def _augment(self, b1, parent):
        pass
    def optimal_assign(self):
        pass

b = dict()

b[1] = Booking("Ada", 
             datetime(2024, 12, 10, 4, 5, 6), 
             Position(48.83206, 2.354888),
             Position(48.86919, 2.309913)
             )
b[2] = Booking("Ben", 
             datetime(2024, 12, 10, 5, 41, 6), 
             Position(48.83757, 2.295798),
             Position(48.73046, 2.367687)
             )
b[3] = Booking("Cal", 
             datetime(2024, 12, 10, 6, 55, 6), 
             Position(48.946404, 2.248097),
             Position(48.8935, 2.25565)
             )
b[4] = Booking("Dan", 
             datetime(2024, 12, 10, 7, 5, 6), 
             Position(48.81832002807286, 2.3908653944064557),
             Position(48.738172082852984, 2.474925295508417)
             )
b[5] = Booking("Eli", 
             datetime(2024, 12, 10, 7, 12, 43), 
             Position(48.854274193964265, 2.4367083553192446),
             Position(48.70988072820906, 2.294819770462278)
             )
b[6] = Booking("Flo", 
             datetime(2024, 12, 10, 7, 37, 17), 
             Position(48.713383700549215, 2.2698822374893193),
             Position(48.72458724724252, 2.1647614867901006)
             )
b[7] = Booking("Gio", 
             datetime(2024, 12, 10, 9, 5, 6), 
             Position(48.86686440098213, 2.1766408138886457),
             Position(48.8803149111712, 2.451501813427641)
             )
b[8] = Booking("Han", 
             datetime(2024, 12, 10, 12, 46, 12), 
             Position(48.72443183957998, 2.365251549588879),
             Position(48.79618976601188, 2.109938461062178)

             )
b[9] = Booking("Ida", 
             datetime(2024, 12, 10, 12, 44, 29), 
             Position(48.83206, 2.354888),
             Position(48.86919, 2.309913)
             )
b[10] = Booking("Jul", 
             datetime(2024, 12, 10, 13, 25, 28), 
             Position(48.81054397472843, 2.3675140905488417),
             Position(48.87357592953463, 2.2887154582135736)
             )
b[11] = Booking("Kei", 
             datetime(2024, 12, 10, 18, 7, 0), 
             Position(48.7273774339021, 2.2744772485109395),
             Position(48.759422368586175, 2.293036544999312)
             )
b[12] = Booking("Luc", 
             datetime(2024, 12, 10, 19, 5, 49), 
             Position(48.813214671560046, 2.3768328137872747),
             Position(48.78519983902859, 2.2464137091921716)
             )
b[13] = Booking("Moh", 
             datetime(2024, 12, 10, 19, 13, 0), 
             Position(48.73578618298117, 2.18893731471201),
             Position(48.73162506176087, 2.180663218189613)
             )
b[14] = Booking("Nik", 
             datetime(2024, 12, 10, 19, 19, 36), 
             Position(48.81466537389353, 2.328403489088749),
             Position(48.779673878136656, 2.3840547889374952)
             )

if __name__ == "__main__":
    # Pour le moment, voici quelques exemples d'utilisation des fonctions
    P = Planning()
    P.taxis = [[b[1]], [b[4],b[7],b[10]]]
    for i in range(1,15):
        P.add_booking(b[i])
    P.show_requests()
    P.show_planning()

