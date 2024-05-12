import random
import sys
import math

sequence = sys.argv[1]

fuel = 100
weight = 5
fuel_per_move = math.log(weight, 10)
fuel_empty = False
destination = 1

def convert_sequence(sequence):
    locations_queue = []
    segments = sequence.split(">")
    segments = segments[1:]
    for segment in segments:
        x, y = segment.split(";")
        locations_queue.append((int(x), int(y)))
    locations_queue.append(0, 0)
    return locations_queue

def get_distance(location1, location2):
    return abs(location1[0] - location2[0]) + abs(location1[1] - location2[1])

print("sequence:", sequence)

x = 0
y = 0
print (fuel_per_move)
locations_queue = convert_sequence(sequence)

while locations_queue:
    if fuel_empty == True or destination > 20:
        break
    
    print(locations_queue)
    location = locations_queue[0]
    
    if (x, y) == (0, 0) and get_distance((0, 0), location) > fuel / 2:
        print("Cant get to destination ", location, " as its too far away!")
        locations_queue.pop(0)
        continue
    
    if get_distance((x, y), location) + get_distance(location, (0, 0)) > fuel:
        next_location = (0, 0)
    else:
        next_location = locations_queue.pop(0)
    arrived = False
    
    while not arrived:
        if (x, y) == next_location:
            if (x, y) == (0, 0):
                fuel = 100
                weight = 5
            print("Arrived at Destination ", destination)
            arrived = True
            destination += 1
        else:
            if fuel < 1:
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
                    
            fuel -= 1
            print(f"> {x};{y}")
