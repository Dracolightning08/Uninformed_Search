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
                path = bfs(rw, contents, actions, verbose=verbose)
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
                bfs(rw, rw.getState(), actions, verbose=True)

                # ***EDIT CODE HERE***
                # this is part (h) on the hw document
                for action in path:
                    # if letter is N
                    # moveNorth()
                    pass

'''-------------------------------------------------------------------------------------------------------------------------------------------------------
                                                    Breadth First Search Method :
--------------------------------------------------------------------------------------------------------------------------------------------------------'''
def bfs(rw, state, actions, verbose=False):
    '''Perform breadth-first search on the world state given an ordered string of actions to check (e.g. 'GNESW').'''
    #***EDIT CODE HERE*** part e
    cnt = 0 # counter to see how long the search took
    path = '' # initialize the path string
    
    # initialize the queue
    q = Queue()
    # list of visited nodes
    visited_nodes = []

    # add starting node to queue
    # Each node is represented by a tuple (of coordinates)
    q.put((rw.robbyRow, rw.robbyCol, ''))
    visited_nodes.append((rw.robbyRow, rw.robbyCol))
    
    # while q is not empty
    while q:
        print('=========Next item on the queue=========')
        # if there are no nodes for expansion then return failure
        if q.empty():
            print("oh no q is empty")
            return path
        
        #pop the node from the queue
        node = q.get()
        print("node's string " + node[2])
        print("===")

        
        

        # get the contents of the spaces around robby
        percept = rw.getPercept() 
        directions = list(percept.keys()) # robby, north, west, east, south
        # for each available action
        ogr = rw.robbyRow #keep a record of the initial robby location
        ogc = rw.robbyCol
        for move in directions:
            rr0 = ogr
            rc0 = ogc
           
            # for each available action
            # "GNWES"
            # Each "move" value (from getPercept()) corresponds to a letter. The letter value (act) is understood by "path"
            act = ''
            if move == "North":
                act = 'N'
            elif move == "West":
                act = "W"
            elif move == "East":
                act = "E"
            elif move == "South":
                act = "S"
            else:
                act = "G"
            

            print("move =" + move)
            print("act =" + act)


             # assign coordinates for if the next move will be a cardinal direction move
            if act == "N":
                rr0 += 1
            elif act == "E":
                rc0 += 1
            elif act == "S":
                rr0 -= 1
            elif act == "W":
                rc0 -= 1


           
            nextnode = percept[move] # eg: percept['Robby'] will get the contents of the grid block where robby is sitting
            # grab cans and batteries
            print("nextnode contents = " + nextnode)
            print("Current coords:")
            print(rr0, rc0)
            
            if move == "Robby" and (nextnode == "C" or nextnode == "B"):
                print('ROBBY IS GRABBING')
                # append grab bc there is something to grab
                # he has not moved since he grabbed
                if isvalid(rw, state, node[2] + act):
                    q.put((rw.robbyRow, rw.robbyCol, node[2] + "G"))
                    visited_nodes.append((rw.robbyRow, rw.robbyCol))
                    rw.grid[rw.RobbyRow][rw.RobbyRow] = "E"

            else:
                if isvalid(rw, state, node[2] + act):
                    print("--This move is valid.--")
                    # move the robby's coordinates and put him on the queue for moving
                    # q.put((rw.robbyRow, rw.robbyCol, node[2] + act))
                    # visited_nodes.append((rw.robbyRow, rw.robbyCol))
                    
                    
                    # if the visited nodes list contains the tuple of coordinates that we are trying to move to
                    if ((rr0, rc0) in visited_nodes):
                        print("rr0, rc0 in visited nodes")
                        
                        continue
                    else:
                        print("putting into the q:")
                        print(node[2] + act)
                        q.put((rr0, rc0, node[2] + act))
                        visited_nodes.append((rr0, rc0))
            
            # if node contains goal state then return solution
            if issolved(rw, rw.getState(), node[2]):
                print("is solved line 176")
                return node[2]
            cnt += 1
            if cnt == 20:
                return "sob"
            if verbose: print('--> searched {} paths'.format(cnt))
            print('===== end path =====')
        #End, put next item on the queue
                    

    if verbose: print('--> searched {} paths'.format(cnt))

    return path
'''-------------------------------------------------------------------------------------------------------------------------------------------------------
                                                    Is Solved Method:
--------------------------------------------------------------------------------------------------------------------------------------------------------'''
def issolved(rw, state, path):
    '''Check whether a series of actions (path) taken in Robby's world results in a solved problem.'''
    # part f
    rows, cols = rw.numRows, rw.numCols # size of the world
    row, col = rw.getCurrentPosition() # Robby's current (starting) position
    state = list(state) # convert the string to a list so we can update it
    battery = rw.fullBattery

    #***EDIT CODE HERE***
    for action in path:

        # Did Robby run out of battery?
        if rw.batteryLife <= 0:
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
    # part g
    rows, cols = rw.numRows, rw.numCols  # size of the maze
    row, col = rw.getCurrentPosition()  # robby's current (starting) position
    state = list(state)
    memory = []  # keep track of where robby has been to prohibit "loops"
    battery = rw.fullBattery

    #***EDIT CODE HERE***
    for action in path:
        #convert action
        if action == "N":
            row += 1
        elif action == "E":
            col +=1
        elif action == "S":
            row -= 1
        elif action == "W":
            col -=1
    
        # Path is invalid if Robby has run out of battery
        if rw.batteryLife <= 0: # ***EDIT CODE HERE***
            print("     dead battery")
            return False

        # Path is invalid if Robby's goes "out of bounds"
        print("                 is valid method:")
        print(row, col)
        if row > rows or row < 0 or col > cols or col < 0: # ***EDIT CODE HERE***
            print("     out of bounds")
            return False

        # Path is invalid if Robby runs into a wall
        if rw.grid[row][col] == 'W': # ***EDIT CODE HERE***
            print("      wall")
            return False

        # Path is invalid if robby repeats a state in memory
        if (row, col, "".join(state)) in memory:
            print("     position in memory")
            return False
        memory.append((row, col, "".join(state)))  # add the new state to memory

    return True  # if we made it this far, the path is valid

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.file, args.actions, args.battery, args.verbose)
