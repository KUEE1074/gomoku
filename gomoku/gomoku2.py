import pygame
from sys import exit
from copy import deepcopy  
from time import time

INF = 10000000
BACKGROUND = 'goban.png'
BOARD_SIZE = (820, 820)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
time_limit = 9.5
invalid_value = -100
start_time = None
number = 0

function_count = 0
class Stone(object):
    def __init__(self, board, point, color):
        self.board = board
        self.point = point
        self.color = color    
        self.coords = (5 + self.point[0] * 40, 5 + self.point[1] * 40)
        self.draw()

    def draw(self):
        print(self.point)
        pygame.draw.circle(screen, self.color, self.coords, 20, 0)
        board.update(self.point, self.color)
        pygame.display.update()

    
class Board(object):
    def __init__(self):
        self.goban = [[0]*19 for _ in range(19)]  
        self.heuristic = [[[0 for k in range(2)] for j in range(19)] for i in range(19)]
        self.adjacecy = set()
        self.next = BLACK
        self.outline = pygame.Rect(45, 45, 720, 720)
        self.draw()

    def draw(self):
        pygame.draw.rect(background, BLACK, self.outline, 3)
        self.outline.inflate_ip(20, 20)
        for i in range(18):
            for j in range(18):
                rect = pygame.Rect(45 + (40 * i), 45 + (40 * j), 40, 40)
                pygame.draw.rect(background, BLACK, rect, 1)
        for i in range(3):
            for j in range(3):
                coords = (165 + (240 * i), 165 + (240 * j))
                pygame.draw.circle(background, BLACK, coords, 5, 0)
        screen.blit(background, (0, 0))
        pygame.display.update()

    def update(self, point, color):
        if color == WHITE:
            self.goban[point[1]-1][point[0]-1] = 'X' 
        else:
            self.goban[point[1]-1][point[0]-1] = 'O'

                       
