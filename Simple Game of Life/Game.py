import random
import time

"""
++++++++++++++++
The Game of Life
++++++++++++++++

Description:
The Game of Life really isn't a game at all. Life is a "cellular automation" - a system of cells that live on a grid,
where they live, die and evolve according to the rules that govern their world. The game starts by initalizing a grid randomly, each cell
labeled as DEAD or ALIVE. The game proceeds round by round, looking at each of its 8 immediate neighbors and counts up the number of them
that are currently alive. The cell then updates its own liveness according to 4 rules:
1. Any live cell with 0 or 1 live neighbors becomes DEAD
2. Any live cell with 2 or 3 live neighbors stays LIVE
3. Any live cell with more than 3 live neighbors become DEAD
4. Any dead cell with exactly 3 live neighbors becomes LIVE
(The rules can be changed to give some unique designs when running the program. These are the ones I used to create the program)

The game can also be started from a save state that the user can insert into the program. (deactivated at the moment)
By: Logan Cole
"""

DEAD = 0
LIVE = 1

def deadState(width, height):
    """
    Construct an empty state with all cells set to dead

    Parameters
    ----------
    width = the width of the state, in cells
    height = the height of the state, in cells

    Return: A state of dimesions width x height, with all cells set to dead
    """
    return [[DEAD for _ in range(height)] for _ in range(width)]
    
def randomState(width, height):
    """
    Construct a random state with all cells randomly set
    
    Parameters
    ----------
    width = the width of the state, in cells
    height = the height of the state, in cells
    
    Return: a state of dimesions width x height, with all cells randomly set to DEAD or LIVE with equal probability
    """
    state = deadState(width, height)
    for x in range(0, stateWidth(state)):
        for y in range(0, stateHeight(state)):
            randomNum = random.random()
            if randomNum > 0.85:
                cellState = LIVE
            else:
                cellState = DEAD
            state[x][y] = cellState
    return state


def stateWidth(state):
    return len(state)

def stateHeight(state):
    return len(state[0])


def nextCellValue(cell_coords, state):
    """
    Get the next value of a single cell
    
    Return: the new state of the given cell - either DEAD or LIVE
    """
    width = stateWidth(state)
    height = stateHeight(state)
    x = cell_coords[0]
    y = cell_coords[1]
    n_live_neighbors = 0
    
    for x1 in range((x-1), (x+1)+1):
        #make sure it doesn't go off board
        if x1 < 0 or x1 >= width: continue
        
        for y1 in range((y-1), (y+1)+1):
            #make sure it doesn't go off board
            if y1 < 0 or y1 >= height: continue
            #make sure it doesn't count the cell as a neighbor of itself
            if x1 == x and y1 == y: continue
            
            if state[x1][y1] == LIVE:
                n_live_neighbors +=1
    if state[x][y] == LIVE:
        if n_live_neighbors <= 1: #rule number 1
            return DEAD
        elif n_live_neighbors <= 3: #rule number 2
            return LIVE
        else:
            return DEAD #rule number 3
    else:
        if n_live_neighbors == 3: #rule number 4
            return LIVE
        else:
            return DEAD


def nextBoardState(initState):
    """
    Take a single step in the game of life
    
    Return: the next state of the Game Board, after taking one step for every cell in the previous state
    """
    width = stateWidth(initState)
    height = stateHeight(initState)
    nextState = deadState(width, height)
    
    for x in range(0, width):
        for y in range(0, height):
            nextState[x][y] = nextCellValue((x,y), initState)
    return nextState


def render(state):
    """
    Displays a state by printing to the terminal
    """
    display_as = {
        DEAD: ' ',
        LIVE: u"\u2588" #Unicode for a filled in sqaure
    }
    
    lines = []
    for y in range(0, stateHeight(state)):
        line = ''
        for x in range(0, stateWidth(state)):
            line += display_as[state[x][y]] * 2
        lines.append(line)
    print ("\n".join(lines))
    


def loadBoardState(filepath):
    """
    Loads a board state from the given filepath
    
    Returns: board state loaded from the given filepath
    """
    
    with open(filepath, 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
    
    height = len(lines)
    width = len(lines[0])
    board = deadState(height, width)
    
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            board[x][y] = int(char)
    return board


def runForever(initState):
    """
    Runs the Game of Life forever, starting from the given inital state
    
    program must be forcibly exited
    """
    
    nextState = initState
    while True:
        render(nextState)
        nextState = nextBoardState(nextState)
        time.sleep(0.03)

if __name__ == "__main__":
    initState = randomState(100, 50)
    runForever(initState)