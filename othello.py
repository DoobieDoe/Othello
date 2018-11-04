# Reversi

import random
import sys

def drawNode(node):
    file = open("träd.txt","a") 
    
    HLINE = '  +---+---+---+---+---+---+---+---+\n'
    VLINE = '  |   |   |   |   |   |   |   |   |\n'

    file.write('    1   2   3   4   5   6   7   8\n')
     
    file.write(HLINE)
    for y in range(8):
        #file.write(VLINE)
        file.write(str(y+1) + ' ')
        for x in range(8):
            file.write('| ' + node.board[x][y] + ' ')
        file.write('|\n')
        #file.write(VLINE)
        file.write(HLINE)

    #file.write('\n')
    file.write('Score for ' + node.turn + ': ' + str(node.score) + '\n\n')
    file.close

def drawBoard(board):
    file = open("träd.txt","a") 
    
    HLINE = '  +---+---+---+---+---+---+---+---+\n'
    VLINE = '  |   |   |   |   |   |   |   |   |\n'

    file.write('    1   2   3   4   5   6   7   8\n')
     
    file.write(HLINE)
    for y in range(8):
        #file.write(VLINE)
        file.write(str(y+1) + ' ')
        for x in range(8):
            file.write('| ' + board[x][y] + ' ')
        file.write('|\n')
        #file.write(VLINE)
        file.write(HLINE)

    file.write('\n')
    file.close

def resetBoard(board):
    # Blanks out the board it is passed, except for the original starting position.
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def getNewBoard():
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([' '] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' ' # restore the empty space
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <=7


def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

def getScoreForPlayer(board, player):
    score = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == player:
                score += 1
    return score

def enterPlayerTile():
    return ['X', 'O']

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
    # Let the player type in their move.
    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the top-right corner.')

    return [x, y]


def getComputerMove(board, computerTile):
    '''
    possibleMoves = getValidMoves(board, computerTile)
    tree = 
    for move in possibleMoves:
        moveScores = minMaxValue(move, board, computerTile)

    return max(moveScores.iterkeys(), key=(lamda key: moveScores[key]))
    '''

    possibleMoves = getValidMoves(board, computerTile)
    tree = Node(board, computerTile)
    addChildrenAndSetScores(tree, computerTile)
    traverse(tree)
    #findMaxMove(tree, computerTile)
    return (1, 1)

'''
def minMaxValue(move, board, turn):
    possibleMoves = getValidMoves(board, turn)
    if len(possibleMoves) == 0
        return getScoreForPlayer(board, turn)

    if player 1's turn
		return highest value of children

	if player 2's turn
		return lowest value of children
'''
def addChildrenAndSetScores(node, turn):
    possibleMoves = getValidMoves(node.board, turn)
    
    if len(possibleMoves) == 0:
        node.score = getScoreForPlayer(node.board, turn)
        return

    minScoreOfChildren = 100
    maxScoreOfChildren = 0
    for (x, y) in possibleMoves:
        print((x, y))
        childBoard = getBoardCopy(node.board)
        makeMove(childBoard, turn, x, y)

        if turn == computerTile:
            childTurn = playerTile
        else:
            childTurn = computerTile

        childScore = getScoreForPlayer(childBoard, turn)

        # if computerturn then maximize
        if turn == computerTile:
            if childScore > maxScoreOfChildren:
                maxScoreOfChildren = childScore
        # if player turn then minimize
        else:
            if childScore < minScoreOfChildren:
                minChildScoreOfChildren = childScore
        
        childNode = Node(childBoard, childTurn)
        node.add_child(childNode)
        childNode.score = childScore
        
        addChildrenAndSetScores(childNode, childTurn)

    if turn == computerTile:
        node.score = maxScoreOfChildren
    else:
        node.score = minChildScoreOfChildren

    

    


def traverse(node):
    if len(node.children) == 0:
        drawNode(node)
    else:
        for child in node.children:
            traverse(child)
        drawNorde(node)


class Node(object):
    
    def __init__(self, board, turn):
        self.board = board 
        self.turn = turn
        self.children = []        

    def add_child(self, node):
        self.children.append(node)



'''
    alpha = -9999
    beta = 9999
    depth = 100
    tree = Node(board, computerTile)
    alphabeta(tree, computerTile, depth, alpha, beta, True)
 
def alphabeta(node, turn, depth, alpha, beta, maximizingPlayer):
    possibleMoves = getValidMoves(board, turn)    
    addChildren(tree, computerTile)


    if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
            α := max(α, value)
            if α ≥ β then
                break (* β cut-off *)
        return value
    else
        value := +∞
        for each child of node do
            value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
            β := min(β, value)
            if α ≥ β then
                break (* α cut-off *)
        return value

'''

def showPoints(playerTile, computerTile):
    # Prints out the current score.
    scores = getScoreOfBoard(mainBoard)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))


sys.setrecursionlimit(10000)

print('Welcome to Reversi!')

while True:
    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    #turn = whoGoesFirst()
    turn = 'computer'
    print('The ' + turn + ' will go first.')

    while True:
        if turn == 'player':
            # Player's turn.
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                #drawBoard(validMovesBoard)
            #else:
                #drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            move = getPlayerMove(mainBoard, playerTile)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit() # terminate the program
            elif move == 'hints':
                showHints = not showHints
                continue
            else:
                makeMove(mainBoard, playerTile, move[0], move[1])

            if getValidMoves(mainBoard, computerTile) == []:
                break
            else:
                turn = 'computer'

        else:
            # Computer's turn.
            #drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            input('Press Enter to see the computer\'s move.')
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)

            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'

    # Display the final score.
    #drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tie!')

    if not playAgain():
        break
