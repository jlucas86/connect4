import random
import copy

import pygad
import numpy

# starts game by making the user choice what type of players they want
# to play
# the random player makes random moves and is mostly for testing
# player means the user is that player
# AI is an ai that chices its moves bsed on the minimax algorithm

def start(): 
    global p1
    global p2
    global board
    print("Select the type of player for player one")
    p1 = input("Type 1 for AI, 2 for Player, or 3 for Random:")
    i=0
    while i == 0:
        p1 = int(p1) 
        if p1 == 1 or p1 == 2 or p1 == 3:
            i = 1
        else:
            print("Error Please enter a valid number")
            p1 = input("Type 1 for AI, 2 for Player, or 3 for Random:")


    print("Select the type of player for player two:")
    p2 = input("Type 1 for AI, 2 for Player, or 3 for Random:")
    i=0
    while i == 0:
        p2 = int(p2) 
        if p2 == 1 or p2 == 2 or p2 == 3:
            i = 1
        else:
            print("Error Please enter a valid number")
            p2 = input("Type 1 for AI, 2 for Player, or 3 for Random:")

    print(p1, "vs", p2)

    board = ["c1","c2","c3","c4","c5","c6","c7"]
    for i in range(0,7):
        board[i] = ["-","-","-","-","-","-"]

# initulizes the game, tracks witch players turn it is and the board stat
# 

def game(p1,p2, Sset ):
    global board
    global win

    board = ["c1","c2","c3","c4","c5","c6","c7"]
    for i in range(0,7):
        board[i] = ["-","-","-","-","-","-"]
    win = False

    turnCount= 0

    turn = random.randint(1,2)
    while win == False:
        if turn == 1:
            if p1 == 1:
                AI(turn, Sset)
            elif p1 == 2:
                player(turn)
            else:
                rand(turn)
            turn = 2
            turnCount = turnCount+1
        else:
            if p2 == 1:
                AI(turn, Sset)
            elif p2 == 2:
                player(turn)
            else:
                rand(turn)
            turn = 1
            turnCount = turnCount+1

        printBoard(board)
        if turnCount == 42:
            return 3, turnCount
    if turn == 1:
        print("winner: player", turn+1, "!!!!")
        return turn+1,turnCount
    else:
        print("winner: player", turn-1, "!!!!")
        return turn-1,turnCount
    
    
    
        
# makes sure no rules are being broke and determins if 
# the board id at a win state
# b is the curent board
# t is the players turn

def rules(m, b):

    if b[m][5] != "-":
        return False
    else:
        return True



    print("not ready")
    return False


def place(t, m, b):
    i = 0
    while i != -1:
        if b[m][i] == "-":
            if t == 1:
                b[m][i] = "X"
            else:
                b[m][i] = "O"
            i = -1
        else:
            i = i+1
    return

def checkWin(t,m, b):

    global board

    # deter mine what symbole to test for based on turn
    if t == 1:
        sym = "X"  
    else:
        sym = "O"

    i = 5 # index number used to find the row the new piece is in
    while i > -1:
        if board[m][i] == sym:
            
            # check vertical
            if i >= 3:    
                if board[m][i-1] == sym and board[m][i-2] == sym and board[m][i-3] == sym:
                    return True
            
            # check horivontal
            total = 0 
            j = m

            # checks for matching pieces to the left of the piece
            while j+1 < 7: 
                if board[j+1][i] == sym:
                    total = total + 1
                    j = j + 1
                else:
                    j = 7
            j = m

            # checks for matching pieces to the right of the piece
            while j-1 > -1: 
                if board[j-1][i] == sym:
                    total = total + 1
                    j = j - 1
                else:
                    j = -1
            if total >= 3: # if there is 3 or more pice surounding the new pice
                return True

            # check diagonal left
            total = 0 
            j = m
            k = i

            # checks for matching pieces to the left and down from the piece
            while j+1 < 7 and k-1 > -1: 
                if board[j+1][k-1] == sym:
                    total = total + 1
                    j = j + 1
                    k = k - 1
                else:
                    j = 7
            j = m
            k = i

            # checks for matching pieces to the right and up from the piece
            while j-1 > -1 and k+1 < 6: 
                if board[j-1][k+1] == sym:
                    total = total + 1
                    j = j - 1
                    k = k + 1
                else:
                    j = 0
            if total >= 3: # if there is 3 or more pice surounding the new pice
                return True


            # check diagonal right
            total = 0 
            j = m
            k = i

            # checks for matching pieces to the left and up from the piece
            while j+1 < 7 and k+1 < 6: 
                if board[j+1][k+1] == sym:
                    total = total + 1
                    j = j + 1
                    k = k + 1
                else:
                    j = 7
            j = m
            k = i

            # checks for matching pieces to the right and down from the piece
            while j-1 > -1 and k-1 > -1: 
                if board[j-1][k-1] == sym:
                    total = total + 1
                    j = j - 1
                    k = k - 1
                else:
                    j = 0
            if total >= 3: # if there is 3 or more pice surounding the new pice
                return True

            # if they don't find a win state return false
            return False

        else:
            i = i-1
        



    

    return False


