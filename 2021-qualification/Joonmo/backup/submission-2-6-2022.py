from collections import defaultdict
from queue import PriorityQueue
import sys

file1 = open("2021-qualification\Joonmo\input\\f.txt","r")
# print(file1.read()) 


# reading of first line
firstline = file1.readline().split()
# print(firstline.split())

# D
durationOfSim               = firstline[0]
numberOfIntersections       = firstline[1]
numberOfStreets             = firstline[2]
numberOfCars                = firstline[3]
bonusPoint                  = firstline[4]

print(f"""
The simulation lasts {durationOfSim } seconds, there are {numberOfIntersections}
intersections, {numberOfStreets} streets, and {numberOfCars} cars; and a car
scores 1000 points for reaching the destination
on time.
        """)

# hash table ==> car1 as key, list of street as value
car_streets_dict = defaultdict(list)

# hash table ==> nameOfStreet as key, tuple of startIntersectionOfStreet, endIntersectionOfStreet, timeToEndStreet
infoOfStreet = dict()

# hash table ==> startIntersectionOfStreet as key,  list of endIntersectionOfStreet as value
start_end_dict = defaultdict(list)

# hash table ==> startIntersectionOfStreet as key, list of car
inter_car_dict = defaultdict(list)

intersectionStatus = defaultdict(list)
# line readings of numberOfStreets
for i in range(int(numberOfStreets)):
    line = file1.readline().split()
    startIntersectionOfStreet = line[0]
    endIntersectionOfStreet = line[1]
    streetName = line[2]
    timeToEndStreet = line[3]
    
    infoOfStreet[streetName] = (startIntersectionOfStreet, endIntersectionOfStreet, timeToEndStreet)
    start_end_dict[startIntersectionOfStreet].append(endIntersectionOfStreet) 
    print(f"""
Street {streetName} starts at intersection {startIntersectionOfStreet},
ends at {endIntersectionOfStreet}, and it takes L={timeToEndStreet} seconds to go from
the beginning to the end""")
  



car_order = list()
remain_street =  dict()
infoOfCar = dict()
# line readings of numberOfCars
for carNumber in range(int(numberOfCars)):
    line = file1.readline().split()
    numberOfStreet = line[0]
    listOfStreetToPass = line[1:]
    # We want to know order of car with intersectionNum in case cars are in same intersectionNum
    firstStreet = listOfStreetToPass[0]
    startStreet = listOfStreetToPass[1]
    timeOnStreet = int(infoOfStreet[startStreet][2])
    minTimeForCar = sys.maxsize
    totalTimeLeft = 0
    timeCounter = 0
    for streetName in listOfStreetToPass[1:]:
        timeToEndStreet = int(infoOfStreet[streetName][2])
        totalTimeLeft += timeToEndStreet
    
    endIntersectionOfStreet = infoOfStreet[firstStreet][1]
    
    infoOfCar[carNumber] = [
        endIntersectionOfStreet,
        listOfStreetToPass[1:],
        totalTimeLeft,
        timeOnStreet]
    
    intersectionStatus[endIntersectionOfStreet].append(carNumber)
    print(f"""
The first car starts at the end of
{firstStreet} and then follows the given path""")
    
file1.close() 

# =========Simulation==============

greenLightAt = defaultdict(list)
movingCarsInfo = dict()
carsExit = list()

for D in range(1, int(durationOfSim)+1):
    
    
            
    # print(intersectionStatus.items())
    
    
    # each intersectionNum and cars are waiting on the line
    for intersectionNum, carNumbers in intersectionStatus.items():
        # nestedListOfStreet = car_streets_dict[intersectionNum]
        # from this intersectionNum, street orderd list
        # cars in this intersectionNum
        
        # if carNumbers is empty
        if not carNumbers:
            continue
        
        else:
            minTimeForCar = sys.maxsize
            minTimeCarNum = None
            streetFirstCarTook = set()
            # loop cars in intersection
            
                
            
            
            for carNumber in carNumbers:
                # do not take cars behind, which has same direction
                # and check minimum time car
                if not infoOfCar[carNumber][1]:
                    continue
                else:
                    currentStreetToPass = infoOfCar[carNumber][1][0]
                    if infoOfCar[carNumber][2] < minTimeForCar and  currentStreetToPass not in streetFirstCarTook:
                        minTimeCarNum = carNumber
                        minTimeForCar =  infoOfCar[carNumber][2]
                        streetFirstCarTook.add(currentStreetToPass)

            # take and remove first street name from list of streets to pass
            if minTimeCarNum is None:
                break
            else:
                streetToPass = infoOfCar[minTimeCarNum][1].pop(0)
            
            
            
            # green light for this min car's street
            greenLightAt[intersectionNum].append((streetToPass, D))
            
            
            # remove car from intersectionNum
            intersectionStatus[intersectionNum].remove(minTimeCarNum)
            
            # make minTimeCarNum on going in the street,
            timeOnStreet = infoOfCar[minTimeCarNum][3]
            onGoingstreetName = streetToPass
            movingCarsInfo[minTimeCarNum] = [onGoingstreetName, timeOnStreet]
            
           
    # update moving cars and intersection
    # print(movingCarsInfo)
    for carNum, info in list(movingCarsInfo.items()):

        info[1] = info[1] - 1
        infoOfCar[carNum][2] = infoOfCar[carNum][2] - 1
        timeOnStreet = info[1]
        totalTimeLeft = infoOfCar[carNum][2]
        # if total time is up, car exit 
        if totalTimeLeft == 0:
            carsExit.append((carNum, D))
            del movingCarsInfo[carNum]
        # if time is up, enter intersection
        elif timeOnStreet == 0:
            onGoingstreetName = info[0]
            endIntersectionOfStreet = infoOfStreet[onGoingstreetName][1]
            intersectionStatus[endIntersectionOfStreet].append(carNum)


print("Car Exit: ", carsExit)
print("Green light", greenLightAt)
file1 = open("MyFile.txt", "w") 

outputIntersections = list(greenLightAt.keys())
file1.write(str(len(outputIntersections)))
file1.write("\n")
for inter in outputIntersections:
    file1.write(inter)
    file1.write("\n")
    numOfIncomingStreets = len(greenLightAt[inter])
    file1.write(str(numOfIncomingStreets))
    file1.write("\n")
    time = 0
    for street, iter in greenLightAt[inter]:
        file1.write(street)
        file1.write(" ")
        file1.write(str(iter - time))
        file1.write("\n")
        time = iter
file1.close() 