def heuristic(x, y, goban, heuristic):
    heuristic[y-1][x-1] = [0, 0] ##놓은곳 초기화
    ## 가로
    hori_count = [0, 0]
    left = 0
    for i in range(19):
        if goban[y-1][i] != 0 and hori_count[0] + hori_count[1] == 0:
            left = i
            if goban[y-1][i] == 'O':
                hori_count[0] += 1
            elif goban[y-1][i] == 'X':
                hori_count[1] += 1
            continue
        if goban[y-1][left] == goban[y-1][i]:
            if goban[y-1][i] == 'O':
                hori_count[0] += 1
                if i == 18:
                    heuristic[y-1][left-1][0] = 10**hori_count[0] / 2           
            if goban[y-1][i] == 'X':
                hori_count[1] += 1
                if i == 18:
                    heuristic[y-1][left-1][1] = 10**hori_count[1] / 2
        else:
            if left > 0:
                if goban[y-1][left-1] == 0:       
                    if goban[y-1][left] =='O' and hori_count[0] < 5:
                        if goban[y-1][i] == 0:
                            heuristic[y-1][left-1][0] = 10**hori_count[0]
                        elif goban[y-1][i] == 'X':
                            heuristic[y-1][left-1][0] = 10**hori_count[0] / 2 
                    elif goban[y-1][left]=='X' and hori_count[1] < 5:
                        if goban[y-1][i] == 0:
                            heuristic[y-1][left-1][1] = 10**hori_count[1]
                        elif goban[y-1][i] == 'O':
                            heuristic[y-1][left-1][1] = 10**hori_count[1] / 2
                        
            if goban[y-1][i] == 0:
                if goban[y-1][left] == 'O' and hori_count[0] < 5:
                    if left == 0:
                        heuristic[y-1][i][0] = 10**hori_count[0] / 2
                        left = i
                        hori_count = [0, 0]
                        continue
                    if goban[y-1][left-1] == 0:
                        heuristic[y-1][i][0] = 10**hori_count[0]
                    elif goban[y-1][left-1] == 'X':
                        heuristic[y-1][i][0] = 10**hori_count[0] / 2
                elif goban[y-1][left] == 'X'and hori_count[1] < 5:
                    if left == 0:
                        heuristic[y-1][i][1] = 10**hori_count[1] / 2
                        left = i
                        hori_count = [0, 0]
                        continue
                    if goban[y-1][left-1] == 0:
                        heuristic[y-1][i][1] = 10**hori_count[1]
                    elif goban[y-1][left-1] == 'O':
                        heuristic[y-1][i][1] = 10**hori_count[1] / 2
                left = i
                hori_count = [0, 0]
            else:
                left = i
                if goban[y-1][i] == 'O':
                    hori_count = [1, 0]
                else:
                    hori_count = [0, 1]
    
    ## 세로 
    verti_count = [0, 0]
    top = 0
    for i in range(19):
        if goban[i][x-1] != 0 and verti_count[0] + verti_count[1] == 0:
            top = i
            if goban[i][x-1] == 'O':
                verti_count[0] += 1
            elif goban[i][x-1] == 'X':
                verti_count[1] += 1
            continue
        if goban[top][x-1] == goban[i][x-1]:
            if goban[i][x-1] == 'O':
                verti_count[0] += 1
                if i == 18:
                    heuristic[top-1][x-1][0] = 10**verti_count[0] / 2        
            if goban[i][x-1] == 'X':
                verti_count[1] += 1
                if i == 18:
                    heuristic[top-1][x-1][1] = 10**verti_count[1] / 2
        else:
            if top > 0:
                if goban[top-1][x-1] == 0:      
                    if goban[top][x-1] == 'O' and verti_count[0] < 5:
                        if goban[i][x-1] == 0 : 
                            heuristic[top-1][x-1][0] = 10**verti_count[0]
                        elif goban[i][x-1] == 'X':
                            heuristic[top-1][x-1][0] = 10**verti_count[0] / 2
                    elif goban[top][x-1] == 'X' and verti_count[1] < 5:
                        if goban[i][x-1] == 0 : 
                            heuristic[top-1][x-1][1] = 10**verti_count[1]
                        elif goban[i][x-1] == 'O':
                            heuristic[top-1][x-1][1] = 10**verti_count[1] / 2
            if goban[i][x-1] == 0:
                if goban[top][x-1] == 'O' and verti_count[0] < 5:
                    if top == 0:
                        heuristic[i][x-1][0] = 10**verti_count[0] / 2
                        verti_count = [0, 0]
                        top = i
                        continue
                    if goban[top-1][x-1] == 0:
                        heuristic[i][x-1][0] = 10**verti_count[0]
                    elif goban[top-1][x-1] == 'X':
                        heuristic[i][x-1][0] = 10**verti_count[0] / 2    
                elif goban[top][x-1] == 'X' and verti_count[1] < 5:
                    if top == 0:
                        heuristic[i][x-1][1] = 10**verti_count[1] / 2
                        verti_count = [0, 0]
                        top = i
                        continue
                    if goban[top-1][x-1] == 0:
                        heuristic[i][x-1][1] = 10**verti_count[1]
                    elif goban[top-1][x-1] == 'O':
                        heuristic[i][x-1][1] = 10**verti_count[1] / 2
                verti_count = [0, 0]
                top = i
            else:
                top = i
                if goban[i][x-1] == 'O':
                    verti_count = [1, 0]
                elif goban[i][x-1] == 'X':
                    verti_count = [0, 1]    
    
    ## /
    diag1_count = [0, 0]
    if x+y <= 20:
        diag1_x = i = 0
        diag1_y = j = x+y-2
    else:
        diag1_x = i = x + y -20
        diag1_y = j = 18 
    while True:
        if i > 18 or j < 0:
            break
        if goban[j][i] != 0 and diag1_count[0] + diag1_count[1] == 0:
            diag1_x = i
            diag1_y = j
            if goban[j][i] == 'O':
                diag1_count[0] += 1
            elif goban[j][i] == 'X':
                diag1_count[1] += 1
            i += 1
            j -= 1
            continue
        if goban[diag1_y][diag1_x] == goban[j][i]:
            if goban[j][i] == 'O':
                diag1_count[0] += 1
                if i == 18 or j == 0:
                    heuristic[diag1_y+1][diag1_x-1][0] = 10**diag1_count[0] / 2
            if goban[j][i] == 'X':
                diag1_count[1] += 1
                if i == 18 or j == 0:
                    heuristic[diag1_y+1][diag1_x-1][1] = 10**diag1_count[1] / 2
        else:
            if diag1_x > 0 and diag1_y < 18:
                if goban[diag1_y+1][diag1_x-1] == 0:      
                    if goban[diag1_y][diag1_x] == 'O' and diag1_count[0] < 5:
                        if goban[j][i] == 0 : 
                            heuristic[diag1_y+1][diag1_x-1][0] = 10**diag1_count[0]
                        elif goban[j][i] == 'X':
                            heuristic[diag1_y+1][diag1_x-1][0] = 10**diag1_count[0] / 2
                    elif goban[diag1_y][diag1_x] == 'X' and diag1_count[1] < 5:
                        if goban[j][i] == 0 : 
                            heuristic[diag1_y+1][diag1_x-1][1] = 10**diag1_count[1]
                        elif goban[j][i] == 'O':
                            heuristic[diag1_y+1][diag1_x-1][1] = 10**diag1_count[1] / 2
            if goban[j][i] == 0:
                if goban[diag1_y][diag1_x] == 'O' and diag1_count[0] < 5:
                    if diag1_y == 18 or diag1_x == 0:
                        heuristic[j][i][0] = 10**diag1_count[0] / 2
                        diag1_count = [0, 0]
                        diag1_x = i
                        diag1_y = j
                        continue
                    if goban[diag1_y+1][diag1_x-1] == 0:
                        heuristic[j][i][0] = 10**diag1_count[0]
                    elif goban[diag1_y+1][diag1_x-1] == 'X':
                        heuristic[j][i][0] = 10**diag1_count[0] / 2    
                elif goban[diag1_y][diag1_x] == 'X' and diag1_count[1] < 5:
                    if diag1_y == 18 or diag1_x == 0:
                        heuristic[j][i][1] = 10**diag1_count[1] / 2
                        diag1_count = [0, 0]
                        diag1_x = i
                        diag1_y = j
                        continue
                    if goban[diag1_y+1][diag1_x-1] == 0:
                        heuristic[j][i][1] = 10**diag1_count[1]
                    elif goban[diag1_y+1][diag1_x-1] == 'O':
                        heuristic[j][i][1] = 10**diag1_count[1] / 2
                diag1_count = [0, 0]
                diag1_x = i
                diag1_y = j
            else:
                diag1_x = i
                diag1_y = j
                if goban[j][i] == 'O':
                    diag1_count = [1, 0]
                elif goban[j][i] == 'X':
                    diag1_count = [0, 1]   
        i += 1
        j -= 1

    ## \  
    diag2_count = [0, 0]
    if x > y:
        diag2_x = i = x-y
        diag2_y = j = 0
    else:
        diag2_x = i = 0
        diag2_y = j = y-x 
    while True:
        if i > 18 or j > 18:
            break
        if goban[j][i] != 0 and diag2_count[0] + diag2_count[1] == 0:
            diag2_x = i
            diag2_y = j
            if goban[j][i] == 'O':
                diag2_count[0] += 1
            elif goban[j][i] == 'X':
                diag2_count[1] += 1
            i += 1
            j += 1
            continue
        if goban[diag2_y][diag2_x] == goban[j][i]:
            if goban[j][i] == 'O' :
                diag2_count[0] += 1
                if i == 18 or j == 18:
                    heuristic[diag2_y-1][diag2_x-1][0] = 10**diag2_count[0] / 2
            if goban[j][i] == 'X':
                diag2_count[1] += 1
                if i == 18 or j == 18:
                    heuristic[diag2_y-1][diag2_x-1][1] = 10**diag2_count[0] / 2
        else:
            if diag2_x > 0:
                if goban[diag2_y-1][diag2_x-1] == 0:      
                    if goban[diag2_y][diag2_x] == 'O' and diag2_count[0] < 5:
                        if goban[j][i] == 0: 
                            heuristic[diag2_y-1][diag2_x-1][0] = 10**diag2_count[0]
                        elif goban[j][i] == 'X':
                            heuristic[diag2_y-1][diag2_x-1][0] = 10**diag2_count[0] / 2
                    elif goban[diag2_y][diag2_x] == 'X' and diag2_count[1] < 5:
                        if goban[j][i] == 0: 
                            heuristic[diag2_y-1][diag2_x-1][1] = 10**diag2_count[1]
                        elif goban[j][i] == 'O':
                            heuristic[diag2_y-1][diag2_x-1][1] = 10**diag2_count[1] / 2
            if goban[j][i] == 0:
                if goban[diag2_y][diag2_x] == 'O' and diag2_count[0] < 5:
                    if diag2_x == 0 or diag2_y == 0:
                        heuristic[j][i][0] = 10**diag2_count[0] / 2
                        diag2_count = [0, 0]
                        diag2_x = i
                        diag2_y = j
                        continue
                    if goban[diag2_y-1][diag2_x-1] == 0:
                        heuristic[j][i][0] = 10**diag2_count[0]
                    elif goban[diag2_y-1][diag1_x-1] == 'X':
                        heuristic[j][i][0] = 10**diag2_count[0] / 2    
                elif goban[diag2_y][diag2_x] == 'X' and diag2_count[1] < 5:
                    if diag2_x == 0 or diag2_y == 0:
                        heuristic[j][i][1] = 10**diag2_count[1] / 2
                        diag2_count = [0, 0]
                        diag2_x = i
                        diag2_y = j
                        continue
                    if goban[diag2_y-1][diag2_x-1] == 0:
                        heuristic[j][i][1] = 10**diag2_count[1]
                    elif goban[diag2_y-1][diag2_x-1] == 'O':
                        heuristic[j][i][1] = 10**diag2_count[1] / 2
                diag2_count = [0, 0]
                diag2_x = i
                diag2_y = j
            else:
                diag2_x = i
                diag2_y = j
                if goban[j][i] == 'O':
                    diag2_count = [1, 0]
                elif goban[j][i] == 'X':
                    diag2_count = [0, 1]   
        i += 1
        j += 1


