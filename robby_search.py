'''-------------------------------------------------------------------------------------------------------------------------------------------------------
                                                    Imports and Modules:
-------------------------------------------------------------------------------------------------------------------------------------------------------'''
# robby_search.py
# Use breadth-first search (BFS) to help Robby the Robot pick up cans without running out of battery.

import argparse
from collections import deque
import pdb
from queue import Queue
from robby.graphics import *
from robby import World
import time
'''-------------------------------------------------------------------------------------------------------------------------------------------------------
                                                    Argparse Arguments:
--------------------------------------------------------------------------------------------------------------------------------------------------------'''
# Use argparse to allow user to enter command line arguments for:
#   *file - a text file containing the world design (required)
#   *actions - a string defining the order of actions to search (optional, default='GNESW')
#   *battery - an integer defining the full battery power (optional, default=7)
#   *verbose - a flag to display details about the search
parser = argparse.ArgumentParser(description="Use breadth-first search (BFS) to help Robby the Robot pick up cans without running out of battery")
#***EDIT CODE HERE*** part a
#parser.parse_args() # call argparse CHECK LATER commented this out bc it wasn't accepting the args with it
# Create the argument for the world design file
parser.add_argument("file", help="A text file containing the world design")
# Create the argument for the actions in the world
parser.add_argument("--actions", default="GNESW", help="Order of actions to search")
# Create the argument for default battery for Robby
parser.add_argument("--battery", type=int, default=7, help="Full battery power")
# Create the argument for the flags to display details regarding the search
parser.add_argument("--verbose", action="store_true", help="Display details about the search")
args = parser.parse_args()

# Assign the value of the command-line with an argument composing of the name world_file.
world_file = args.file
# Assigns the value of the command-line with name actions containing instructions on what to do
actions = args.actions
# Assigns the value of the command-line with the name battery and with the total battery life.
battery = args.battery
# Assigns the argument verbose to whatever being flagged
verbose = args.verbose

'''-------------------------------------------------------------------------------------------------------------------------------------------------------
                                                    Main Method:
--------------------------------------------------------------------------------------------------------------------------------------------------------'''
def main(file, actions, battery, verbose):
    # Read world parameters (size, location of Robby, and contents) from file
    # part b
    # open the file
    f = open(file, "r")
    # read the rows and cols
    rowsandcols = f.readline()
    rowsandcols = rowsandcols.split()
    # Define the size of Robby's World
    rows = int(rowsandcols[0])
    cols = int(rowsandcols[1])

    # Read robby's starting coordinates
    rc = f.readline()
    rc = rc.split()
    # Define robby's starting coordinates
    #r0 = row coordinate
    #c0 = col coordinate
    r0 = int(rc[0])
    c0 = int(rc[1])

    # Define the string that populates Robby's World as one line
    contents = f.read().replace('\n', '').replace('.', 'E')

    f.close()

    

    # Create Robby's world
    #***EDIT CODE HERE*** part c
    rw = World(rows, cols)
    # Populate the world with walls, cans, and batteries
    rw.load(contents)
    # Put robby in his designated spot
    rw.goto(r0, c0)
    # Set the full battery level
    rw.setFullBattery(battery)
    #Turn on Robby's World
    rw.graphicsOn()
    #***END EDIT CODE HERE***

    # Play in Robby's world
    path = ''
    while True:
        # Check to see if Robby has picked up all the cans
        cons = rw._gridContents()
        #***EDIT CODE HERE*** part d
        if not cons.__contains__("C"): 
            #***END EDIT CODE HERE*** 
            rw.graphicsOff("Robby wins!")

        # Handle key presses
        key = rw.checkKey()
        if key:
            if key == "Escape":
                break
            elif key == "Up":
                rw.north()
            elif key == "Down":
                rw.south()
            elif key == "Right":
                rw.east()
            elif key == "Left":
                rw.west()
            elif key == "space":
                rw.grab()
            elif key == "d": # debug
                pdb.set_trace()
            elif key == "r": # reset the world
                rw.reset()
                rw.goto(r0, c0)
                rw.graphicsOn()
            elif key == "s": # display the current world at the command line
                rw.show()
            elif key == "b": # BFS
                print('Running breadth-first search...', end='')
                time.sleep(0.5)
                path = BFS(rw, 7)
                if len(path) > 0:
                    print(path)
                else:
                    print("No solution found.")
            elif key == "Return":
                # Use the discovered path (from bfs) to actually move robby through
                # the world! Add a small time delay with time.sleep() so that robby does not move too fast.
                print("yippee (return was pressed)")
                rw.reset()
                rw.goto(r0, c0)
                time.sleep(0.5)
                # print(type(rw))
                path = BFS(rw, 7)
                # Reset again after the search
                rw.reset()
                rw.goto(r0, c0)
                if path != "F":
                    # If path is not a failure
                    for action in path:
                        # if letter is N
                        # moveNorth()
                        if action == "N":
                            rw.north()
                        elif action == "S":
                            rw.south()
                        elif action == "W":
                            rw.west()
                        elif action == "E":
                            rw.east()
                        elif action == "G":
                            rw.grab()
                        time.sleep(0.5)
                        print(action)
                    # print(path)

                else:
                    print("No path found")

from robby.__init__ import World
#This is here for autofill
def convertDir(dir, row, col):
    if dir == "N":
        return (row - 1, col)
    if dir == "S":
        return (row + 1, col)
    if dir == "E":
        return (row, col + 1)
    if dir == "W":
        return (row, col - 1)
    return (row, col)
