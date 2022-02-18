from collections import defaultdict
from queue import PriorityQueue
import sys
import textwrap





class StreetInfo:
    def __init__(self):
        self.streetName = ""
        self.listOfMovingCars = []
        self.startIntersectionOfStreet = None
        self.endIntersectionOfStreet = None
        self.timeToEndStreet = None
        self.listOfWaitingCars = []
        
class CarInfo:
    def __init__(self):
        self.carNumber = None
        self.currentStreet = None
        self.totalTimeLeft = None
        self.currentTimeLeft = None
        self.carStartingIntersection = None
        self.listOfStreetsToPass = None
    

        
    
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
    
    
    for D in range(1, int(durationOfSim)+1):
        if debug2:
            
            print(f"=========Start D:{D}===============")
            print(f"=============================")
           
        frontLineCars = []
        
        for car in carList:
            
            # is this car at first line in the intersection?
            currentStreet = carDict[car].currentStreet
            if debug2:
                print(f"Waiting list of cars on {currentStreet}:",
                    streetDict[currentStreet].listOfWaitingCars)
            if (not streetDict[currentStreet].listOfWaitingCars):
                pass
            elif (car == streetDict[currentStreet].listOfWaitingCars[0]):
                frontLineCars.append(car)
        
        
        # add in list and sort
        for car in frontLineCars:
            
            # is this car is smallest time in the intersection?
            currentStreet = carDict[car].currentStreet
            currentFacingInter = streetDict[currentStreet].endIntersectionOfStreet
            IntersectionInfo[currentFacingInter].append((carDict[car].totalTimeLeft, car))
            # sort time left
            IntersectionInfo[currentFacingInter].sort(key = lambda x :x[0])
            if debug2:
                
                print("Sorted car list: ",IntersectionInfo[currentFacingInter])
                print("Sorted car list: ",IntersectionInfo[currentFacingInter])
                
        # give greenlight to street at intersection
        
        carsCrossed = set()
        if not frontLineCars:
            pass
        else:
            
            for inter, carPQ in IntersectionInfo.items():
                # (totaltimeleft, car)
                
                car = carPQ[0][1]
                carsCrossed.add(car)
                if carDict[car].listOfStreetsToPass:
                    streetToPass = carDict[car].listOfStreetsToPass[0]
                else:
                    pass
                
                
                greenlightInfo[inter].append((streetToPass, D))
                if debug2:
                    print("green Light Info: ", greenlightInfo[inter])
        
        # update car
        for car in carList:
            
            
            # if car got green light
            if car in carsCrossed:
                # new street
                currentStreet = carDict[car].currentStreet
                if streetDict[currentStreet].listOfWaitingCars:
                    streetDict[currentStreet].listOfWaitingCars.pop(0)
                
                    
                if carDict[car].listOfStreetsToPass:
                    streetToPass = carDict[car].listOfStreetsToPass.pop(0)
                    carDict[car].currentStreet = streetToPass
                    streetDict[streetToPass].listOfMovingCars.append(car)
                    # Assign new street time
                    carDict[car].currentTimeLeft = streetDict[streetToPass].timeToEndStreet
                
                carDict[car].totalTimeLeft = carDict[car].totalTimeLeft -1
            
            # other cars did not get green light
            else:
                currentStreet =  carDict[car].currentStreet
                listOfMovingCars = streetDict[currentStreet].listOfMovingCars
                # check this is car is moving list
                if car in listOfMovingCars:
                    carDict[car].totalTimeLeft = carDict[car].totalTimeLeft - 1
                    carDict[car].currentTimeLeft = carDict[car].currentTimeLeft -1
                
            # check reach final or end of street
            if carDict[car].totalTimeLeft == 0:
                exitcars.append((car, D))
                carList.remove(car)
                
                
                
                
            elif carDict[car].currentTimeLeft == 0:
                currentStreet =  carDict[car].currentStreet
                if car in  streetDict[currentStreet].listOfMovingCars:
                    streetDict[currentStreet].listOfMovingCars.remove(car)
                streetDict[currentStreet].listOfWaitingCars.append(car)
                
            
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

