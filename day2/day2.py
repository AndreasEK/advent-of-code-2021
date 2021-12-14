command = input()
horizontal = 0
depth = 0
aim = 0

while command != "STOP":
    direction, distance = command.split()
    distance = int(distance)
    if direction == "forward":
        horizontal += distance
        depth += aim * distance
    if direction == "down":
        aim += distance
    if direction == "up":
        aim -= distance
    command = input()

    print(f"horizontal = {horizontal}")
    print(f"depth =  {depth}")
    print(f"Multiplied: {horizontal * depth}")
