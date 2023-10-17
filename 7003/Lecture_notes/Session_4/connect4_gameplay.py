import pandas as pd
OldTreeData = pd.read_csv('Player2_Tree.csv', header=0, index_col=0, keep_default_na=False)
OldTree = OldTreeData.T.to_dict();print(len(OldTree))
import ast
for i in range(len(OldTree)):
    OldTree[i]['Child']=ast.literal_eval(OldTree[i]['Child'])
    OldTree[i]['State']=ast.literal_eval(OldTree[i]['State'])
    if OldTree[i]['Type']=='D':
        OldTree[i].pop('Decision')
        OldTree[i].pop('UCB')
board_depth=7; board_columns=['A','B','C','D','E','F','G']
import random
import math
import copy
UCB_constant=1
# Generate an empty board
def gen_board():
    B={}
    for col in board_columns:
        B[col]={}
        for i in range(1,board_depth+1):
            B[col][i]=0
    return B
# Function to make a move and check if the player wins
# (board = B; player = 1 or 2; last move = col)
def make_move(B,player,col):
    # place the disc
    row=1;error=0
    while not B[col][row]==0:
        row=row+1
        if row>board_depth:
            row=row-1;error=1;break
    if error==0:
        B[col][row]=player
    # check column
    win_col=0;count=0
    for i in range(row):
        if B[col][row-i]==player:
            count=count+1
        else:
            break
    if count==4:
        win_col=1
    # check row
    win_row=0;count=0
    for i in range(len(board_columns)):
        if B[board_columns[i]][row]==player:
            count=count+1
        else:
            count=0
        if count==4:
            win_row=1;break
    # check diagnal
    win_dia=0;count=0
    col_index=1
    while not board_columns[col_index-1]==col:
        col_index=col_index+1
    step_down=min(col_index,row)
    col_room=len(board_columns)-col_index
    row_room=board_depth-row
    step_up=min(col_room,row_room)
    for i in range(-step_down,step_up):
        if B[board_columns[col_index+i]][row+i+1]==player:
            count=count+1
        else:
            count=0
        if count==4:
            win_dia=1;break
    count=0
    step_down=min(col_index,row_room+1)
    step_up=min(col_room,row-1)
    for i in range(-step_down,step_up):
        if B[board_columns[col_index+i]][row-i-1]==player:
            count=count+1
        else:
            count=0
        if count==4:
            win_dia=1;break
    # determine result
    win=0
    if (win_col+win_row+win_dia)>=1:
        win=1
    return [error,win]
def Expand(tree, nodeX):
    if len(tree[nodeX]['Child'])==0:
        temp_state=copy.deepcopy(tree[nodeX]['State']);temp_state.append('A')
        tree[len(tree)]={'Parent':nodeX,'Child':[],'Decision':'A','Type':'S',
                         'State':temp_state,'n':0,'V':0,'UCB':float('inf')}
        temp_state=copy.deepcopy(tree[nodeX]['State']);temp_state.append('B')
        tree[len(tree)]={'Parent':nodeX,'Child':[],'Decision':'B','Type':'S',
                         'State':temp_state,'n':0,'V':0,'UCB':float('inf')}
        temp_state=copy.deepcopy(tree[nodeX]['State']);temp_state.append('C')
        tree[len(tree)]={'Parent':nodeX,'Child':[],'Decision':'C','Type':'S',
                         'State':temp_state,'n':0,'V':0,'UCB':float('inf')}
        temp_state=copy.deepcopy(tree[nodeX]['State']);temp_state.append('D')
        tree[len(tree)]={'Parent':nodeX,'Child':[],'Decision':'D','Type':'S',
                         'State':temp_state,'n':0,'V':0,'UCB':float('inf')}
        temp_state=copy.deepcopy(tree[nodeX]['State']);temp_state.append('E')
        tree[len(tree)]={'Parent':nodeX,'Child':[],'Decision':'E','Type':'S',
                         'State':temp_state,'n':0,'V':0,'UCB':float('inf')}
        temp_state=copy.deepcopy(tree[nodeX]['State']);temp_state.append('F')
        tree[len(tree)]={'Parent':nodeX,'Child':[],'Decision':'F','Type':'S',
                         'State':temp_state,'n':0,'V':0,'UCB':float('inf')}
        temp_state=copy.deepcopy(tree[nodeX]['State']);temp_state.append('G')
        tree[len(tree)]={'Parent':nodeX,'Child':[],'Decision':'G','Type':'S',
                         'State':temp_state,'n':0,'V':0,'UCB':float('inf')}
        tree[nodeX]['Child']=[len(tree)-1,len(tree)-2,len(tree)-3,len(tree)-4,len(tree)-5,len(tree)-6,len(tree)-7]
