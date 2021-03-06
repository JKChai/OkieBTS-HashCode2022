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
        self.queue = []
        
class CarInfo:
    def __init__(self):
        self.carNumber = None
        self.currentStreet = None
        self.totalTimeLeft = None
        self.currentTimeLeft = 0
        self.carFacingIntersection = None
        self.isWaiting = None

        self.listOfStreetsToPass = []
    

        
    
class IntersectionInfo:
    def __init__(self):
        pass

def trafficSim():
    debug1 = False
    debug2 = False
    debug3 = False
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
        
        
        
        carFacingIntersection = streetDict[firstStreet].endIntersectionOfStreet
        
        totalTimeLeft = 0
        for streetName in listOfStreetsToPass:
            timeToEndStreet = int(streetDict[streetName].timeToEndStreet)
            totalTimeLeft += timeToEndStreet

        car_obj = CarInfo()
        car_obj.carNumber
        car_obj.currentStreet = firstStreet
        car_obj.totalTimeLeft = totalTimeLeft
        car_obj.carFacingIntersection = carFacingIntersection
        car_obj.listOfStreetsToPass = listOfStreetsToPass
        car_obj.isWaiting = True
        carDict[carNumber] = car_obj
        streetDict[firstStreet].queue.append(carNumber)
        # streetDict[firstStreet].listOfWaitingCars.append(carNumber)
        

        if debug1:
            print(f"""
                The first car starts at the end of
                {firstStreet} and then follows the given path""")
        
    
    inputFile.close() 

    
    carList = [*range(int(numberOfCars))]
    
    movingCars = []
    
    for D in range(0, int(durationOfSim)):
        
        
        if debug2:
            print(f"=========Start D:{D}===============")
            print(f"=============================")
        
        # iter car and find front line car
        frontLineCars = []
        
        
        for c in carList:
            # front car
            if debug2:
                print(streetDict[carDict[c].currentStreet].queue[0])
                
            if c == streetDict[carDict[c].currentStreet].queue[0]:
                
                
                if not carDict[c].listOfStreetsToPass:
                    
                    if debug3:
                         print(f"HERE")
                         
                    carList.remove(c)
                    exitcars.append((c, D))
                    
                elif carDict[c].isWaiting:
                    frontLineCars.append(c)

        # iter front car and collect cars in intersection sort cars
        intersectionDict = defaultdict(list)
        for c in frontLineCars:
            intersectionDict[carDict[c].carFacingIntersection].append((c, carDict[c].totalTimeLeft))
        
        # sort cars in each intersection to find smallest total time
        # give greenlight to smallest total time car
        carCrossed = set()
        for inter in intersectionDict.keys():
            intersectionDict[inter].sort(key = lambda x: x[1])
            smallestCar = intersectionDict[inter][0][0]
            # append greenlight dict
            greenlightInfo[inter].append((carDict[smallestCar].currentStreet, D))
            carCrossed.add(smallestCar)
        
  
        # update cars

        #For cars crossed,
        for c in carCrossed:
            #  update waiting status
            carDict[c].isWaiting = False
            # deqeue car in street
            streetDict[carDict[c].currentStreet].queue.pop(0)
            # change car street to pass
            carDict[c].currentStreet = carDict[c].listOfStreetsToPass.pop(0)
            
            # change intersection to face
            
            carDict[c].carFacingIntersection = streetDict[carDict[c].currentStreet].endIntersectionOfStreet
            
            streetDict[carDict[c].currentStreet].queue.append(c)

            carDict[c].currentTimeLeft = streetDict[carDict[c].currentStreet].timeToEndStreet
            
            movingCars.append(c)
        
        # for moving car
        for c in movingCars:
            # if c not in carCrossed:
                
            carDict[c].currentTimeLeft = carDict[c].currentTimeLeft -1
            if debug2:
                        print(carDict[c].listOfStreetsToPass)
                        print("Time left: ",carDict[c].currentTimeLeft)
            if carDict[c].currentTimeLeft == 0:
                carDict[c].isWaiting = True
                movingCars.remove(c)
        
        if debug2:
            print(f"=========END D:{D}===============")
            print(f"=============================")
            
            
    print("greenlightInfo[inter].append((streetToPass, D))")
    print(greenlightInfo.items())
    file1 = open("output.csv", "w+")
    outputIntersections = list(greenlightInfo.keys())
    file1.write(str(len(outputIntersections)))
    file1.write("\n")
    for inter in outputIntersections:
        file1.write(inter)
        file1.write("\n")
        numOfIncomingStreets = len(greenlightInfo[inter])
        file1.write(str(numOfIncomingStreets))
        file1.write("\n")
        time = 0
        currentStreet = None
        for street, iter in greenlightInfo[inter]:

    
            file1.write(street)
            file1.write(" ")
            file1.write(str(iter - time))
            file1.write("\n")
            time = iter
    file1.close()

    
    
    print(exitcars)
    return
    
    def gradingSim():
        pass




  
def main():
    trafficSim()
    
    
  
if __name__=="__main__":
    main()