# prints the board state

def printBoard(b):
    board = b
    i = 5
    while i != -1: # row
        for j in range(0,7): # colmnb
            print("|", board[j][i], end =" ")
        print("|")
        i = i-1
    
    return

# all AI Stuff
# -------------------------------------------------------------------------------

class node:
    
    def __init__(self, id, value, choices):
        self.value = value
        self.id = id
        self.choices = choices
    



# function that holds paramiters for the AI, starts minimax tree
# also, places the value that the in the best spot of the board.

def AI(t, trainer):
    global win
    global board

    level = 4 # number of levels in the minimax algo
    root = node(0,0,[])
    b = copy.deepcopy(board)
    minimax(t, level, 0, root, b, trainer) # holds the best move to make
    move = 0
    for i in root.choices: #determin which columb to place piece
        if root.value == i.value:
            move = i.id
    print( "player", t,"AI")
    print( "--------------------------------------------")
    place(t, move, board)
    win = checkWin(t, move, board)
    del root
    return


# minimax algorithm
# uses 
# if the leve value is odd the maximum value is returned
# else min is returned

def minimax(t, ml, l, n, b, trainer):

    if ml == l: # at leaf nodes, determin value trough heuristic then return
        if t == 1:
            n.value = heuristic(t, b, trainer)
        else:
            n.value = heuristic(t, b, trainer)
        return
    
    # go through each cloumb and determin weather or not the move is valid 
    # if valid create a new node and add it to list of choices
    # else ignore value 

    
    i = 0
    while i < 7:
        if rules(i, b) == True: 
            #create new node in tree and add node to list of children
            
            hold = node(i,0,[])
            #create copy of board and add new move
            board1 = copy.deepcopy(b)
            place(t, i, board1)
            #printBoard(board1)
            # call minimax function on next node with updated board
            # the turn is alos changer
            if t == 1:
                minimax(t+1, ml, l+1, hold, board1, trainer)
            else:
                minimax(t-1, ml, l+1, hold, board1, trainer)
            n.choices.append(hold)
            del hold
            
        # increment i
        i= i+1

    # go trough children and find the value you want to equate with the node
    #  if l%2 == ml%2 pick max value
    # else pick min value
    #print("level", l)
    max = -100
    min = 100
    for j in n.choices:
        #if l == 2:
            #print("posible choices id", j.id,"value of parent",n.value, "value of leaf",j.value)
        
        if l%2 != ml%2: #min
            if min > j.value:
                n.value = j.value
                min = j.value
        else: #max
            if max < j.value:
                n.value = j.value
                max = j.value
    
    #1
    #print(n.value)
        
    return
        
# adds value for difretn board stated 
# valus for state of board determined using machine learning based on
# p == player turn
# b == board
# returns a numeric value where negative is in favor of the opponet and
# possitive is in favor of the player