def set_append(my_set, x, y, graph):
    for i in range(x-2, x+1):
        if i < 0 or i > 18:
            continue
        for j in range(y-2, y+1):
            if j < 0 or j > 18:
                continue
            if graph[j][i] == 0:
                my_set.add((i,j))
    if (x-1, y-1) in my_set:
        my_set.remove((x-1,y-1))


def Ai_turn(goban, heuristic, sett): ##alpha_beta_pruning: return이 좌표여야함
    global start_time, invalid_value
    global number
    start_time = time()
    depth = 0
    depth_limit = 121
    
    for limit in range(1, depth_limit, 2):
        number = 0
        temp = black_value(goban, heuristic, sett, [0,0] ,-INF, INF, depth, limit)
        if temp[2] == invalid_value:
            break
        result = temp
        print(limit, "일 때 선택좌표+heuristic값:", result[0]+1, result[1]+1, result[2])
    print("코드 시간", time() - start_time)    
    return result
    

def black_value(goban, m_heuristic, sett, state, alpha, beta, depth, limit):
   
    global invalid_value, start_time, time_limit
    depth += 1
    my_goban = deepcopy(goban)
    my_heuristic = deepcopy(m_heuristic)
    my_set = deepcopy(sett)
    if depth != 1:
        my_goban[state[1]][state[0]] = 'X'
        heuristic(state[0]+1, state[1]+1, my_goban, my_heuristic)
        set_append(my_set, state[0]+1, state[1]+1, my_goban)
    if win_check(my_goban, state[0]+1, state[1]+1): ##white의 수가 승리 인경우
        return [0,0,-INF+100] 
    if three_three_check(my_goban, state[0]+1, state[1]+1): ##white의 수가 3-3인경우
        return [0,0, INF-100]
    if depth == limit:

        if time()-start_time > time_limit:
            return [0, 0, invalid_value]
        max_value = -INF
        max_move = [0, 0]
        for (i, j) in my_set:
            if my_heuristic[j][i][0] + my_heuristic[j][i][1] > max_value:
                max_value = my_heuristic[j][i][0]+ my_heuristic[j][i][1]
                max_move = [i, j]
        max_move.append(max_value)
        return max_move
        
    lst = []
    result = [0, 0, -INF]
    for k in range(int(len(my_set)/4)):
        max_value = -INF
        max_move = [0, 0]
        for (i, j) in my_set:
            if [i, j] in lst:
                continue
            if my_heuristic[j][i][0] + my_heuristic[j][i][1] > max_value:
                max_value = my_heuristic[j][i][0] + my_heuristic[j][i][1]
                max_move = [i, j]    
        lst.append([max_move[0],max_move[1]])
        temp = white_value(my_goban, my_heuristic, my_set, max_move, alpha, beta, depth, limit)
        if temp[2] == invalid_value:
            return [0, 0, invalid_value]
        max_move.append(temp[2])
        if result[2] < max_move[2]:
            result = max_move
        if result[2] >= beta:
            return result
        alpha = max(alpha, result[2])
    return result

    
