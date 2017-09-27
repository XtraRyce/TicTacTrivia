import pygame
import csv
import random
import fileinput
from itertools import chain

anime = csv.DictReader(open('50animequestions.csv', encoding="utf8"))
vg = csv.DictReader(open('50videogamequestions.csv', encoding="utf8"))
myDict = []
for row in anime:
    myDict.append(row)
for row in vg:
    myDict.append(row)

for row in myDict:
    print(row)

dupecheck = []

with open('dupecheck.txt') as file:
    for line in file:
        line = line.split()
        if line:
            line = [int(i) for i in line]
            dupecheck.extend(line)



print(dupecheck)


pygame.init()

# go_back = False

ongoing = False

FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)
red = (155, 0, 0)
green = (0, 155 ,0)
bright_green = (0, 255, 0)
bright_red = (255,0, 0)
team_o = (39, 167, 216)
team_x = (255, 154, 0)

display_width = 1280
display_height = 720
cell_width = round(display_width/3)
cell_height = round(display_height/3)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('TicTacTrivia')

clock = pygame.time.Clock()
# smallfont = pygame.font.SysFont(None, 25)
smallerfont = pygame.font.SysFont("tahoma", 18)
smallfont = pygame.font.SysFont("tahoma", 25)
medfont = pygame.font.SysFont("tahoma", 50)
largefont = pygame.font.SysFont("tahoma", 80)

def quitgame():
    pygame.quit()
    quit()

def initvalues():
    global board_state, o_state, x_state, win_conditions, isShuffled, order
    board_state = {1: [-1, False],
                   2: [-1, False],
                   3: [-1, False],
                   4: [-1, False],
                   5: [-1, False],
                   6: [-1, False],
                   7: [-1, False],
                   8: [-1, False],
                   9: [-1, False]}
    o_state = [False,
               False,
               False,
               False,
               False,
               False,
               False,
               False,
               False]
    x_state = [False,
               False,
               False,
               False,
               False,
               False,
               False,
               False,
               False]
    win_conditions = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [1, 5, 9],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
        [3, 5, 7]]
    isShuffled = [False,
                  False,
                  False,
                  False,
                  False,
                  False,
                  False,
                  False,
                  False]
    order = {1: [],
             2: [],
             3: [],
             4: [],
             5: [],
             6: [],
             7: [],
             8: [],
             9: []
             }

def truncline(text, font, maxwidth):
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    old = None
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


def wrapline(text, font, maxwidth):
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)

def cell_pos(x,y):
    for i in range(1,10):
        temp = get_cell(i)
        if temp[1] >= x >= temp[0] and temp[3] >= y >= temp[2]:
            z = i
    return z

