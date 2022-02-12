- F + (D – T) points if T ≤ D
- F =  defualt
- T = time the car took

1. make reading of first line: durationOfSim, numberOfintersections, numberOfStreets numberOfCars, bonusPoint

2. make line readings of numberOfStreets: startOfstreet and endOfstreet, nameOfStreet, timeToEndStreet

3. make line readings of numberOfCars: numberOfStreetCarWant, nameOfStreet ...

    1. Dictionary ==> car1 as key, list of street as value

    2. Dictionary ==> nameOfStreet as key, tuple of startOfstreet, endOfstreet, timeToEndStreet

    3. Dictionary ==> startOfstreet as key,  list of endOfstreet as value


4. Dictionary ==> car 



Find sumOfTimeConsumtion  for each car

Rank cars have shorest path

open green light for them



=========Simulation==============
Goal: to get green light time for the street in each intersection

D = 0 all red light for each intersection
D = 1 one of incoming streets green light(take timeToEndStreet-1 for car) for each intersection
D = 2 another of incoming streets green light and the others are red  for each intersection
.
.
.
for D loop:
    for each intersection:
        if D = 0:
            all red
        else:
            if car in rank:
                give green light
            



first car takes  1 + 3 +2 = 6

second car takes 3 + 1 = 4



Do Not:
    Find minimumpath(dijktra algo) for each car