def white_value(goban, m_heuristic, sett, state, alpha, beta, depth, limit):
    global invalid_value
    depth += 1
    my_goban = deepcopy(goban)
    my_heuristic = deepcopy(m_heuristic)
    my_set = deepcopy(sett)
    my_goban[state[1]][state[0]] = 'O'
    heuristic(state[0]+1, state[1]+1, my_goban, my_heuristic)
    set_append(my_set, state[0]+1, state[1]+1, my_goban)    

    if win_check(my_goban, state[0]+1, state[1]+1):
        return [0,0,INF-100]
    if three_three_check(my_goban, state[0]+1, state[1]+1):
        return [0,0, -INF+100]    
    
    lst = []
    result = [0, 0, INF]
    for k in range(int(len(my_set)/4)):
        max_value = -INF
        max_move = [0, 0]
        for (i, j) in my_set:
            if [i, j] in lst:
                continue
            if my_heuristic[j][i][0] + my_heuristic[j][i][1] > max_value:
                max_value = my_heuristic[j][i][0] + my_heuristic[j][i][1]
                max_move = [i, j]    

        lst.append([max_move[0],max_move[1]])
        temp = black_value(my_goban, my_heuristic, my_set, max_move, alpha, beta, depth, limit)
        if temp[2] == invalid_value:
            return [0, 0, invalid_value]
        max_move.append(temp[2])
        if result[2] > max_move[2]:
            result = max_move
        if result[2] <= alpha:
            return result
        beta = min(beta, result[2])
    return result