# dirOptions = ["N", "S", "E", "W", "G"]
def checkDirections(rw: World, QZero : tuple, maxBattery : int):
    dirOptions = ["N", "S", "E", "W"]
    dirOptionsFull = {"N": "North", "S": "South", "E": "East", "W": "West", "G": "Robby"}

    finalOptions = []
    startBattery = QZero[3] - 1
    startCans = QZero[4]
    grab = ""
    # print("Checking directions", rw.getPercept()["Robby"], rw.getCurrentPosition())
    rw.goto(QZero[1], QZero[2])
    if startBattery <= 0:
        # Out of battery check
        # print("Ran out of battery", QZero[0])
        return []
    # print(rw.getCurrentPosition())
    batteryBattery = 0
    batteryOption = False
    if  rw.getPercept()["Robby"] == "B":
        # If the starting position is a battery and youre grabbing it
        # print("Grabbed a battery", rw.getCurrentPosition())
        batteryBattery = maxBattery #The battery if we grab the battery
        batteryOption = True
        # startBattery = maxBattery
        grab = "G"
    elif rw.getPercept()["Robby"] == "C":
        # If the starting position is a can and youre grabbing it
        # print(QZero[0])
        # print("Grabbed a can", startCans + 1, "/", rw.getCansRemaining(), "Position: ", rw.getCurrentPosition())
        startCans += 1
        startBattery -= 1
        grab = "G"
        if (startCans == rw.getCansRemaining()):
            # print("Found all cans")
            return True, QZero[0] + "G"
        # print(startBattery, QZero[0])
        if startBattery <= 0:
            # Out of battery check
            # print("Ran out of battery")
            return []
    for dir in dirOptions:
        cans = startCans
        battery = startBattery
        # print(QZero[0], dir)
        # print(dir)

        # Setting up Q requires running dirOptions at base

        row, col = convertDir(dir, QZero[1], QZero[2])
        # print((x, y))


        KnownPos : list = QZero[5].copy()
        # failed = False
        # print("A")
        if row >= rw.numRows or col >= rw.numCols or col < 0 or row < 0:
            # Out of bounds check
            # print("Went out of bounds",QZero[0] + dir, row,col)
            continue
        # print("B")
        if rw.getPercept()[dirOptionsFull[dir]] == "W":
            # Wall check
            # print(QZero[0])
            # print("Tried to walk into a wall", rw.getPercept()[dirOptionsFull[dir]], dir, (row, col))
            continue
        # print("C")
        shouldAvoidGrabbing = False
        if battery <= 0 and not batteryOption:
            # Out of battery check
            # print("Ran out of battery")
            continue

        elif battery <= 0:
            # If you have no battery and grabbing a battery is an option always take it
            shouldAvoidGrabbing = True

        # print("D")
        if (row, col) in KnownPos:
            # print("XY: ", (row,col), " KnownPos: ", KnownPos)
            # Double back check
            # print("Went to same position twice")
            continue
        # print("E")
        KnownPos.append(rw.getCurrentPosition())
        # print("Direction good")
        # Check path without battery first, its lower cost
        if(batteryOption):
            # print("Adding not grabbing battery")
            finalOptions.append((QZero[0] + dir, row, col, battery, cans, KnownPos))
        if not shouldAvoidGrabbing:
            # Basically if battery was empty without grabbing battery ignore this path
            if batteryOption:
                finalOptions.append((QZero[0] + grab + dir, row, col, batteryBattery, cans, KnownPos))
            else:
                finalOptions.append((QZero[0] + grab + dir, row, col, battery, cans, KnownPos))



    # print( finalOptions)
    return finalOptions

def BFS(rw : World, maxBattery):
    dirOptions = ["N", "S", "E", "W"]
    dirOptionsFull = {"N": "North", "S": "South", "E": "East", "W": "West", "G": "Robby"}
    # Lets set up Q:
    # Q follows the following format:
    # [(dir, x, y, battery, cans, [knownPos])]
    Q = []
    grab = ""
    battery = maxBattery
    cans = 0
    startX, startY = rw.getCurrentPosition()
    if rw.getPercept()["Robby"] == "C":
        # Started on a can
        # print("Started on a can", rw.getCurrentPosition())
        grab = "G"
        battery -= 1
        cans = 1
    elif rw.getPercept()["Robby"] == "B":
        # Started on a battery
        # Who cares, would cost extra to grab and no change in overall points
        grab = ""
    for dir in dirOptions:
        # Setting up Q requires running dirOptions at base
        row, col = convertDir(dir, startX, startY)
        # battery = maxBattery - 1
        # cans = 0
        if row >= rw.numRows or col >= rw.numCols or col < 0 or row < 0:
            # Out of bounds check
            continue
        if rw.getPercept()[dirOptionsFull[dir]] == "W":
            # Wall check
            continue
        # print(row,col)
        rw.goto(row, col)
        # failed = False
        Q.append((grab + dir, row, col, battery, cans, [(startX,startY)]))
    # Initial q is the same as the options

    while len(Q) != 0:
        # While Q isn't empty
        # knownPos = Q[0][5]
        # print(Q)
        # print(Q[0][5])
        cansFound = Q[0][4]
        if cansFound == rw.getCansRemaining(): #Since we aren't actually picking up any cans while we simulate the motion, this will always be all the cans
            # Grabbed all the cans
            return Q[0][0]
        # print(Q[0])
        # char = Q[0][0][-1] # Final character
        options = checkDirections(rw, Q[0], maxBattery)
        if options != []:
            if(options[0] == True):
                # This is a weird way of doing things
                return options[1]

        Q.extend(options)
        Q.pop(0)
        # Pop the first part, knowing the path didn't find everything
    # print("No path found")
    # rw.goto(1,1)
    # print(rw.getCurrentPosition())
    return "F"

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.file, args.actions, args.battery, args.verbose)
