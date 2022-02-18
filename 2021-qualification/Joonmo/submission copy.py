from collections import defaultdict
from queue import PriorityQueue
import sys
import textwrap





class StreetInfo:
    def __init__(self):
        self.streetName = ""
        self.startIntersectionOfStreet = None
        self.endIntersectionOfStreet = None
        self.timeToEndStreet = None
        self.listOfWaitingCars = []
        self.listOfMovingCars = []
        
class CarInfo:
    def __init__(self):
        self.carNumber = None
        self.currentStreet = None
        self.totalTimeLeft = None
        self.currentTimeLeft = 0
        self.carStartingIntersection = None
        self.isWaiting = None
        self.isMoving = None
        self.listOfStreetsToPass = []
    

        
    
class IntersectionInfo:
    def __init__(self):
        pass

def trafficSim():
    debug1 = False
    debug2 = True
    
    durationOfSim               = None
    numberOfIntersections       = None
    numberOfStreets             = None
    numberOfCars                = None
    bonusPoint                  = None
    inputFile                   = None

    intersectionDirect = defaultdict(list)
    IntersectionInfo = defaultdict(list)
    exitcars = []
    greenlightInfo = defaultdict(list)
    streetDict = dict()
    carDict = dict()
    
    inputFile = open("2021-qualification\Joonmo\input\\a.txt","r")
    firstline = inputFile.readline().split()
    durationOfSim               = firstline[0]
    numberOfIntersections       = firstline[1]
    numberOfStreets             = firstline[2]
    numberOfCars                = firstline[3]
    bonusPoint                  = firstline[4]
    if debug1:
        print(
        f"""
        The simulation lasts {durationOfSim } seconds, there are {numberOfIntersections}
        intersections, {numberOfStreets} streets, and {numberOfCars} cars; and a car
        scores 1000 points for reaching the destination
        on time.""")

    
    # line readings of numberOfStreets
    for i in range(int(numberOfStreets)):
        
        line = inputFile.readline().split()
        startIntersectionOfStreet  = line[0]
        endIntersectionOfStreet     = line[1]
        streetName                  = line[2]
        timeToEndStreet             = int(line[3])

        
        si_obj = StreetInfo()
        si_obj.streetName = streetName
        si_obj.timeToEndStreet = timeToEndStreet
        si_obj.endIntersectionOfStreet = endIntersectionOfStreet
        si_obj.startIntersectionOfStreet  = startIntersectionOfStreet

        streetDict[streetName] = si_obj
        

        intersectionDirect[startIntersectionOfStreet].append(endIntersectionOfStreet)
        
        
        # streetDict[streetName] = (listOfMovingCars,
        #                                     startIntersectionOfStreet,
        #                                     endIntersectionOfStreet,
        #                                       timeToEndStreet)
        # streetDict[streetName].listOfMovingCars = []
        # streetDict[streetName].startIntersectionOfStreet = startIntersectionOfStreet
        # streetDict[streetName].endIntersectionOfStreet = endIntersectionOfStreet
        # streetDict[streetName].timeToEndStreet = timeToEndStreet
        # streetDict[streetName].listOfWaitingCars = []
        if debug1:
            print(f"""
                Street {streetName} starts at intersection {startIntersectionOfStreet},
                ends at {endIntersectionOfStreet}, and it takes L={timeToEndStreet} seconds to go from
                the beginning to the end""")

        
        # line readings of numberOfCars
    for carNumber in range(int(numberOfCars)):
        line = inputFile.readline().split()
        numberOfStreetsForCar = line[0]
        listOfStreetsGiven = line[1:]
        firstStreet = listOfStreetsGiven[0]
        secondStreet = listOfStreetsGiven[1]
        listOfStreetsToPass = listOfStreetsGiven[1:]
        
        
        
        carStartingIntersection = streetDict[firstStreet].endIntersectionOfStreet
        
        totalTimeLeft = 0
        for streetName in listOfStreetsToPass:
            timeToEndStreet = int(streetDict[streetName].timeToEndStreet)
            totalTimeLeft += timeToEndStreet

        car_obj = CarInfo()
        car_obj.carNumber
        car_obj.currentStreet = firstStreet
        car_obj.totalTimeLeft = totalTimeLeft
        car_obj.carStartingIntersection = carStartingIntersection
        car_obj.listOfStreetsToPass = listOfStreetsToPass
        car_obj.isWaiting = True
        
        carDict[carNumber] = car_obj
        streetDict[firstStreet].listOfWaitingCars.append(carNumber)
        
        # carDict[carNumber].currentStreet = firstStreet
        # carDict[carNumber].totalTimeLeft = totalTimeLeft
        # carDict[carNumber].currentTimeLeft = 0
        # carDict[carNumber].carStartingIntersection = carStartingIntersection
        # carDict[carNumber].listOfStreetsToPass = listOfStreetsToPass
        # streetDict[firstStreet].listOfWaitingCars.append(carNumber)
        
        
        if debug1:
            print(f"""
                The first car starts at the end of
                {firstStreet} and then follows the given path""")
        
    
    inputFile.close() 

    
    carList = [*range(int(numberOfCars))]
    
    movingCars = []
    
    for D in range(0, int(durationOfSim)+1):
        if debug2:
            
            print(f"=========Start D:{D}===============")
            print(f"=============================")
        
        carsCrossed = set()
        frontLineCars = []
        for c in carList:
            # check if car is at front line
            if streetDict[carDict[c].currentStreet].listOfWaitingCars:
                if c == streetDict[carDict[c].currentStreet].listOfWaitingCars[0]:
                    frontLineCars.append(c)
        
        inter_car  = defaultdict(list)
        for c in frontLineCars:
            inter_car[carDict[c].carStartingIntersection].append((c, carDict[c].totalTimeLeft))
        
        carsCross = set()
        for intersection, cars in list(inter_car.items()):
            # print("intersection, cars")
            # print(f"{intersection, cars}")
            cars.sort(key= lambda x: x[1])
            greenlightInfo[intersection].append((carDict[cars[0][0]].currentStreet, D))
            carsCross.add(cars[0][0])
            movingCars.append(cars[0][0])
        
        
        print("Car Cross")
        print(carsCross)
        print("movingCars")
        print(movingCars)
        for c in movingCars:
            print(carDict[c].currentTimeLeft)
        # update else cars
        for c in movingCars:
            if c not in carsCross:
                carDict[c].currentTimeLeft = carDict[c].currentTimeLeft -1
                carDict[c].totalTimeLeft = carDict[c].totalTimeLeft - 1
                
                if carDict[c].totalTimeLeft <= 0:
                    exitcars.append((c, D))
                    carList.remove(c)
                    movingCars.remove(c)
                    
                elif carDict[c].currentTimeLeft <= 0:
                    streetDict[carDict[c].currentStreet].listOfWaitingCars.append(c)
                    streetDict[carDict[c].currentStreet].listOfMovingCars.remove(c)
                    movingCars.remove(c)
        
        # update carCross
        for c in carsCross:
            streetDict[carDict[c].currentStreet].listOfWaitingCars.pop(0)
            carDict[c].currentStreet = carDict[c].listOfStreetsToPass.pop(0)
            carDict[c].currentTimeLeft = streetDict[carDict[c].currentStreet].timeToEndStreet - 1
            carDict[c].totalTimeLeft = carDict[c].totalTimeLeft - 1
            carDict[c].carStartingIntersection =  streetDict[carDict[c].currentStreet].endIntersectionOfStreet
            streetDict[carDict[c].currentStreet].listOfMovingCars.append(c)
        
        
        
        if debug2:
            print(f"=========END D:{D}===============")
            print(f"=============================")
            
            
    print("greenlightInfo[inter].append((streetToPass, D))")
    print(greenlightInfo.items())
    print(exitcars)
    return
    
    def gradingSim():
        pass




  
def main():
    trafficSim()
    
    
  
if __name__=="__main__":
    main()