def heuristic(p, b, trainer):
    #print("this is p;ayer", p)
    
    # player symboles
    p1s = "X"
    p2s = "O"

    # defin opont symbole and playe symbol

    if p == 1:
        player = p1s
        opponent = p2s
    else:
        player = p2s
        opponent = p1s

    # variable that will account for the value being returned
    # intiulized to 0 as a neutral
    value = 0
    valueP = 0
    valueOP = 0


    #itorate through each piece on the board and check state

    i = 0 # index for x-axis

    while i < 7:
        j = 0 # index for y-axis
        while j < 6:

            
            # check vertical
            if j == 0:

                # variable to use as place holders
                j1 = j
                countvOP = 0
                countvP = 0
                while j1 < 6 :

                    if b[i][j1] == "-":
                        j1 = 6
                    elif b[i][j1] == opponent:
                        
                        countvP = 0
                        countvOP = countvOP + 1
                        # opponent wins
                        if countvOP == 4:
                            return trainer[26]*-1
                    
                    else:

                        countvOP = 0
                        countvP = countvP + 1
                       
                    j1 = j1 + 1
                
                # setting values
                if countvP > 0:
                    hold=VPpoints(countvP, trainer)
                    if hold > valueP:
                        valueP = hold
                if countvOP > 0:
                    hold=VOPpoints(countvOP, trainer)
                    if hold > valueOP:
                        valueOP = hold

                

            # check horizontal
            if i == 0:
                
                # index used to go through row
                i1 = i

                while i1 < 4:
                    #place holder for value while calculating
                    holdp = 0
                    holdop = 0
                    
                    #check values in chuncks of 4 of current board
                    hold1 = [b[i1][j], b[i1+1][j], b[i1+2][j], b[i1+3][j]]
                    hold2 = [board[i1][j], board[i1+1][j], board[i1+2][j], board[i1+3][j]]
                    #if there is any of opponent and player set value to 0
                    if player in hold1 and opponent in hold1:
                        # compare current board state to actual board
                        # to detect a blocked win i.e. 

                        #if boards samples are the same set value to zero
                        if hold1 == hold2:
                            holdp = 0 
                            holdop = 0

                        #if boards samples are not the same check for a block
                        #player blocks win
                        elif hold1[0] == opponent and hold1[1] == opponent and hold1[2] == opponent:
                            holdp = trainer[13] 

                        #opponet bloacks win
                        elif hold1[0] == player and hold1[1] == player and hold1[2] == player:
                            holdop = trainer[27] 

                        # no win blocked
                        else:
                            holdp = 0 
                            holdop = 0


                        
                    #if there is 1 pieces and 3 gaps value = ph1 or oph1
                    elif hold1.count("-") == 3:
                        if player in hold1:
                            holdp = trainer[3]
                        elif opponent in hold1:
                            holdop = trainer[17]
                    #if there is 2 pieces and 2 gaps value = ph2 or oph2
                    elif hold1.count("-") == 2:
                        if player in hold1:
                            holdp = trainer[4]
                        elif opponent in hold1:
                            holdop = trainer[18]
                    #if there is 3 pieces and 1 gaps value = ph3 or oph3
                    elif hold1.count("-") == 1:
                        if player in hold1:
                            holdp = trainer[5]
                        elif opponent in hold1:
                            holdop = trainer[19]
                    #if there is 4 pieces and 0 gaps value = pWin or return opWin
                    elif hold1.count("-") == 0:
                        if player in hold1:
                            holdp = trainer[12]
                        elif opponent in hold1:
                            holdop = trainer[26]
                            return holdop*-1 
                    #determin which is higher then compar to the value already being used.
                    if holdop > holdp:
                        if valueOP < holdop:
                            valueOP = holdop
                    else:
                        if valueP < holdp:
                            valueP = holdp

                    #increment i1
                    i1 = i1 + 1


            # check diagonal up and right

            # make sure there can be 4 up and 4 to the right
            if i < 4 and j < 3:

                #place holder for value while calculating
                holdp = 0
                holdop = 0

                # get a group of 4
                hold1 = [b[i][j], b[i+1][j+1], b[i+2][j+2], b[i+3][j+3]]
                hold2 = [board[i][j], board[i+1][j+1], board[i+2][j+2], board[i+3][j+3]]
                # if there is atleast one of both player and opponent assign value to 0
                if player in hold1 and opponent in hold1:
                    # compare current board state to actual board
                    # to detect a blocked win i.e. 

                    #if boards samples are the same set value to zero
                    if hold1 == hold2:
                        holdp = 0 
                        holdop = 0

                    #if boards samples are not the same check for a block
                    #player blocks win
                    elif hold1[0] == opponent and hold1[1] == opponent and hold1[2] == opponent:
                        holdp = trainer[13] 

                    #opponet bloacks win
                    elif hold1[0] == player and hold1[1] == player and hold1[2] == player:
                        holdop = trainer[27] 

                    # no win blocked
                    else:
                        holdp = 0 
                        holdop = 0
                # if there is one of a kind and 3 gaps
                elif hold1.count("-") == 3:
                    if player in hold1:
                        holdp = trainer[6]
                    elif opponent in hold1:
                        holdop = trainer[20]
                # if there are two of a kind and 2 gaps
                elif hold1.count("-") == 2:
                    if player in hold1:
                        holdp = trainer[7]
                    elif opponent in hold1:
                        holdop = trainer[21]
                # if ther are three of a kind and 1 gap
                elif hold1.count("-") == 1:
                    if player in hold1:
                        holdp = trainer[8]
                    elif opponent in hold1:
                        holdop = trainer[22]
                # if a win state is detected auto retur for oponent win
                elif hold1.count("-") == 0:
                    if player in hold1:
                        holdp = trainer[12]
                    elif opponent in hold1:
                        holdop = trainer[26]
                        return hold*-1
                #determin which is higher then compar to the value already being used.
                if holdop > holdp:
                    if valueOP < holdop:
                        valueOP = holdop
                else:
                    if valueP < holdp:
                        valueP = holdp

            # check diagonal down and right

            # make sure there can be 4 down and 4 to the right
            if i < 4 and j > 2:

                #place holder for value while calculating
                holdp = 0
                holdop = 0 # fix alows for easy wins

                # get a group of 4
                hold1 = [b[i][j], b[i+1][j-1], b[i+2][j-2], b[i+3][j-3]]
                hold2 = [board[i][j], board[i+1][j-1], board[i+2][j-2], board[i+3][j-3]]
                # if there is atleast one of both player and opponent assign value to 0
                if player in hold1 and opponent in hold1:
                    # compare current board state to actual board
                    # to detect a blocked win i.e. 

                    #if boards samples are the same set value to zero
                    if hold1 == hold2:
                        holdp = 0 
                        holdop = 0

                    #if boards samples are not the same check for a block
                    #player blocks win
                    elif hold1[0] == opponent and hold1[1] == opponent and hold1[2] == opponent:
                        holdp = trainer[13] 

                    #opponet bloacks win
                    elif hold1[0] == player and hold1[1] == player and hold1[2] == player:
                        holdop = trainer[27] 

                    # no win blocked
                    else:
                        holdp = 0 
                        holdop = 0
                # if there is one of a kind and 3 gaps
                elif hold1.count("-") == 3:
                    if player in hold1:
                        holdp = trainer[9]
                    elif opponent in hold1:
                        holdop = trainer[23]
                # if there are two of a kind and 2 gaps
                elif hold1.count("-") == 2:
                    if player in hold1:
                        holdp = trainer[10]
                    elif opponent in hold1:
                        holdop = trainer[24]
                # if ther are three of a kind and 1 gap
                elif hold1.count("-") == 1:
                    if player in hold1:
                        holdp = trainer[11]
                    elif opponent in hold1:
                        holdop = trainer[25]
                # if a win state is detected auto retur for oponent win
                elif hold1.count("-") == 0:
                    if player in hold1:
                        holdp = trainer[12]
                    elif opponent in hold1:
                        holdop = trainer[26]
                        return hold*-1
                #determin which is higher then compar to the value already being used.
                if holdop > holdp:
                    if valueOP < holdop:
                        valueOP = holdop
                else:
                    if valueP < holdp:
                        valueP = holdp
            #increment vertival
            j = j + 1
        #increment horizontal
        i = i + 1
    
    #determin which value to return
    if valueP > valueOP:
        value = valueP
    else:
        value = valueOP * -1
    #print("this is returned value", value)

    return value


    

