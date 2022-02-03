

file1 = open("input/a.txt","r+")
# print(file1.read()) 

firstline = file1.readline().split()
# print(firstline.split())
durationOfSim               = firstline[0]
numberOfIntersections       = firstline[1]
numberOfStreets             = firstline[2]
numberOfCars                = firstline[3]
bonusPoint                  = firstline[4]


car_streets_dict = dict()
street_prop_dict = dict()
start_end_dict = dict()
for i in range(numberOfStreets):
    line = file1.readline()
    startOfStreet = line[0]
    endOfStreet = line[1]
    nameOfStreet = line[2]
    timeToEndStreet = line[3]
    
    if startOfStreet in street_prop_dict:
        continue
    else:
        street_prop_dict[nameOfStreet] = (startOfStreet, endOfStreet, timeToEndStreet)
    
    if startOfStreet in start_end_dict:
        start_end_dict[startOfStreet].append(endOfStreet)
    else:
         start_end_dict[startOfStreet] =[endOfStreet]
    
    
    
for i in range()
