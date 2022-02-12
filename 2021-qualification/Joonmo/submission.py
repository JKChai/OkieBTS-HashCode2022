from collections import defaultdict
from queue import PriorityQueue
import sys
import textwrap

class InputValue:
    debug1 = False
    debug2 = False
    
    durationOfSim               = None
    numberOfIntersections       = None
    numberOfStreets             = None
    numberOfCars                = None
    bonusPoint                  = None
    inputFile                   = None
    
    intersectionDirect          = defaultdict(list)
    streetInfo                  = defaultdict(dict)
    carInfo                     = defaultdict(dict)
    
    IntersectionInfo = defaultdict(list)
    exitcars = []
    greenlightInfo = defaultdict(list)
    def __init__(self):
       pass

        
    def readText(self):
        self.inputFile = open("2021-qualification\Joonmo\input\\a.txt","r")
        firstline = self.inputFile.readline().split()
        self.durationOfSim               = firstline[0]
        self.numberOfIntersections       = firstline[1]
        self.numberOfStreets             = firstline[2]
        self.numberOfCars                = firstline[3]
        self.bonusPoint                  = firstline[4]
        if self.debug1:
            print(
            f"""
            The simulation lasts {self.durationOfSim } seconds, there are {self.numberOfIntersections}
            intersections, {self.numberOfStreets} streets, and {self.numberOfCars} cars; and a car
            scores 1000 points for reaching the destination
            on time.""")

    def makeDict(self):
        # line readings of numberOfStreets
        for i in range(int(self.numberOfStreets)):
            line = self.inputFile.readline().split()
            startIntersectionOfStreet  = line[0]
            endIntersectionOfStreet     = line[1]
            streetName                  = line[2]
            timeToEndStreet             = int(line[3])

            
            self.intersectionDirect[startIntersectionOfStreet].append(endIntersectionOfStreet)
            # self.streetInfo[self.streetName] = (listOfMovingCars,
            #                                     startIntersectionOfStreet,
            #                                     endIntersectionOfStreet,
            #                                       timeToEndStreet)
            self.streetInfo[streetName]["listOfMovingCars"] = []
            self.streetInfo[streetName]["startIntersectionOfStreet"] = startIntersectionOfStreet
            self.streetInfo[streetName]["endIntersectionOfStreet"] = endIntersectionOfStreet
            self.streetInfo[streetName]["timeToEndStreet"] = timeToEndStreet
            self.streetInfo[streetName]["listOfWaitingCars"] = []
            if self.debug1:
                print(f"""
                    Street {streetName} starts at intersection {startIntersectionOfStreet},
                    ends at {endIntersectionOfStreet}, and it takes L={timeToEndStreet} seconds to go from
                    the beginning to the end""")

        
        # line readings of numberOfCars
        for carNumber in range(int(self.numberOfCars)):
            line = self.inputFile.readline().split()
            numberOfStreetsForCar = line[0]
            listOfStreetsGiven = line[1:]
            firstStreet = listOfStreetsGiven[0]
            secondStreet = listOfStreetsGiven[1]
            listOfStreetsToPass = listOfStreetsGiven[1:]
            
            carStartingIntersection = self.streetInfo[firstStreet]["endIntersectionOfStreet"]
            
            totalTimeLeft = 0
            for streetName in listOfStreetsToPass:
                timeToEndStreet = int(self.streetInfo[streetName]["timeToEndStreet"])
                totalTimeLeft += timeToEndStreet

            self.carInfo[carNumber]["currentStreet"] = firstStreet
            self.carInfo[carNumber]["totalTimeLeft"] = totalTimeLeft
            self.carInfo[carNumber]["currentTimeLeft"] = 0
            self.carInfo[carNumber]["carStartingIntersection"] = carStartingIntersection
            self.carInfo[carNumber]["listOfStreetsToPass"] = listOfStreetsToPass
            self.streetInfo[firstStreet]["listOfWaitingCars"].append(carNumber)
            
            
            if self.debug1:
                print(f"""
                    The first car starts at the end of
                    {firstStreet} and then follows the given path""")
            
        
        self.inputFile.close() 

    def algoSoultion(self):
        carList = [*range(int(self.numberOfCars))]
        
        
        for D in range(1, int(self.durationOfSim)+1):
            frontLineCars = []
            
            for car in carList:
                
                # is this car at first line in the intersection?
                currentStreet = self.carInfo[car]["currentStreet"]
                if (not self.streetInfo[currentStreet]["listOfWaitingCars"]):
                    pass
                elif (car == self.streetInfo[currentStreet]["listOfWaitingCars"][0]):
                    
                    frontLineCars.append(car)
            
            
            # q = PriorityQueue()
            for car in frontLineCars:
                
                # is this car is smallest time in the intersection?
                currentStreet = self.carInfo[car]["currentStreet"]
                currentFacingInter = self.streetInfo[currentStreet]["endIntersectionOfStreet"]
                self.IntersectionInfo[currentFacingInter].append((self.carInfo[car]["totalTimeLeft"], car))
                self.IntersectionInfo[currentFacingInter].sort(key = lambda x :x[0])
                
            # give greenlight to street at intersection
            if not frontLineCars:
                pass
            else:
                carsCrossed = set()
                for inter, carPQ in self.IntersectionInfo.items():
                    # (totaltimeleft, car)
                    car = carPQ[0][1]
                    carsCrossed.add(car)
                    if self.carInfo[car]["listOfStreetsToPass"]:
                        streetToPass = self.carInfo[car]["listOfStreetsToPass"][0]
                    else:
                        pass
                    self.greenlightInfo[inter].append((streetToPass, D))
            
            # update car
            for car in carList:
                # if car got green light
                if car in carsCrossed:
                    # new street
                    currentStreet = self.carInfo[car]["currentStreet"]
                    if self.streetInfo[currentStreet]["listOfWaitingCars"]:
                        self.streetInfo[currentStreet]["listOfWaitingCars"].pop(0)
                    if self.carInfo[car]["listOfStreetsToPass"]:
                        streetToPass = self.carInfo[car]["listOfStreetsToPass"].pop(0)
                        self.carInfo[car]["currentStreet"] = streetToPass
                        self.streetInfo[streetToPass]["listOfMovingCars"].append(car)
                        # Assign new street time
                        self.carInfo[car]["currentTimeLeft"] = self.streetInfo[streetToPass]["timeToEndStreet"]
                    self.carInfo[car]["totalTimeLeft"] = self.carInfo[car]["totalTimeLeft"] -1
                # other cars did not get green light
                else:
                    currentStreet =  self.carInfo[car]["currentStreet"]
                    listOfMovingCars = self.streetInfo[currentStreet]["listOfMovingCars"]
                    # check this is car is moving list
                    if car in listOfMovingCars:
                        self.carInfo[car]["totalTimeLeft"] = self.carInfo[car]["totalTimeLeft"] - 1
                        self.carInfo[car]["currentTimeLeft"] = self.carInfo[car]["currentTimeLeft"] -1
                    
                # check reach final or end of street
                if self.carInfo[car]["totalTimeLeft"] == 0:
                    self.exitcars.append((car, D))
                    carList.remove(car)
                    
                    
                    
                    
                elif self.carInfo[car]["currentTimeLeft"] == 0:
                    currentStreet =  self.carInfo[car]["currentStreet"]
                    if car in  self.streetInfo[currentStreet]["listOfMovingCars"]:
                        self.streetInfo[currentStreet]["listOfMovingCars"].remove(car)
                    self.streetInfo[currentStreet]["listOfWaitingCars"].append(car)
                    
             
            if self.debug2:
                
                print(f"=========D:{D}===============")
                
                for key, value in list(self.carInfo.items()):
                    if key == 0:
                        print("Car:", key)
                        for key2, valueinner in list(value.items()):
                            print(f"{key2}: {valueinner}")
                print(f"====={carList}===============")
                print(f"=============================")
                   

        return
    
    def gradingSim():
        pass




  