def VPpoints(a, trainer):

    switcher = {
        1:trainer[0],
        2:trainer[1],
        3:trainer[2],
        4:trainer[12]
    }
    return switcher.get(a,0)

def VOPpoints(a, trainer):

    switcher = {
        1:trainer[14],
        2:trainer[15],
        3:trainer[16]
    }
    return switcher.get(a,0)



# END AI
#-----------------------------------------------------------------------------

def rand(t):
    global win
    global board

    print( "player", t,"randome player")
    print( "--------------------------------------------")
    rulling = False
    while rulling == False:
        move = random.randint(0,6)
        rulling = rules(move, board)
    place(t,move, board)
    win = checkWin(t, move, board)

    

def player(t):
    global win 
    global board

    print( "player", t)
    print( "--------------------------------------------")
    move = input("choose the colunb to drop your chip:") 
    move = int(move)-1
    rulling = False
    while rulling == False:
        i = False
        while i == False:
            if move > 6 or move < 0:
                print("ERROR")
                move = input("please choose a valid colunb to drop your chip:")
                move = int(move)-1
            else:
                i = True
            
        rulling = rules(move, board)
    place(t, move, board)
    win = checkWin(t, move, board)




p1 = None #player one type
p2 = None #player one type
board = None 
win = False
# board is a list with 7 nested lists
# the outer list represents columns and the  inner list represents rows

