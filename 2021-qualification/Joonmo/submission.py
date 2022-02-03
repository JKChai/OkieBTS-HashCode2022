from collections import defaultdict
from queue import PriorityQueue

file1 = open("input/f.txt","r+")
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


# hash table ==> car1 as key, list of street as value
car_streets_dict = defaultdict(list)

# hash table ==> nameOfStreet as key, tuple of startIntersectionOfStreet, endIntersectionOfStreet, timeToEndStreet
street_prop_dict = defaultdict(list)

# hash table ==> startIntersectionOfStreet as key,  list of endIntersectionOfStreet as value
start_end_dict = defaultdict(list)

# hash table ==> startIntersectionOfStreet as key, list of car
inter_car_dict = defaultdict(list)

# line readings of numberOfStreets
for i in range(int(numberOfStreets)):
    line = file1.readline().split()
    startIntersectionOfStreet = line[0]
    endIntersectionOfStreet = line[1]
    nameOfStreet = line[2]
    timeToEndStreet = line[3]

    street_prop_dict[nameOfStreet].append([startIntersectionOfStreet, endIntersectionOfStreet, timeToEndStreet])
    start_end_dict[startIntersectionOfStreet].append(endIntersectionOfStreet)

car_order = list()
remain_street =  dict()
# line readings of numberOfCars
for i in range(int(numberOfCars)):
    line = file1.readline().split()
    startIntersectionOfCar = line[0]
    listOfStreet = line[1:]
    # We want to know order of car with intersection in case cars are in same intersection
    car_order.append(startIntersectionOfCar)
    car_streets_dict[startIntersectionOfCar].append(listOfStreet)
    inter_car_dict[startIntersectionOfCar].append(i)
    remain_street[i] = listOfStreet
    
orderedListTotalTime = list()
car_totaltime_dict = dict()
# Find sumOfTimeConsumption  for each car
for carNumber, startIntersectionOfCar in enumerate(car_order):
    # get timeToEndStreet
    sumOfTimeConsumption = 0
    
    for nameOfStreet in car_streets_dict[startIntersectionOfCar][0]:
        timeToEndStreet = int(street_prop_dict[nameOfStreet][0][2])
        sumOfTimeConsumption += timeToEndStreet
        
    car_streets_dict[startIntersectionOfCar].pop(0)
    orderedListTotalTime.append([carNumber, sumOfTimeConsumption])
    car_totaltime_dict[carNumber] = sumOfTimeConsumption

# Rank cars
temp = orderedListTotalTime.copy()
rankedListTotalTime = temp.sort(key = lambda x : x[1])
print(rankedListTotalTime)

import sys
# =========Simulation==============
currentCarLeftDist = 0
greenLightStreetforInter_dict = defaultdict(list)
for D in range(durationOfSim):
    # each intersection
    for startIntersectionOfCar in start_end_dict.keys():
        # nestedListOfStreet = car_streets_dict[startIntersectionOfCar]
        # from this intersection, street orderd list
        # cars in this intersection
        listOfCars = inter_car_dict[startIntersectionOfCar]
        minTimeCar = sys.maxint
        for carNumber in listOfCars:
            if car_totaltime_dict[carNumber] < minTimeCar:
                minTimeCar = carNumber
                
        # green light for this min car street
        greenLightStreetforInter_dict[startIntersectionOfCar].append[(remain_street[minTimeCar][0], D)]
        
        # remove car from intersection
        inter_car_dict[startIntersectionOfCar].remove(minTimeCar)
        # check any car is done with street, then pop remain_street
        
        
        # add any car reach intersection
        

# sumOfTimeConsumtion = dict()
# for 


    
    
# for D in range(durationOfSim):
