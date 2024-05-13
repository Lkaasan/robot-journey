import random
import sys
import math

sequence = sys.argv[1]

fuel = 100
weight = 5
fuel_empty = False
fuel_consumed = 0
destination = 0

x = 0
y = 0

dropped_samples = {}
    
def convert_sequence(sequence):
    locations_queue = []
    segments = sequence.split(">")
    segments = segments[1:]
    for segment in segments:
        x, y = segment.split(";")
        locations_queue.append((int(x), int(y)))
    locations_queue.append((0, 0))
    return locations_queue

def get_fuel_consumption(weight):
    return math.log(weight, 10)

def get_distance(location1, location2, weight):
    return (abs((location1[0] - location2[0])) + abs(location1[1] - location2[1])) * get_fuel_consumption(weight)

print("sequence:", sequence)

locations_queue = convert_sequence(sequence)

while locations_queue:
    location = locations_queue[0]
    print(get_fuel_consumption(weight))
    if (x, y) == (0, 0) and get_distance((0, 0), location, weight) > fuel / 2:
        
        print("Cant get to destination ", location, " as its too far away!")
        locations_queue.pop(0)
        continue
    
    if get_distance((x, y), location, weight) + get_distance(location, (0, 0), weight + 10) > fuel:
        if location in dropped_samples:
            addedweight = dropped_samples.get(location)
        else:
            addedweight = 5
        if get_distance((x, y), location, addedweight) + get_distance(location, (0, 0), addedweight + 10) <= fuel:
            print("Dropping Samples")
            next_location = locations_queue.pop(0)
            locations_queue.insert(-1, (x, y))
            dropped_samples[(x, y)] = weight - 5
            weight = 5 
        else:
            next_location = (0, 0)
    else:
        next_location = locations_queue.pop(0)
    arrived = False
    
    while not arrived:
        if (x, y) == next_location:
            if (x, y) == (0, 0):
                fuel = 100
                weight = 5 
                print("Refueling!")
            else:
                destination += 1
                if (x, y) in dropped_samples:
                    weight += dropped_samples.get((x, y))
                    del dropped_samples[(x, y)]
                else:
                    weight += 10
                print("Arrived at Destination ", destination)
                print("Fuel: ", fuel)
            arrived = True
        else:
            if fuel <= 0:
                print("Ran out of fuel!")
                fuel_empty = True
                break
            
            if x < next_location[0]:
                x += 1
            elif x > next_location[0]:
                x -= 1 
            else:
                if y < next_location[1]:
                    y += 1
                elif y > next_location[1]:
                    y -= 1
            fuel_used = get_fuel_consumption(weight)     
            fuel -= fuel_used
            fuel_consumed += fuel_used
            print(f"> {x};{y}")

print("Total Fuel Used: " , fuel_consumed)