def main():
    taskobj =InputValue()
    taskobj.readText()
    taskobj.makeDict()
    taskobj.algoSoultion()
    print(taskobj.greenlightInfo)
    print(taskobj.exitcars)
    
  
if __name__=="__main__":
    main()



# # =========Simulation==============

# greenLightAt = defaultdict(list)
# movingCarsInfo = dict()
# carsExit = list()

# for D in range(1, int(durationOfSim)+1):
    
    
            
#     # print(intersectionStatus.items())
    
    
#     # each intersectionNum and cars are waiting on the line
#     for intersectionNum, carNumbers in intersectionStatus.items():
#         # nestedListOfStreet = car_streets_dict[intersectionNum]
#         # from this intersectionNum, street orderd list
#         # cars in this intersectionNum
        
#         # if carNumbers is empty
#         if not carNumbers:
#             continue
        
#         else:
#             minTimeForCar = sys.maxsize
#             minTimeCarNum = None
#             streetFirstCarTook = set()
#             # loop cars in intersection
            
                
            
            
#             for carNumber in carNumbers:
#                 # do not take cars behind, which has same direction
#                 # and check minimum time car
#                 if not infoOfCar[carNumber][1]:
#                     continue
#                 else:
#                     currentStreetToPass = infoOfCar[carNumber][1][0]
#                     if infoOfCar[carNumber][2] < minTimeForCar and  currentStreetToPass not in streetFirstCarTook:
#                         minTimeCarNum = carNumber
#                         minTimeForCar =  infoOfCar[carNumber][2]
#                         streetFirstCarTook.add(currentStreetToPass)

