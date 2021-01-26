#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 12:59:09 2021

@author: jason
"""
#!/usr/bin/env python3


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """
    return new_game_nd((num_rows, num_cols), bombs)

#    board = []
#    mask = []
    
#    for r in range(num_rows):
#        row = []
#        for c in range(num_cols):
#            if (r,c) in bombs: #change from [r,c] to (r,c)
#                row.append('.')
#            else:
#                row.append(0)
#        board.append(row)
    
#    for r in range(num_rows):
#        row = []
#        for c in range(num_cols):
#            row.append(False)
#        mask.append(row)
    
#    for r in range(num_rows):
#        for c in range(num_cols):
#            if board[r][c] == 0:
#                neighbor_bombs = 0
#                if 0 <= r-1 < num_rows:
#                    if 0 <= c-1 < num_cols:
#                        if board[r-1][c-1] == '.':
#                            neighbor_bombs += 1
#                if 0 <= r < num_rows:
#                    if 0 <= c-1 < num_cols:
#                        if board[r][c-1] == '.':
#                            neighbor_bombs += 1
#                if 0 <= r+1 < num_rows:
#                    if 0 <= c-1 < num_cols:
#                        if board[r+1][c-1] == '.':
#                            neighbor_bombs += 1
#                if 0 <= r-1 < num_rows:
#                    if 0 <= c < num_cols:
#                        if board[r-1][c] == '.':
#                            neighbor_bombs += 1
#                if 0 <= r < num_rows:
#                    if 0 <= c < num_cols:
#                        if board[r][c] == '.':
#                            neighbor_bombs += 1
#                if 0 <= r+1 < num_rows:
#                    if 0 <= c < num_cols:
#                        if board[r+1][c] == '.':
#                            neighbor_bombs += 1
#                if 0 <= r-1 < num_rows:
#                    if 0 <= c+1 < num_cols:
#                        if board[r-1][c+1] == '.':
#                            neighbor_bombs += 1
#                if 0 <= r < num_rows:
#                    if 0 <= c+1 < num_cols:
#                        if board[r][c+1] == '.':
#                            neighbor_bombs += 1
#                if 0 <= r+1 < num_rows:
#                    if 0 <= c+1 < num_cols:
#                        if board[r+1][c+1] == '.':
#                            neighbor_bombs += 1
#                board[r][c] = neighbor_bombs
#    return {
#        'dimensions': (num_rows, num_cols),
#        'board' : board,
#        'mask' : mask,
#        'state': 'ongoing'}


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """
    return dig_nd(game, (row, col))

#    if game['state'] == 'defeat' or game['state'] == 'victory':
#        game['state'] = game['state']  # keep the state the same
#        return 0
#
#    if game['board'][row][col] == '.':
#        game['mask'][row][col] = True
#        game['state'] = 'defeat'
#        return 1
#
#    bombs = 0
#    covered_squares = 0
#    for r in range(game['dimensions'][0]):
#        for c in range(game['dimensions'][1]):
#            if game['board'][r][c] == '.':
#                if  game['mask'][r][c] == True:
#                    bombs += 1
#            elif game['mask'][r][c] == False:
#                covered_squares += 1
#    if bombs != 0:
#        # if bombs is not equal to zero, set the game state to defeat and
#        # return 0
#        game['state'] = 'defeat'
#        return 0
#    if covered_squares == 0:
#        game['state'] = 'victory'
#        return 0
#
#    if game['mask'][row][col] != True:
#        game['mask'][row][col] = True
#        revealed = 1
#    else:
#        return 0
#
#    if game['board'][row][col] == 0:
#        num_rows, num_cols = game['dimensions']
#        if 0 <= row-1 < num_rows:
#            if 0 <= col-1 < num_cols:
#                if game['board'][row-1][col-1] != '.':
#                    if game['mask'][row-1][col-1] == False:
#                        revealed += dig_2d(game, row-1, col-1)
#        if 0 <= row < num_rows:
#            if 0 <= col-1 < num_cols:
#                if game['board'][row][col-1] != '.':
#                    if game['mask'][row][col-1] == False:
#                        revealed += dig_2d(game, row, col-1)
#        if 0 <= row+1 < num_rows:
#            if 0 <= col-1 < num_cols:
#                if game['board'][row+1][col-1] != '.':
#                    if game['mask'][row+1][col-1] == False:
#                        revealed += dig_2d(game, row+1, col-1)
#        if 0 <= row-1 < num_rows:
#            if 0 <= col < num_cols:
#                if game['board'][row-1][col] != '.':
#                    if game['mask'][row-1][col] == False:
#                        revealed += dig_2d(game, row-1, col)
#        if 0 <= row < num_rows:
#            if 0 <= col < num_cols:
#                if game['board'][row][col] != '.':
#                    if game['mask'][row][col] == False:
#                        revealed += dig_2d(game, row, col)
#        if 0 <= row+1 < num_rows:
#            if 0 <= col < num_cols:
#                if game['board'][row+1][col] != '.':
#                    if game['mask'][row+1][col] == False:
#                        revealed += dig_2d(game, row+1, col)
#        if 0 <= row-1 < num_rows:
#            if 0 <= col+1 < num_cols:
#                if game['board'][row-1][col+1] != '.':
#                    if game['mask'][row-1][col+1] == False:
#                        revealed += dig_2d(game, row-1, col+1)
#        if 0 <= row < num_rows:
#            if 0 <= col+1 < num_cols:
#                if game['board'][row][col+1] != '.':
#                    if game['mask'][row][col+1] == False:
#                        revealed += dig_2d(game, row, col+1)
#        if 0 <= row+1 < num_rows:
#            if 0 <= col+1 < num_cols:
#                if game['board'][row+1][col+1] != '.':
#                    if game['mask'][row+1][col+1] == False:
#                        revealed += dig_2d(game, row+1, col+1)
#
#    bombs = 0  # set number of bombs to 0
#    covered_squares = 0
#    for r in range(game['dimensions'][0]):
#        # for each r,
#        for c in range(game['dimensions'][1]):
#            # for each c,
#            if game['board'][r][c] == '.':
#                if  game['mask'][r][c] == True:
#                    # if the game mask is True, and the board is '.', add 1 to
#                    # bombs
#                    bombs += 1
#            elif game['mask'][r][c] == False:
#                covered_squares += 1
#    bad_squares = bombs + covered_squares
#    if bad_squares > 0:
#        game['state'] = 'ongoing'
#        return revealed
#    else:
#        game['state'] = 'victory'
#        return revealed
#    
#    return {
#        'dimensions': (num_rows, num_cols),
#        'board' : board,
#        'mask' : mask,
#        'state': 'ongoing'}

def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
#    board = []
#    for row in game['board']:
#        board.append(row[:])
#
#    for y in range(len(board)):
#        for x in range(len(board[y])):
#            if board[x][y] == 0:
#                board[x][y] = ' '
#            else:
#                board[x][y] = str(board[x][y])
#            if not game['mask'][x][y]:
#                if not xray:
#                    board[x][y] = "_"
#    return board
    return render_nd(game, xray)


def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    board = render_2d(game, xray)       
        
    result = ""
    
    for i in range(len(board)):
        temp = ""
        for j in board[i]:
            temp += j
        result += temp + '\n'

    return result[:-1]

# N-D IMPLEMENTATION
    
def initialize(dimension, num):
    """
    This helper function creates the basic board based on dimensions.
    Parameters: dimensions (tuple), num (int)
    
    >>> dimension = (3, 3, 2)
    >>> initialize(dimension, 0)
    [[[0, 0], [0, 0], [0, 0]], 
    [[0, 0], [0, 0], [0, 0]], 
    [[0, 0], [0, 0], [0, 0]]]
    """        
    #initialize variable
    result = []
    #if the len(dimensions) doesn't equal 1
    if len(dimension) != 1:
        for i in range(dimension[0]): 
            #for the x coord in dimension, append result, then go to next dimensions
            result.append(initialize(dimension[1:], num))
            #dimension[1:] = (3,3)
        return result
    #once len(dimensions) equals 1, then make final append
    else:
        for i in range(dimension[-1]):
            result.append(num)
        return result

def set_point(result, coordinate, num):
    """
    This helper function sets a new value at a specific coordinate point.
    >>> result = [[[0, 0], [0, 0], [0, 0], [0, 0]],
    ...         [[0, 0], [0, 0], [0, 0], [0, 0]]]
    >>> set_point(result, (0, 0, 1), 1)
    >>> print(result)     
    [[[0, 1], [0, 0], [0, 0], [0, 0]], 
    [[0, 0], [0, 0], [0, 0], [0, 0]]]
    """
    #if the len(coordinate) doesn't equal 1
    if len(coordinate) != 1:
        #go to the x coord in result, and move the coordinate one over
        set_point(result[coordinate[0]], coordinate[1:], num)
    else:
        #if the len(coordinate) does equal 1, then change the value at that point
        result[coordinate[0]] = num

def get_adj_points(li, dimension, coordinate):
    """
    Given a coordinate in an array, returns list of adjacent coordinates as tuples
    >>> li = []
    >>> dimension = (3, 3, 3)
    >>> coordinate = (0, 0, 1)
    >>> get_adj_points(li, dimension, coordinate)
    [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), 
    (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1), 
    (0, 0, 2), (1, 0, 2), (0, 1, 2), (1, 1, 2)]
    """
    #initialize variables
    new = []
    
    #for the range in between minimum/maximum (edge conditions)
    for i in range(max(0, coordinate[0] - 1), min(dimension[0], coordinate[0] + 2)):
        #if not empty, add range in dimension
        if li != []:
            for point in li: #for each point, add range in dimension
                new.append(point + [i])
        #if empty, add value
        else:
            new.append([i])
    
    result = []
    #when recursion is complete
    if len(coordinate) == 1:
        for point in new:
            result.append(tuple(point))
        return result
    
    #run recursive as you move onto the next dimensions and coordinate
    return get_adj_points(new, dimension[1:], coordinate[1:]) 

def get_value_from_coordinate(result, coordinate):
    """
    This helper function obtains the value at the coordinate of an array.
    
    >>> result = [[[3, '.'], [3, 3], [1, 1], [0, 0]], [['.', 3], [3, '.'], [1, 1], [0, 0]]]
    >>> get_value_from_coordinate(result, (0, 0, 1))
    '.'
    """
    #run recursive --> keep going until you go through all the coordinate
    if len(coordinate) != 1:
        return get_value_from_coordinate(result[coordinate[0]], coordinate[1:])
    else:
        #when complete, return value at coordinate
        return result[coordinate[0]]

def all_possible_points(points, dimension):
    """
    The helper function returns all the points based on the dimensions.
    >>> li = []
    >>> dimension = (3, 3, 3)
    >>> all_possible_points(li, dimension)
    [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0), (1, 1, 0), (2, 1, 0), (0, 2, 0), 
    (1, 2, 0), (2, 2, 0), (0, 0, 1), (1, 0, 1), (2, 0, 1), (0, 1, 1), (1, 1, 1), 
    (2, 1, 1), (0, 2, 1), (1, 2, 1), (2, 2, 1), (0, 0, 2), (1, 0, 2), (2, 0, 2), 
    (0, 1, 2), (1, 1, 2), (2, 1, 2), (0, 2, 2), (1, 2, 2), (2, 2, 2)]
    """
    result = []
    temp = []
    
    #if the length of the list isn't 0,
    if len(points) != 0:
        #go through each point in the dimensions and appent he point
        for x in range(dimension[0]): 
            for point in points:
                result.append(point + [x])
                
    #if empty, add all numbers in dimension
    if len(points) == 0:
        for x in range(dimension[0]):
            result.append([x])
            
    #if recursion is complete, cast every point as tuple to return value
    if len(dimension) == 1:
        for x in result:
            temp.append(tuple(x))
        return temp
    
    #go through recursion, going through step at a time
    return all_possible_points(result, dimension[1:])


def check_state(board, mask, dimension):
    """
    This helper function checks the state of the game.
    Parameters: board(list), mask(list), dimension(tuple)
    >>> board1 = [[['.', '.'], [2, 1]],
    ...          [['.', 3], [2, '.']]]
    >>> mask1 = [[[False, False], [False, False]],
    ...         [[False, False], [True, False]]]
    >>> dimension = (2, 2, 2)
    >>> check_state(board1, mask1, dimension)
        'ongoing'

    >>> board2 = [[['.', '.'], [2, 1]],
    ...          [['.', 3], [2, '.']]]
    >>> mask2 = [[[False, False], [True, True]],
    ...         [[False, True], [True, False]]]
    >>> dimension = (2, 2, 2)
    >>> check_state(board2, mask2, dimension)
        'victory'
    """
    #initialize variables
    ls = []
    points = all_possible_points(ls, dimension)
        
    #for each point in points
    for point in points:
        value_coord = get_value_from_coordinate(board, point)
        value_mask = get_value_from_coordinate(mask, point)
        #if the value is not a bomb and it is False
        if value_coord != '.':
            if not value_mask: 
                #the game has not been won, and it is ongoing
                return 'ongoing' #if any covered squares, end loop and return False
    
    #if every square has revealed, then victory!
    return 'victory'


def zero_checker(game, points):
    """
    This helper function assists when the uncovered value is a 0 for dig_nd function.
    The structure is similar to dig_nd function.
    Parameters: game (dictionary), points (tuple)
    """
    value_mask = get_value_from_coordinate(game['mask'], points)
    value_coord = get_value_from_coordinate(game['board'], points)
    uncovered = 0
    
    #if already checked, then return uncovered value
    if value_mask:
        return uncovered
    
    #set point, and reveal the value
    set_point(game['mask'], points, True)
    uncovered += 1
    
    adjacent_points = []
    #if this value is 0, go through adjacent points
    if value_coord == 0:
        for point in get_adj_points(adjacent_points, game['dimensions'], points):
            #run recursively to check if the value is equal to 0
            temp = zero_checker(game, point)
            uncovered += temp
    
    return uncovered

def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """
    #initialize board and mask
    board = initialize(dimensions, 0)
    mask = initialize(dimensions, False)
    
    #for each coordinate of the bombs
    for coordinate in bombs:
        #set the coordinate as a bomb
        set_point(board, coordinate, '.')
        #create a list of all the adjacent points of the bombs
        adjacent_points = []
        adjacents = get_adj_points(adjacent_points, dimensions, coordinate)
        
        #for each point, create the adjacent points
        for point in adjacents:
            #get the value of the point, and if it is a bomb, pass
            if get_value_from_coordinate(board, point) == '.':
                pass
            else:
                #if it isn't a bomb, it is near the bomb, so change the value by 1
                set_point(board, point, get_value_from_coordinate(board, point)+1)

    return {'dimensions': dimensions, 'board' : board, 'mask' : mask, 'state': 'ongoing'}


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """
    #initialize variables
    dimensions, board, mask = game['dimensions'], game['board'], game['mask']
    value = get_value_from_coordinate(board, coordinates)
    uncovered = 0

    #if the coordinate has been checked, or the game has been won or lost, return the revealed value
    if get_value_from_coordinate(mask, coordinates) or game['state'] == 'victory' or game['state'] == 'defeat':
        return uncovered

    #if the value equal to 0,
    adjacent_points = []
    uncovered += 1
    set_point(mask, coordinates, True)
    
    if value == 0:
        #helper function on all adjacents if 0
        for point in get_adj_points(adjacent_points, dimensions, coordinates):
            temp = zero_checker(game, point)
            uncovered += temp
    #if the bomb has been found, game is over
    elif value == '.':
        game['state'] = 'defeat'
        return uncovered
    
    #check game state to see if game has been won
    if check_state(board, mask, dimensions) == 'victory':
        game['state'] = 'victory'
            
    return uncovered


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    #initialize variables
    board, mask, dimensions = game['board'], game['mask'], game['dimensions']
    result = initialize(dimensions, 0)

    #for each point in all the possible points
    for point in all_possible_points([], dimensions):
        #obtain the value of the mask and the coordinate
        value_mask = get_value_from_coordinate(mask, point)
        value_coord = get_value_from_coordinate(board, point)
        #if the mask is False and the xray is False
        if not value_mask and not xray:
            set_point(result, point, '_')
                
        #if the value of the coordinate is 0
        elif value_coord == 0:
            set_point(result, point, ' ')
        
        #if the value of the coordinate is not 0 or True
        elif value_coord != 0 or value_mask:
            set_point(result, point, str(value_coord))
    
    return result


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    #doctest.run_docstring_examples(render_2d, globals(), optionflags=_doctest_flags, verbose=False)