def three_three_check(goban, x, y):
    three_count = 0
    ##가로
    i = x
    count = 1
    right = left = True
    while right or left:
        if i > 18 or i < 0:
            count = 0 
            break
        if right:
            if i-x>2:
                i = x-2
                right = False
                continue
            if goban[y-1][i] == goban[y-1][x-1]:
                if count > 3:
                    return
                count += 1 
                i += 1
            else:
                if goban[y-1][i] == 0:
                    right = False
                    i = x-2
                else:
                    count = 0
                    break
        else:
            if x-i > 4:
                left = False
                continue
            if goban[y-1][i] == goban[y-1][x-1]:
                if count > 3: 
                    return
                count += 1 
                i -= 1
            else:
                if goban[y-1][i] != 0:
                    count = 0    
                break
    if count == 3:
        three_count += 1
    ##세로
    i = y
    count = 1
    top = bottom = True
    while bottom or top:
        if i > 18 or i < 0:
            count = 0
            break
        if bottom:
            if i-y>2:
                i = y-2
                bottom = False
                continue
            if goban[i][x-1] == goban[y-1][x-1]:
                if count > 3:
                    return
                count += 1 
                i += 1
            else:
                if goban[i][x-1] == 0:
                    bottom = False
                    i = y-2
                else:
                    count = 0
                    break
        else:
            if y-i > 4:
                top = False
                continue
            if goban[i][x-1] == goban[y-1][x-1]:
                if count >= 3: 
                    return
                count += 1 
                i -= 1
            else:
                if goban[i][x-1] != 0:
                    count = 0
                break
    if count == 3:
        three_count += 1
    
    # 대각선 /
    count = 1
    i = x
    j = y-2
    diag1_top = diag1_bot = True
    while diag1_top or diag1_bot:
        if i < 0 or i > 18 or j < 0 or j > 18:
            count = 0
            break
        if diag1_top:
            if i-x>2:
                i = x-2
                j = y
                diag1_top = False
                continue
            if goban[j][i] == goban[y-1][x-1]:
                if count >= 3:
                    return
                count += 1 
                i += 1
                j -= 1
            else:
                if goban[j][i] == 0:
                    diag1_top = False
                    i = x-2
                    j = y 
                else:
                    count = 0
                    break
        else:
            if i - x > 4:
                diag1_bot = False
                continue
            if goban[j][i] == goban[y-1][x-1]:
                if count >= 3: 
                    return
                count += 1 
                i -= 1
                j += 1
            else:
                if goban[j][i] != 0:
                    count = 0
                break
    if count == 3:
        three_count += 1
    
    # 대각선 \
    count = 1
    i = x
    j = y
    diag2_top = diag2_bot = True
    while diag2_top or diag2_bot:
        if i < 0 or i > 18 or j < 0 or j > 18:
            count = 0
            break
        if diag2_bot:
            if i-x>2:
                i = x-2
                j = y-2
                diag2_bot = False
                continue
            if goban[j][i] == goban[y-1][x-1]:
                if count >= 3:
                    return
                count += 1 
                i += 1
                j += 1
            else:
                if goban[j][i] == 0:
                    diag2_bot = False
                    i = x-2
                    j = y-2 
                else:
                    count = 0
                    break
        else:
            if i - x > 4:
                diag2_top = False
                continue
            if goban[j][i] == goban[y-1][x-1]:
                if count >= 3: 
                    return
                count += 1 
                i -= 1
                j -= 1
            else:
                if goban[j][i] != 0:
                    count = 0
                break
    if count == 3:
        three_count += 1

    if three_count >=2:
        return True
         

