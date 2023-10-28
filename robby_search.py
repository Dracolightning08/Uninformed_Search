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
#***EDIT CODE HERE***
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

    #***START EICHOLTZ CODE***
    # #***EDIT CODE HERE***
    # rows, cols = 1, 1
    # r0, c0 = 0, 0
    # contents = 'E'
    #***END EICHOLTZ CODE***

    # Create Robby's world
    #***EDIT CODE HERE***
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
        #***EDIT CODE HERE***
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
                path = bfs(rw, contents, actions, verbose=verbose)
                if len(path) > 0:
                    print(path)
                else:
                    print("No solution found.")
            elif key == "Return":
                # Use the discovered path (from bfs) to actually move robby through
                # the world! Add a small time delay with time.sleep() so that robby does not move too fast.
                rw.reset()
                rw.goto(r0, c0)
                time.sleep(0.5)

                # ***EDIT CODE HERE***
                # this is part (h) on the hw document
                for action in path:
                    pass

'''-------------------------------------------------------------------------------------------------------------------------------------------------------
                                                    Breadth First Search Method :
--------------------------------------------------------------------------------------------------------------------------------------------------------'''
def bfs(rw, state, actions, verbose=False):
    '''Perform breadth-first search on the world state given an ordered string of actions to check (e.g. 'GNESW').'''
    #***EDIT CODE HERE***
    cnt = 0 # counter to see how long the search took
    path = ''

    if verbose: print('--> searched {} paths'.format(cnt))

    return path
'''-------------------------------------------------------------------------------------------------------------------------------------------------------
                                                    Is Solved Method:
--------------------------------------------------------------------------------------------------------------------------------------------------------'''
def issolved(rw, state, path):
    '''Check whether a series of actions (path) taken in Robby's world results in a solved problem.'''
    rows, cols = rw.numRows, rw.numCols # size of the world
    row, col = rw.getCurrentPosition() # Robby's current (starting) position
    state = list(state) # convert the string to a list so we can update it
    battery = rw.fullBattery

    #***EDIT CODE HERE***
    for action in path:
        pass

        # Did Robby run out of battery?
        if battery <= 0:
            return False

        # Did Robby grab all the cans?
        if state.count("C") == 0:
            return True

    return False # if we made it this far, we did not complete the goal
'''-------------------------------------------------------------------------------------------------------------------------------------------------------
                                                    Is Valid Method:
--------------------------------------------------------------------------------------------------------------------------------------------------------'''
def isvalid(rw, state, path):
    '''Check whether a series of actions (path) taken in Robby's world is valid.'''
    rows, cols = rw.numRows, rw.numCols  # size of the maze
    row, col = rw.getCurrentPosition()  # robby's current (starting) position
    state = list(state)
    memory = []  # keep track of where robby has been to prohibit "loops"
    battery = rw.fullBattery

    #***EDIT CODE HERE***
    for action in path:
        pass
        
        # Path is invalid if Robby has run out of battery
        if False: # ***EDIT CODE HERE***
            return False

        # Path is invalid if Robby's goes "out of bounds"
        if False: # ***EDIT CODE HERE***
            return False

        # Path is invalid if Robby runs into a wall
        if False: # ***EDIT CODE HERE***
            return False

        # Path is invalid if robby repeats a state in memory
        if (row, col, "".join(state)) in memory:
            return False
        memory.append((row, col, "".join(state)))  # add the new state to memory

    return True  # if we made it this far, the path is valid

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.file, args.actions, args.battery, args.verbose)