# board[0][n] ------> board[6][n]
# | - | - | - | - | - | - | - | board[n][5]
# | - | - | - | - | - | - | - |
# | - | - | - | - | - | - | - |
# | - | - | - | - | - | - | - |
# | - | - | - | - | - | - | - |
# | - | - | - | - | - | - | - |  board[n][0]


# value assigned to difrent stated in the hyuristic
trainerSet = [1,2,5,1,2,3,1,2,5,1,2,4,15,10,1,2,6,1,3,7,1,2,6,1,2,6,30,20]
#trainerSet2 = [-2.99400644,  5.92230696, -0.42301532, -2.67481924,  0.31886061,  1.40693725,3.26969297,  4.24051469,  2.96972973,  1.44904858,  0.39713142,  0.42696471,-0.94280505, -2.60055002, -2.50949234, -2.41009439,  2.77167538, -4.30529845, 0.0787161,  -1.61145266,  4.03260016, -3.53699484, -1.10208284,  2.26496525,-1.13947445,  3.17959487,  0.8646078,  -3.46059956]
trainerSet3 = [ 3.18413636,  2.8984671,  -3.77324805, -1.06333681,  0.09326676,  1.26644788,
    -2.80517403,  1.51658984, -2.69972569, -2.7140356,   2.36278517, -0.35967965,
    -3.04878961,  3.71754146,  3.811102,    0.29308778, -2.80009347, -2.9263032,
    1.5068292,  -2.81978421,  0.19276,     0.63397554,  3.809857,    2.95726062,
    -1.99512598, -3.08175769, -3.83479188, -2.84797605]
trainerSet4 = [-2.72171517,  1.92554469, -0.19880063,  3.07851452,  1.74363364,  2.21034002,       
  3.86176211,  3.75077792, -1.5618922,   2.29772829,  0.71351073,  1.49612079,
 -1.47777475,  3.54862305,  3.71728857, -2.89347585, -4.35676747,  2.06267105,
  2.7446313,   1.24488257,  1.83714551,  1.25352113, -0.40124741,  0.33813772,
  2.61303777, -4.89763556, -3.59750382,  1.35274915,]

for x in range(len(trainerSet)):
    trainerSet4[x] = trainerSet4[x]*trainerSet3[x]
    

pv1 = 1
pv2 = 2
pv3 = 5

ph1 = 1
ph2 = 2
ph3 = 3

pdu1 = 1
pdu2 = 2
pdu3 = 5

pdd1 = 1
pdd2 = 2
pdd3 = 5

pWin = 15

pBlockWin = 10

opv1 = 1
opv2 = 2
opv3 = 6

oph1 = 1
oph2 = 3
oph3 = 7

opdu1 = 1
opdu2 = 2
opdu3 = 6

opdd1 = 1
opdd2 = 2
opdd3 = 6

opWin = 30

opBlockWin = 20

replay = True

while replay == True:
    start() 
    game(p1,p2, trainerSet4)
    hold = True
    while hold:
        ans = input("Play Again Y/n: ")
        if ans == "Y" or ans == 'y':
            replay = True
            hold = False
        elif ans == "N" or ans == 'n':
            replay = False
            hold = False

        





#---------------------------------------------------- training data ------------------

'''function_inputs = copy.deepcopy(trainerSet4)
desired_output = 40

def fitness_func(solution, solution_idx):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    #prep_game(solution)
    output = game(1,1,solution )
    hold = output[0]*output[1]
    if output[0] == 2:
        hold = 1000000000
    fitness = 1.0 / numpy.abs(hold - desired_output)
    return fitness

fitness_function = fitness_func

num_generations = 40 # Number of generations.
num_parents_mating = 7 # Number of solutions to be selected as parents in the mating pool.

# To prepare the initial population, there are 2 ways:
# 1) Prepare it yourself and pass it to the initial_population parameter. This way is useful when the user wants to start the genetic algorithm with a custom initial population.
# 2) Assign valid integer values to the sol_per_pop and num_genes parameters. If the initial_population parameter exists, then the sol_per_pop and num_genes parameters are useless.
sol_per_pop = 50 # Number of solutions in the population.
num_genes = len(function_inputs)

last_fitness = 0
def callback_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution()[1] - last_fitness))
    last_fitness = ga_instance.best_solution()[1]

# Creating an instance of the GA class inside the ga module. Some parameters are initialized within the constructor.
ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating, 
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop, 
                       num_genes=num_genes,
                       on_generation=callback_generation)

# Running the GA to optimize the parameters of the function.
ga_instance.run()

# After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
ga_instance.plot_fitness()

# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))'''