def BuildTree(tree, node, k):
    for game in range(k):
        state=copy.deepcopy(tree[node]['State'])
        # Restore the board first
        board=gen_board()
        result=[0,0]
        for m in range(len(state)):
            p=1+m%2
            result=make_move(board,p,state[m])
        if result[1]==1:
            if tree[node]['Type']=='S':
                finish=1;payoff=1
            else:
                finish=1;payoff=0
        else:
            finish=0;payoff=0
        # Start the game
        pointer=node
        while finish==0:
            # If the node is of type 'S', simulate the opponent's move
            if tree[pointer]['Type']=='S':
                # The opponent will make a random move if there is no move to win immediately
                win_now=0
                for col in board_columns:
                    test_board=copy.deepcopy(board)
                    test_result=make_move(test_board,1+len(state)%2,col)
                    if test_result[0]==0 and test_result[1]==1:
                        win_now=1;move=col;result=make_move(board,1+len(state)%2,move);break
                if win_now==0:
                    lose_now=0
                    for col in board_columns:
                        test_board=copy.deepcopy(board)
                        test_result=make_move(test_board,2-len(state)%2,col)
                        if test_result[0]==0 and test_result[1]==1:
                            lose_now=1;move=col;result=make_move(board,1+len(state)%2,move);break
                    if lose_now==0:
                        error_move=1
                        while error_move==1:
                            move=board_columns[int(math.floor(random.random()*7))]
                            result=make_move(board,1+len(state)%2,move)
                            error_move=result[0]
                state.append(move)
                # check if the state has been realized before
                n_child=len(tree[pointer]['Child'])
                while n_child>0:
                    if tree[tree[pointer]['Child'][n_child-1]]['State']==state:
                        pointer=tree[pointer]['Child'][n_child-1]
                        break
                    else:
                        n_child=n_child-1
                # if no, add a new decision node
                if n_child==0:
                    tree[len(tree)]={'Parent':pointer,'Child':[],'Type':'D','State':copy.deepcopy(state),'n':0,'V':0}
                    tree[pointer]['Child'].append(len(tree)-1)
                    pointer=len(tree)-1
                if result[1]==1:
                    finish=1;break
            else:
                # Expansion
                if len(tree[pointer]['Child'])==0:
                    Expand(tree, pointer)
                # Selection
                error_move=1
                while error_move==1:
                    select_child=0
                    for i in range(1,len(tree[pointer]['Child'])):
                        if float(tree[tree[pointer]['Child'][i]]['UCB'])>float(tree[tree[pointer]['Child'][select_child]]['UCB']):
                            select_child=i
                    move=tree[tree[pointer]['Child'][select_child]]['Decision']
                    result=make_move(board,1+len(state)%2,move)
                    error_move=result[0]
                    if error_move==1:
                        tree[pointer]['Child'].pop(select_child)
                state.append(move)
                pointer=tree[pointer]['Child'][select_child]
                if result[1]==1:
                    finish=1;payoff=1;break
            # Check if it is a draw
            count=0
            for row in range(board_depth):
                for col in board_columns:
                    if board[col][board_depth-row]==0:
                        count=count+1
            if count<1:
                finish=1;payoff=0.5
        # Start backpropagation
        while pointer>=node:
            tree[pointer]['V']=(tree[pointer]['V']*tree[pointer]['n']+payoff)/(tree[pointer]['n']+1)
            tree[pointer]['n']=tree[pointer]['n']+1
            if tree[pointer]['Type']=='S' and pointer>0:
                tree[pointer]['UCB']=tree[pointer]['V']+UCB_constant*(
                    math.log(tree[tree[pointer]['Parent']]['n']+1)/tree[pointer]['n'])**0.5
                for i in tree[tree[pointer]['Parent']]['Child']:
                    if tree[i]['n']>0 and not i==pointer:
                        tree[i]['UCB']=tree[i]['V']+UCB_constant*(
                            math.log(tree[tree[i]['Parent']]['n']+1)/tree[i]['n'])**0.5
            pointer=tree[pointer]['Parent']
        
def Optimization(tree, k):
    pointerO=0;total_move=0
    while total_move<49:
        if tree[pointerO]['Type']=='D':
            if tree[pointerO]['n']<in_game_sim:
                BuildTree(tree, pointerO, k)
            if len(tree[pointerO]['Child'])==0:
                print('You lose!');break
            choice=0
            for i in range(1,len(tree[pointerO]['Child'])):
                if tree[tree[pointerO]['Child'][i]]['V']>tree[tree[pointerO]['Child'][choice]]['V']:
                    choice=i
            pointerO=tree[pointerO]['Child'][choice]
            print('Your move:',tree[pointerO]['Decision'])
            BuildTree(tree, pointerO, 1)
            if len(tree[pointerO]['Child'])==0:
                print('You win!');break
        else:
            move=input('Move of the opponent:')
            while not move in board_columns:
                move=input('Invalid entry! Move of the opponent:')
            state=copy.deepcopy(tree[pointerO]['State'])
            state.append(move)
            n_Child=len(tree[pointerO]['Child'])
            while n_Child>0:
                if tree[tree[pointerO]['Child'][n_Child-1]]['State']==state:
                    pointerO=tree[pointerO]['Child'][n_Child-1]
                    break
                else:
                    n_Child=n_Child-1
            if n_Child==0:
                tree[len(tree)]={'Parent':pointerO,'Child':[],'Type':'D','State':copy.deepcopy(state),'n':0,'V':0}
                tree[pointerO]['Child'].append(len(tree)-1)
                pointerO=len(tree)-1
        total_move=total_move+1
    if total_move==49:
        print('It is a draw!')

in_game_sim=2000
play_again='y'
while play_again=='y':
    Optimization(OldTree, in_game_sim)
    play_again=input('Play again?(y/n)')