#             # take and remove first street name from list of streets to pass
#             if minTimeCarNum is None:
#                 break
#             else:
#                 streetToPass = infoOfCar[minTimeCarNum][1].pop(0)
            
            
            
#             # green light for this min car's street
#             greenLightAt[intersectionNum].append((streetToPass, D))
            
            
#             # remove car from intersectionNum
#             intersectionStatus[intersectionNum].remove(minTimeCarNum)
            
#             # make minTimeCarNum on going in the street,
#             timeOnStreet = infoOfCar[minTimeCarNum][3]
#             onGoingstreetName = streetToPass
#             movingCarsInfo[minTimeCarNum] = [onGoingstreetName, timeOnStreet]
            
           
#     # update moving cars and intersection
#     # print(movingCarsInfo)
#     for carNum, info in list(movingCarsInfo.items()):

#         info[1] = info[1] - 1
#         infoOfCar[carNum][2] = infoOfCar[carNum][2] - 1
#         timeOnStreet = info[1]
#         totalTimeLeft = infoOfCar[carNum][2]
#         # if total time is up, car exit 
#         if totalTimeLeft == 0:
#             carsExit.append((carNum, D))
#             del movingCarsInfo[carNum]
#         # if time is up, enter intersection
#         elif timeOnStreet == 0:
#             onGoingstreetName = info[0]
#             endIntersectionOfStreet = infoOfStreet[onGoingstreetName][1]
#             intersectionStatus[endIntersectionOfStreet].append(carNum)


# print("Car Exit: ", carsExit)
# print("Green light", greenLightAt)
# file1 = open("MyFile.txt", "w") 

# outputIntersections = list(greenLightAt.keys())
# file1.write(str(len(outputIntersections)))
# file1.write("\n")
# for inter in outputIntersections:
#     file1.write(inter)
#     file1.write("\n")
#     numOfIncomingStreets = len(greenLightAt[inter])
#     file1.write(str(numOfIncomingStreets))
#     file1.write("\n")
#     time = 0
#     for street, iter in greenLightAt[inter]:
#         file1.write(street)
#         file1.write(" ")
#         file1.write(str(iter - time))
#         file1.write("\n")
#         time = iter
# file1.close()


