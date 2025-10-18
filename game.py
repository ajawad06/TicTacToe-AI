# TIC TAC TOE using MINIMAX & ALPHA-BETA PRUNING
import math
import copy
import random

X="X"
O="O"
EMPTY=None

# return starting state of game board
def initialState():
    return [[EMPTY,EMPTY,EMPTY],
            [EMPTY,EMPTY,EMPTY],
            [EMPTY,EMPTY,EMPTY]]

# print board
def printBoard(board):
    for row in board:
        print(row)

# returns player who has the next turn
def player(board):
    count=0
    for i in board:
        for j in i:
            if j:
                count+=1

    if count%2!=0:
        return O
    return X

# returns set of possible actions (i,j) on a certain state of board
def actions(board):
    possible_actions=set()
    n=len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j]==EMPTY:
                possible_actions.add((i,j))

    return possible_actions

# returns a resultant board after performing a action (i,j)
def result(board,action):
    current_player=player(board)
    result_board=copy.deepcopy(board)
    (i,j)=action
    result_board[i][j]=current_player
    return result_board

def check_horizontal_winner(board):
    winner_val=None
    n=len(board)
    for i in range(n):
        winner_val=board[i][0]
        for j in range(n):
            if winner_val!=board[i][j]:
                winner_val=None
        if winner_val:
            return winner_val
    return winner_val

def check_vertical_winner(board):
    winner_val=None
    n=len(board)
    for i in range(n):
        winner_val=board[0][i]
        for j in range(n):
            if winner_val!=board[j][i]:
                winner_val=None
        if winner_val:
            return winner_val
    return winner_val

def check_diagonal_winner(board):
    n = len(board)
    # 1st diagonal
    winner_val = board[0][0]
    if winner_val is not None:
        win=True
        for i in range(n):
            if board[i][i]!=winner_val:
                win=False
                break
        if win:
            return winner_val
    

    # 2nd diagonal
    winner_val=board[0][n-1]
    if winner_val is not None:
        win=True
        for i in range(n):
            if board[i][n-i-1] != winner_val:
                win = False
                break
        if win:
            return winner_val
    
    return None

# returns X or O depending on winner
def winner(board):
    winner_player=check_horizontal_winner(board) or check_vertical_winner(board) or check_diagonal_winner(board) or None
    return winner_player


# returns true if game is over and false otherwise
def terminal(board):
    if winner(board)!=None:
        return True
    
    n = len(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] == EMPTY:
                return False
            
    return True

# returns 1 if X wins, 0 if draw and -1 if O wins
def utility(board):
    winner_val=winner(board)
    if winner_val==X:
        return 1
    elif winner_val==O:
        return -1
    else:
        return 0

# max value function for minimax
def max_value(board,alpha,beta):
    if terminal(board):
        return utility(board)
    v=-math.inf
    for action in actions(board):
        if alpha<beta:
            v=max(v,min_value(result(board,action),alpha,beta))
            if alpha<v:
                alpha=v
    return v

# min value function for minimax
def min_value(board,alpha,beta):
    if terminal(board): 
        return utility(board)
    v=math.inf
    for action in actions(board):
        if alpha<beta:
            v=min(v,max_value(result(board,action),alpha,beta))
            if beta>v:
                beta=v
    return v

# returns optimal function for current player
def minimax(board):
    # 1. If board is empty, AI picks random move
    if board==initialState():
        return (random.randint(0,2),random.randint(0,2))
    
    # 2. Get the current player
    currPlayer=player(board)
    action_to_return=None
    
    # 3.1 Case: Player X – Since X is the maximizing player, we evaluate all possible moves it can make. 
    # For each move, we assume the opponent (O) will play optimally, so we calculate the minimum utility
    # that X could get from O’s responses. After considering all moves, X chooses the move that gives the 
    # maximum of these minimum values.
    if currPlayer==X:
        val=-math.inf
        for action in actions(board):
            min_res=min_value(result(board,action))
            if val<min_res:
                val=min_res
                action_to_return=action

    # 3.2 Case: Player O – Since O is the minimizing player, we evaluate all possible moves it can make. 
    # For each move, we assume the opponent (X) will play optimally, so we calculate the maximum utility
    # that O could get from X’s responses. After considering all moves, O chooses the move that gives the 
    # minimum of these maximum values.   
    elif currPlayer==O:
        val=math.inf
        for action in actions(board):
            max_res=max_value(result(board,action))
            if val<max_res:
                val=max_res
                action_to_return=action
    
    return action_to_return

# returns optimal function for current player using pruning
def alpha_beta(board):
    alpha=-math.inf
    beta=math.inf

    # 1. If board is empty, AI picks random move
    if board==initialState():
        return (random.randint(0,2),random.randint(0,2))
    
    # 2. Get the current player
    currPlayer=player(board)
    action_to_return=None

    # 3.1 X player
    if currPlayer==X:
        val=-math.inf
        for action in actions(board):
            if alpha<beta:
                min_val_res=min_value(result(board,action),alpha,beta)
                if val<min_val_res:
                    val=min_val_res
                    action_to_return=action
                    alpha = max(alpha, val) 

    # 3.2 O player  
    elif currPlayer==O:
        val=math.inf
        for action in actions(board):
            if alpha<beta:
                max_val_res=max_value(result(board,action),alpha,beta)
                if val>max_val_res:
                    val=max_val_res
                    action_to_return=action
                beta = min(beta, val)
    
    return action_to_return


def main():
    board=initialState()
    user=None
    while user not in ["X", "O"]:
        user = input("Choose X or O: ").upper()

    printBoard(board)
    while True:
        # 1. If game over, display result
        if terminal(board):
            win = winner(board)
            if win:
                print(f"Game Over: {win} wins!")
            else:
                print("Game Over: It's a tie!")

            print("Game Successful using Alpha Beta Pruning!")
            break

        current_turn = player(board)

        # 2. If user turn, ask for move
        if current_turn == user:
            # Human move
            print("\nYour turn:")
            row = int(input("Row: "))
            col = int(input("Col: "))
            if board[row][col] == EMPTY:
                board = result(board, (row, col))
              
        # 3. If AI turn, use a-b prune function
        else:
            # AI move
            print("\nAI is thinking...")
            move = alpha_beta(board)
            board = result(board, move) 

        print()
        printBoard(board)

main()
