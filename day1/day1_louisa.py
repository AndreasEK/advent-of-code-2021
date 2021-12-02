depth1 = input()
depth2 = input()
deeper = 0
while depth2 != '':
    if ( int(depth1)  <  int(depth2) ):
        deeper = deeper + 1
    depth1 = depth2
    depth2 = input()

print(deeper)