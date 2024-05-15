#Imports
import random
import sys
import math

#User input for sequence of coordinates
sequence = sys.argv[1]

#Variables for the robot and state
fuel = 100
weight = 5
fuel_empty = False
fuel_consumed = 0
destination = 0

#Robot Coordinates
x = 0
y = 0

#Dictionary to store dropped samples
#Key = coordinate of sample
#Value = total weight of samples
dropped_samples = {}
    
#Printing the sequence
print("sequence:", sequence)

#Queue to store the sequence dynamically

#Function that converts the user input sequence to a queue of (x, y) coordinates
#@Param sequence as a string
#@Return locations queue as Queue
def convert_sequence(sequence):
    locations_queue = []
    segments = sequence.split(">")
    segments = segments[1:]
    for segment in segments:
        x, y = segment.split(";")
        locations_queue.append((int(x), int(y)))
    locations_queue.append((0, 0))
    return locations_queue

#Function that calculates the fuel consumption per move
#@Param weight as int
#@Return Fuel per move as decimal
def get_fuel_consumption(weight):
    return math.log(weight, 10)

#Function that calculates the fuel usage for the distance to be travelled
#@Param location1 as (x, y) coordinate
#@param location2 as (x, y) coordinate
#Return the fuel consumption to go from loca tion1 to location2 as decimal 
def get__fuel_distance(location1, location2, weight):
    return (abs((location1[0] - location2[0])) + abs(location1[1] - location2[1])) * get_fuel_consumption(weight)

def distance_from_base(location):
    return (abs((location[0] - 0)) + abs(location[1] - 0))

locations_queue = convert_sequence(sequence)

#Loop until location queue is empty
while locations_queue:
    
    #Peek at next location in the queue
    if (fuel_empty == True):
        break
    location = locations_queue[0]
    
    #Printing fuel consumption per move
    print("Fuel Consumption per Move: ", get_fuel_consumption(weight))
    
    #Check if location is not possible to reach
    if (x, y) == (0, 0) and get__fuel_distance((0, 0), location, weight) > fuel / 2:
        
        #Skip this location
        print("Cant get to destination ", location, " as its too far away!")
        locations_queue.pop(0)
        continue
    #Checks if next location is a dropped sample, to get weight of robot
    if location in dropped_samples:
        addedweight = dropped_samples.get(location)
    else:
        addedweight = 10
            
    #Check if robot can't pick up next sample and still make it back to homebase
    if get__fuel_distance((x, y), location, weight) + get__fuel_distance(location, (0, 0), weight + addedweight) > fuel:
        
        #Checks if robot should drop its samples and continue to the next location
        if (get__fuel_distance((x, y), location, 5) + get__fuel_distance(location, (0, 0), weight + addedweight) <= fuel) and distance_from_base((x, y)) < 30:
            #Dropping Samples
            print("Dropping Samples")
            next_location = locations_queue.pop(0)
            locations_queue.insert(-1, (x, y))
            dropped_samples[(x, y)] = weight - 5
            print("Dropped locations: ", dropped_samples)
            weight = 5 
        else:
            #Go back to homebase
            next_location = (0, 0)
    else:
        
        #pop next location from queue
        next_location = locations_queue.pop(0)
        
    arrived = False
    fuel_used = get_fuel_consumption(weight)
    #Loop to move to next location
    while not arrived:
        
        #Base case to check if location has been reached
        if (x, y) == next_location:
            
            #If current location is homebase
            if (x, y) == (0, 0):
                fuel = 100
                weight = 5 
                print("Refueling!")
            else:
                destination += 1
                
                #if current location is a dropped sample
                if (x, y) in dropped_samples:
                    weight += dropped_samples.get((x, y))
                    del dropped_samples[(x, y)]
                else:
                    weight += 10
                    
                print("Arrived at Destination ", destination)
                print("Fuel: ", fuel)
                
            #Change boolean to end loop
            arrived = True
        else:
            #Checks if fuel has ran out, ends both loops
            if fuel <= 0:
                print("Ran out of fuel!")
                fuel_empty = True
                break
            
            #Moving towards location
            if x < next_location[0]:
                x += 1
            elif x > next_location[0]:
                x -= 1 
            else:
                if y < next_location[1]:
                    y += 1
                elif y > next_location[1]:
                    y -= 1
                    
            #Editing fuel variables     
            fuel -= fuel_used
            fuel_consumed += fuel_used
            print(f"> {x};{y}")

#Printing total fuel consumed
print("Total Fuel Used: " , fuel_consumed)