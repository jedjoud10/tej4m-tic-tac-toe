import copy
computerPlaying = "1"
opposingPlayer = "2"
turnTaken = False

def printBoard(gameState):
    print(gameState[0])
    print(gameState[1])
    print(gameState[2])

def gameWon(gameState):
    for x in range(3):
        s = "".join([gameState[x][0], gameState[x][1], gameState[x][2]])
        t = "".join([gameState[0][x], gameState[1][x], gameState[2][x]])
        if s == "111" or s == "222" or t == "111" or t == "222":
            if s == "222" or t == "222":
                return(True, 2)
            else:
                return(True, 1)
    a = gameState[0][0] == gameState[1][1] and gameState[0][0] == gameState[2][2]
    b = gameState[2][0] == gameState[1][1] and gameState[2][0] == gameState[0][2]       
    if a or b:
        return (True, int(gameState[1][1]))

    return (False, 0)

def checkHorizontal(player, board):
    #checking horizontal win possibilities
    move = None
    for x in range(3):
        row = board[x]
        for y in range(3):
            if (row[y] == row[y-1] and row[y] == player):
                #return the location that should be changed and the change made
                if (y+1 == 3):
                    move = [x, 0]
                else:
                    move = [x, y+1]
                #if the box is filled, resets the move
                if board[move[0]][move[1]] != "0":
                    move = None
    return(move)

def checkVertical(player, board):
    #checking vertical win possibilities
    move = None
    for x in range(3):
        for y in range(3):
            if(board[y][x] == board[y-1][x] and board[y][x] == player):
                #return location that should be changed
                if (y+1 == 3):
                 move = [0, x]
                else:
                    move = [y+1, x]
                #if the box is filled, resets the move
                if board[move[0]][move[1]] != "0":
                    move = None
    return(move)

def checkDiagonal(player, board):
    a = [0, 2]
    b = [0, 2]
    move = None
    for x in range(2):
        for y in range(2):
            if (board[a[x]][b[y]] == player and board[a[x-1]][b[y-1]] == player):
                #if opposing corners are free, go for the center
                move = [1, 1]
    return(move)

def checkCompleteLine(player, gameState):
    if checkHorizontal(player, gameState) is None:
        if checkVertical(player, gameState) is None:
            if checkDiagonal(player, gameState) is None:
                return(False)
            else:
                 gameState[checkDiagonal(player, gameState)[0]][checkDiagonal(player, gameState)[1]] = computerPlaying
                 return(True)
        else:
            gameState[checkVertical(player, gameState)[0]][checkVertical(player, gameState)[1]] = computerPlaying
            return(True)
    else:
        gameState[checkHorizontal(player, gameState)[0]][checkHorizontal(player, gameState)[1]] = computerPlaying
        return(True)

def countFork(player, gameState):
    result = None, None
    for x in range(3):
        for y in range(3):
            winCount = 0
            jameState = copy.deepcopy(gameState)
            jameState[x][y] = player
            if checkDiagonal(player, jameState) != None:
                winCount += 1
            if checkHorizontal(player, jameState) != None:
                winCount += 1
            if checkVertical(player, jameState) != None:
                winCount += 1
            if winCount >= 2:
                if (jameState[x][y] == "0"):
                    return(x, y)
    return(result)

def oppCorner(gameState):
    if gameState[0][0] == opposingPlayer and gameState[2][2] == "0":
        return(2, 2)
    elif gameState[0][2] == opposingPlayer and gameState[2][0] == "0":
        return(2, 0)
    elif gameState[2][0] == opposingPlayer and gameState[0][2] == "0":
        return(0, 2)
    elif gameState[2][2] == opposingPlayer and gameState[0][0] == "0":
        return(0, 0)
    else:
        return(None, None)

def findCorner(gameState):
    if gameState[0][0] == "0":
        return(0, 0)
    elif gameState[2][0] == "0":
        return(2, 0)
    elif gameState[0][2] == "0":
        return(0, 2)
    elif gameState[2][2] == "0":
        return(2, 2)
    return(None, None)

def findSide(gameState):
    if gameState[0][1] == "0":
        return(0, 1)
    elif gameState[1][0] == "0":
        return(1, 0)
    elif gameState[2][1] == "0":
        return(2, 1)
    elif gameState[1][2] == "0":
        return(1, 2)
    return(None, None)

def isBoardFull(gameState):
    for x in range(3):
        for y in range(3):
            if gameState[x][y] == "0":
                return(False, x, y)
    return(True, None, None)

def takeTurn(gameState):
    #check for WIN
    turnTaken = False
    
    #check if game is over at the start and end of turn
    isWin, Winner = gameWon(gameState)
    if isWin == True:
        turnTaken = True
        print("GAME OVER", Winner, "won")

    #Priority 1: win
    if turnTaken == False:
        turnTaken = checkCompleteLine(computerPlaying, gameState)

    #Priority 2: block other player's win
    if turnTaken == False:
        turnTaken = checkCompleteLine(opposingPlayer, gameState)

    #Priority 3: create a fork
    if turnTaken == False:
        x, y = countFork(computerPlaying, gameState)
        if (x != None):
            gameState[x][y] = computerPlaying
            turnTaken = True
    
    #Priority 4: block opponent's fork
    if turnTaken == False:
        x, y = countFork(opposingPlayer, gameState)
        if (x != None):
            gameState[x][y] = computerPlaying
            turnTaken = True

    #Priority 5: mark cneter
    if turnTaken == False:
        if gameState[1][1] == "0":
            gameState[1][1] = computerPlaying
            turnTaken = True
    
    #Priority 6: play in opposite corner to opposing playter
    if turnTaken == False:
        x, y = oppCorner(gameState)
        if x != None:
            gameState[x][y] = computerPlaying
            turnTaken = True

    #Priority 7: play in an empty corner
    if turnTaken == False:
        x, y = findCorner(gameState)
        if x != None:
            gameState[x][y] = computerPlaying
            turnTaken = True

    #Priority 8: play in an empty side
    if turnTaken == False:
        x, y = findSide(gameState)
        if x != None:
            gameState[x][y] = computerPlaying
            turnTaken = True
    
    #Check if board is full
    if turnTaken == False:
        boardFull, x, y = isBoardFull()
        if boardFull == True:
            isWin, Winner = gameWon(gameState)
            if isWin == True:
                print("GAME OVER", Winner, "won")
            else:
                print("TIE")
        else:
            gameState[x][y] = computerPlaying

#currentBoard = [["2", "1", "2"], ["2", "1", "2"], ["1", "1", "1"]]
#takeTurn(currentBoard)
#printBoard(currentBoard)