def text_objects(text, color, size):
    if size == "smaller":
        textSurface = smallerfont.render(text, True, color)
    elif size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, cell, size = "small", y_align = "center"):
    textSurf, textRect = text_objects(msg, color, size)
    if cell is 0:
        if y_align == "center":
            textRect.center = (display_width // 2), (display_height // 2)
        elif y_align == "top":
            textRect.center = (display_width // 2), (display_height // 3)
        elif y_align == "bottom":
            textRect.center = (display_width // 2), ((display_height // 3) * 2)
    elif cell <= 3 and cell >= 1:
        if y_align == "center":
            textRect.center = ((cell_width * ((cell - 1) % 3)) + (cell_width // 2)), (cell_height // 2)
        elif y_align == "top":
            textRect.center = ((cell_width * ((cell - 1) % 3)) + (cell_width // 2)), (cell_height // 3)
        elif y_align == "bottom":
            textRect.center = ((cell_width * ((cell - 1) % 3)) + (cell_width // 2)), ((cell_height // 3) * 2)
    elif cell <= 6 and cell >= 4:
        if y_align == "center":
            textRect.center = ((cell_width * ((cell - 1) % 3)) + (cell_width // 2)), (cell_height + (cell_height // 2))
        elif y_align == "top":
            textRect.center = ((cell_width * ((cell - 1) % 3)) + (cell_width // 2)), (cell_height + (cell_height // 3))
        elif y_align == "bottom":
            textRect.center = ((cell_width * ((cell - 1) % 3)) + (cell_width // 2)), (cell_height + ((cell_height // 3) * 2))
    elif cell <= 9 and cell >= 7:
        if y_align == "center":
            textRect.center = ((cell_width * ((cell - 1) % 3)) + (cell_width // 2)), (cell_height + cell_height + (cell_height // 2))
        elif y_align == "top":
            textRect.center = ((cell_width * ((cell - 1) % 3)) + (cell_width // 2)), (cell_height + cell_height + (cell_height // 3))
        elif y_align == "bottom":
            textRect.center = ((cell_width * ((cell - 1) % 3)) + (cell_width // 2)), (cell_height + cell_height + ((cell_height // 3) * 2))
    screen.blit(textSurf, textRect)

def get_cell(cell):
    minX = ((cell_width * ((cell - 1) % 3)))
    maxX = minX + cell_width
    if cell <= 3 and cell >= 1:
        minY = 0
        maxY = cell_height
    elif cell <= 6 and cell >= 4:
        minY = cell_height
        maxY = cell_height * 2
    elif cell <= 9 and cell >= 7:
        minY = cell_height * 2
        maxY = cell_height * 3
    return (minX, maxX, minY, maxY)

def cell_button(text, cell, fc, fs, ac, ic, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    bounds = get_cell(cell)
    if bounds[1] >= mouse[0] >= bounds[0] and bounds[3] >= mouse[1] >= bounds[2]:
        screen.fill(ac, rect=[bounds[0], bounds[2], cell_width, cell_height])
        if click[0] == 1 and action != None:
            action()
    else:
        screen.fill(ic, rect=[bounds[0], bounds[2], cell_width, cell_height])
    message_to_screen(text, fc, cell, fs)

def print_question(text, color, font, size):
    qwrap = wrapline(text, font, display_width)
    height = 0
    for x in qwrap:
        textSurf, textRect = text_objects(x, color, size)
        textRect.center = (display_width // 2), ((display_height // 8) + height)
        height += (textRect.bottom - textRect.top)
        screen.blit(textSurf, textRect)

def print_answer(index, cell, color, font, size):
    choices = []
    if myDict[index]['type'] == 'multiple':
        if isShuffled[cell-1] == False:
            order[cell] = [1, 2, 3, 4]
            random.shuffle(order[cell])
            isShuffled[cell-1] = True
        choices.append([myDict[index]['correct_answer'], True])
        choices.append([myDict[index]['incorrect_answers/0'], False])
        choices.append([myDict[index]['incorrect_answers/1'], False])
        choices.append([myDict[index]['incorrect_answers/2'], False])
    if myDict[index]['type'] == 'boolean':
        if isShuffled[cell-1] == False:
            order[cell] = [1, 2]
            isShuffled[cell-1] = True
        choices.append([myDict[index]['correct_answer'], True])
        choices.append([myDict[index]['incorrect_answers/0'], False])
    answer_bound = []

    for x,i in enumerate(order[cell]):
        textSurf, textRect = text_objects(choices[i-1][0], color, size)
        textRect.center = (((display_width // 2) * (x % 2)) + (display_width // 4)), ((display_height // 2) + ((display_height // 4) * (x // 2)))
        if choices[i-1][1] == True:
            correct = x + 1
        answer_bound.append(textSurf.get_rect())
        screen.blit(textSurf, textRect)
    # print(choices)
    # print(isShuffled)
    # print(order)
    return correct, answer_bound




def MainMenu():
    # gameOver = False
    gameExit = True


    while gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        screen.fill(white)
        message_to_screen("TIC", black, 1, size="large")
        message_to_screen("TAC", black, 2, size="large")
        message_to_screen("TRIVIA", black, 3, size="large")

        if ongoing == False:
            cell_button("New Game", 4, white, "medium", bright_red, red, gamescreen)
        else:
            cell_button("Resume Game", 4, white, "medium", bright_red, red, gamescreen)
        cell_button("Demo", 5, white, "medium", bright_red, red)
        cell_button("Options", 6, white, "medium", bright_red, red)
        cell_button("Quit", 8, white, "medium", bright_red, red, quitgame)

        # print(event)



        # screen.fill(red, rect=[0, 0, cell_width, cell_height])
        # screen.fill(black, rect=[cell_width, 0, cell_width, cell_height])
        # screen.fill(red, rect=[cell_width*2, 0, cell_width, cell_height])
        #
        # screen.fill(black, rect=[0, cell_height, cell_width, cell_height])
        # screen.fill(red, rect=[cell_width, cell_height, cell_width, cell_height])
        # screen.fill(black, rect=[cell_width*2, cell_height, cell_width, cell_height])
        #
        # screen.fill(red, rect=[0, cell_height*2, cell_width, cell_height])
        # screen.fill(black, rect=[cell_width, cell_height*2, cell_width, cell_height])
        # screen.fill(red, rect=[cell_width*2, cell_height*2, cell_width, cell_height])
        #
        # message_to_screen("T", white, 1)
        # message_to_screen("I", white, 2)
        # message_to_screen("C", white, 3)
        # message_to_screen("T", white, 4)
        # message_to_screen("A", white, 5)
        # message_to_screen("C", white, 6)
        # message_to_screen("T", white, 7)
        # message_to_screen("O", white, 8)
        # message_to_screen("E", white, 9)

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()

qindex = random.sample(range(0,99), 9)


def gamescreen():
    gameOver = False
    global ongoing, qindex, board_state, turn
    if ongoing == False:
        initvalues()
        print(qindex)
        for i,q in enumerate(qindex):
            print(i,q)
            print(dupecheck[q])
            if dupecheck[q] == 0:
                dupecheck[q] = 1
            else:
                while dupecheck[q] != 1:
                    qindex[i] = random.randint(1, 100)
                    if dupecheck[q] == 0:
                        dupecheck[q] = 1
        # with fileinput.FileInput('dupecheck.txt', inplace=True, backup='.bak') as file:
        #     for i, line in enumerate(file):
        #         if dupecheck[i] == 1:
        #             print(line.replace('0', '1'), end='')
        #         else:
        #             print(line.replace('0', '0'), end='')

        for key, cell in board_state.items():
            cell[0] = qindex[key-1]
        ongoing = True
    else:
        print(qindex)
        print(board_state)
        while not gameOver:
            current_pos = pygame.mouse.get_pos()
            current_cell = cell_pos(current_pos[0], current_pos[1])
            # print(current_cell)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameOver = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    question(qindex[current_cell-1], current_cell)

            for key, cell in board_state.items():
                if cell[1] == False:
                    mouse = pygame.mouse.get_pos()
                    bounds = get_cell(key)
                    if bounds[1] >= mouse[0] >= bounds[0] and bounds[3] >= mouse[1] >= bounds[2]:
                        screen.fill(bright_red, rect=[bounds[0], bounds[2], cell_width, cell_height])
                    else:
                        screen.fill(red, rect=[bounds[0], bounds[2], cell_width, cell_height])
                    message_to_screen(myDict[qindex[key - 1]]['category'].capitalize(), white, key, "smaller", "top")
                    message_to_screen(myDict[qindex[key - 1]]['difficulty'].capitalize(), white, key, "medium", "bottom")

            pygame.display.update()
            clock.tick(FPS)
            # else:

            # for i in range(1,10):

            # for i in board_state:
            #     if board_state[0] == False:
            #         cell_button("?", i, black, "large", white, white, question)
            #     else

            # cell_button("Back to Main Menu", 7, black, "medium", bright_red, red, goback)
            # if go_back == 1:
            #     gameOver = True
            #     go_back = 0
            # pygame.display.update()
            # clock.tick(FPS)

def question(index, cell):
    goBack = False
    global board_state, x_state, o_state
    print(index)
    while not goBack:
        # print('nope')
        current_pos = pygame.mouse.get_pos()
        current_cell = cell_pos(current_pos[0], current_pos[1])
        screen.fill(white)
        print_question(myDict[index]['question'].capitalize(), black, medfont, "medium")
        print_answer(index, cell, black, smallfont, "small")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    goBack = True
                # if event.key == pygame.K_SPACE:
                #     countdown()

            # elif event.type == pygame.MOUSEBUTTONDOWN:

                # question(qindex[current_cell - 1], current_cell)

        pygame.display.update()
        clock.tick(FPS)


    # for i in board_state:
    #     board_state[0] = random.randint(0,99
    # screen.fill(white)
    # cell_button("Yes", 4, black, "medium", white, white, )

MainMenu()