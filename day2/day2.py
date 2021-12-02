command = input()
horizontal = 0
depth = 0
aim = 0
while command != "STOP":
    distance = int(command.split()[1])
    if command.startswith("forward"):
        horizontal += distance
        depth += aim * distance
    if command.startswith("down"):
        aim += distance
    if command.startswith("up"):
        aim -= distance
    command = input()

print(f"horizontal = {horizontal}")
print(f"depth =  {depth}")
print(f"Multiplied: {horizontal * depth}")