def win_check(goban, x, y):
    horizon = 1
    vertical = 1
    diagonal1 = 1  ## / 모양
    diagonal2 = 1  ## \ 모양
    for i in range(x, 19):
        if goban[y-1][i] == goban[y-1][x-1]:
            horizon += 1
        else:
            break
    for i in reversed(range(x-1)):
        if goban[y-1][i] == goban[y-1][x-1]:
            horizon += 1
        else:
            break
    if horizon == 5:
        return True

    for i in range(y, 19):
        if goban[i][x-1] == goban[y-1][x-1]:
            vertical += 1
        else:
            break
    for i in reversed(range(y-1)):
        if goban[i][x-1] == goban[y-1][x-1]:
            vertical += 1
        else:
            break
    if vertical == 5:
        return True
    
    i = x-1
    j = y-1
    while i<18 and j >0:
        i += 1
        j -= 1
        if goban[j][i] == goban[y-1][x-1]:
            diagonal1 += 1
        else:
            break
    i = x-1
    j = y-1
    while i>0 and j<19:
        i -= 1
        j += 1
        if goban[j][i] == goban[y-1][x-1]:
            diagonal1 += 1
        else:
            break
    if diagonal1 == 5:
        return True
    
    i = x-1
    j = y-1
    while i<18 and j<18:
        i += 1
        j += 1
        if goban[j][i] == goban[y-1][x-1]:
            diagonal2 += 1
        else:
            break
    i = x-1
    j = y-1
    while i>0 and j>0:
        i -= 1
        j -= 1
        if goban[j][i] == goban[y-1][x-1]:
            diagonal2 += 1      
        else:
            break
    if diagonal2 == 5:
        return True
    return False         


def main():
    order = BLACK
    count = 0
    while True:
        pygame.time.wait(500)
        if order == BLACK: ## Ai Turn
            if count == 0:
                Stone(board, (10, 10), order)
                heuristic(10, 10, board.goban, board.heuristic)
                set_append(board.adjacecy, 10, 10, board.goban)
                order = WHITE
                count += 1
            else:
                move = Ai_turn(board.goban, board.heuristic, board.adjacecy)
                Stone(board, (move[0]+1, move[1]+1), order)
                heuristic(move[0]+1, move[1]+1 , board.goban, board.heuristic)
                set_append(board.adjacecy, move[0]+1, move[1]+1, board.goban)
                if win_check(board.goban, move[0]+1, move[1]+1):
                    print('AI 승리')
                    exit()
                order = WHITE
           
        else: ## Player Turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and board.outline.collidepoint(event.pos):
                        x = int(round(((event.pos[0] - 5) / 40.0), 0))
                        y = int(round(((event.pos[1] - 5) / 40.0), 0))
                        board.goban[y-1][x-1] = 'X'
                        if three_three_check(board.goban,x, y):
                            print("여기는 삼-삼입니다!")
                            board.goban[y-1][x-1] = 0
                        else:
                            
                            Stone(board, (x, y), order)
                            heuristic(x, y, board.goban, board.heuristic)
                            set_append(board.adjacecy, x, y, board.goban)
                            if win_check(board.goban, x, y):
                                print('PLAYER 승리')
                                exit()
                            order = BLACK
                    
                    
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('오목')
    screen = pygame.display.set_mode(BOARD_SIZE, 0, 32)
    background = pygame.image.load(BACKGROUND).convert()
    board = Board()
    main()

