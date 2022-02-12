- F + (D – T) points if T ≤ D
- F =  defualt
- T = time the car took

Goal: to get output
    first line: number of intersections with traffic light schedules

    loop:
        line 1: IntersectionNum
        line 2: numberOfDifferentStreets 
        line 3: streetName timeforGreenlight
        .
        .
        . untill range(numberOfDifferentStreets)


Intersection:
    dict values: streets
CarInfo:
    dict values: currentStreet
    dict values: totalTimeLeft
    dict values: currentTime
Street:
    queue: moving cars
    starIntersection
    endIntersection




1. make reading of first line: durationOfSim, numberOfintersections, numberOfStreets numberOfCars, bonusPoint

2. make line readings of numberOfStreets: startOfstreet and endOfstreet, nameOfStreet, timeToEndStreet

3. make line readings of numberOfCars: numberOfStreetCarWant, nameOfStreet ...



Find sumOfTimeConsumtion  for each car

Rank cars have shorest path

open green light for them



=========Simulation==============


D = 0 all red light for each intersection
D = 1 one of incoming streets green light(take timeToEndStreet-1 for car) for each intersection
D = 2 another of incoming streets green light and the others are red  for each intersection
.
.
.
for D loop:
    for each car:




first car takes  1 + 3 +2 = 6

second car takes 3 + 1 = 4



Do Not:
    Find minimumpath(dijktra algo) for each car