import pygame
import csv
import random
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

win_flavor = ("%s won the round!", "%s gets it!", "%s takes the cell!", "%s wins the round!", "Impressive win by %s!")
lose_flavor = ("%s steals it!", "%s grabs this one away!", "Stolen by %s!", "Effortless round for %s!", "%s, now\'s your chance!")

pygame.init()

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

smallerfont = pygame.font.SysFont("tahoma", 18)
smallfont = pygame.font.SysFont("tahoma", 25)
medfont = pygame.font.SysFont("tahoma", 50)
largefont = pygame.font.SysFont("tahoma", 80)

win_conditions = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [1, 5, 9],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
        [3, 5, 7]]

def quitgame():
    pygame.quit()
    quit()

def initvalues():
    global board_state, turn, o_state, x_state, isShuffled, order
    board_state = {1: [-1, False],
                   2: [-1, False],
                   3: [-1, False],
                   4: [-1, False],
                   5: [-1, False],
                   6: [-1, False],
                   7: [-1, False],
                   8: [-1, False],
                   9: [-1, False]}
    turn = 0
    o_state = []
    x_state = []
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

def print_answer(index, cell, color, font, size, turn=False):
    current_pos = pygame.mouse.get_pos()
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
    for x, i in enumerate(order[cell]):
        textSurf, textRect = text_objects(choices[i - 1][0], color, size)
        textRect.center = (((display_width // 2) * (x % 2)) + (display_width // 4)), (
            (display_height // 2) + ((display_height // 4) * (x // 2)))
        if choices[i - 1][1] == True:
            correct = x + 1
        answer_bound.append(textRect)
        if textRect.right >= current_pos[0] >= textRect.left and textRect.bottom >= current_pos[1] >= textRect.top:
            if turn == True:
                screen.fill(team_o, textRect)
            else:
                screen.fill(team_x, textRect)
        screen.blit(textSurf, textRect)
    return correct, answer_bound

def countdown():
    counter = 15
    loop = True
    while loop:
        if counter == 0:
            textSurf, textRect = text_objects("Time's up!", red, "large")
            textRect.center = ((display_width // 2), ((display_height // 8) * 7))
            screen.blit(textSurf, textRect)
        else:
            textSurf, textRect = text_objects(str(counter), black, "large")
            textRect.center = ((display_width // 2), ((display_height // 8) * 7))
            screen.blit(textSurf, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            else:
                print(event)
        pygame.display.flip()
        clock.tick(1)
        screen.fill(white, textRect)
        pygame.display.flip()
        counter -= 1
        if counter < 0:
            loop = False

def result(cell, correct=None):
    global board_state, turn, o_state, x_state, ongoing
    board_state[cell][1] = True
    screen.fill(white)

    if turn % 2 == 0:
        if correct == True:
            team = "O"
            o_state.append(cell)
            message_to_screen((random.choice(win_flavor) % team), team_o, 0, "large")
        else:
            team = "X"
            x_state.append(cell)
            message_to_screen((random.choice(lose_flavor) % team), team_x, 0, "large")
        turn = 1
    elif turn % 2 == 1:
        if correct == True:
            team = "X"
            x_state.append(cell)
            message_to_screen((random.choice(win_flavor) % team), team_x, 0, "large")
        else:
            team = "O"
            o_state.append(cell)
            message_to_screen((random.choice(lose_flavor) % team), team_o, 0, "large")
        turn = 0
    pygame.display.flip()
    clock.tick(1)
    clock.tick(1)

    for cond in win_conditions:
        if set(cond).issubset(o_state):
            for i in range(0,3):
                screen.fill(team_o)
                message_to_screen("O Team wins the game!", black, 0, "large", "top")
                message_to_screen("Congratulations!", black, 0, "large", "bottom")
                pygame.display.flip()
                clock.tick(1)
                screen.fill(team_o)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    else:
                        print(event)
                pygame.display.flip()
                clock.tick(1)
            ongoing = False
        elif set(cond).issubset(x_state):
            for i in range(0,3):
                screen.fill(team_x)
                message_to_screen("X Team wins the game!", black, 0, "large", "top")
                message_to_screen("Congratulations!", black, 0, "large", "bottom")
                pygame.display.flip()
                clock.tick(1)
                screen.fill(team_x)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    else:
                        print(event)
                pygame.display.flip()
                clock.tick(1)
            ongoing = False
    if not ongoing:
        MainMenu()
    else:
        gamescreen()



def MainMenu():
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

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()

qindex = random.sample(range(0, len(myDict)), 9)


def gamescreen():
    gameOver = False
    global ongoing, qindex, board_state, turn, o_state, x_state, win_conditions
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
                    qindex[i] = random.randint(0, len(myDict))
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
        gameOver = False
        transition = False
        draw = 0
        for i in board_state:
            if board_state[i][1] == True:
                draw += 1
        while not gameOver and draw < 9:
            current_pos = pygame.mouse.get_pos()
            current_cell = cell_pos(current_pos[0], current_pos[1])
            screen.fill(white)
            if turn % 2 == 0 and transition == False:
                message_to_screen('O\'s Turn!', team_o, 0, "large")
                pygame.display.flip()
                clock.tick(1)
                transition = True
            elif turn % 2 == 1 and transition == False:
                message_to_screen('X\'s Turn!', team_x, 0, "large")
                pygame.display.flip()
                clock.tick(1)
                transition = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        MainMenu()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if board_state[current_cell][1] == False:
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
                else:
                    bounds = get_cell(key)
                    if key in o_state:
                        screen.fill(team_o, rect=[bounds[0], bounds[2], cell_width, cell_height])
                        message_to_screen("O", black, key, "large")
                    elif key in x_state:
                        screen.fill(team_x, rect=[bounds[0], bounds[2], cell_width, cell_height])
                        message_to_screen("X", black, key, "large")
            if turn % 2 == 0:
                textSurf, textRect = text_objects('O\'s Turn', black, "small")
                textRect.bottom = display_height
                screen.blit(textSurf, textRect)
                pygame.display.update()
            elif turn % 2 == 1:
                textSurf, textRect = text_objects('X\'s Turn', black, "small")
                textRect.bottom = display_height
                textRect.right = display_width
                screen.blit(textSurf, textRect)
                pygame.display.update()
        if draw == 9:
            screen.fill(red)
            pygame.display.flip()
            clock.tick(1)
            message_to_screen(":(", white, 0, "large")
            pygame.display.flip()
            clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                else:
                    print(event)
            screen.fill(red)
            pygame.display.flip()
            clock.tick(1)
            message_to_screen("It\'s a stalemate", white, 0, "large", "top")
            message_to_screen("No one won.", white, 0, "large", )
            pygame.display.flip()
            clock.tick(1)
            while not gameOver:
                current_pos = pygame.mouse.get_pos()

                textSurf, textRect = text_objects("You all suck", white, "smaller")
                textRect.bottom = display_height
                textRect.center = (display_width / 2),(display_height - 20)
                if textRect.right >= current_pos[0] >= textRect.left and textRect.bottom >= current_pos[1] >= textRect.top:
                    screen.fill(bright_red, textRect)
                else:
                    screen.fill(red, textRect)
                screen.blit(textSurf, textRect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            ongoing = False
                            MainMenu()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if textRect.right >= current_pos[0] >= textRect.left and textRect.bottom >= current_pos[1] >= textRect.top:
                            ongoing = False
                            gameOver = True
                    pygame.display.update()
            MainMenu()
            clock.tick(FPS)


def question(index, cell):
    goBack = False
    global board_state, x_state, o_state
    while not goBack:
        current_pos = pygame.mouse.get_pos()
        screen.fill(white)
        print_question(myDict[index]['question'].capitalize(), black, medfont, "medium")
        correct, ans_bounds= print_answer(index, cell, black, smallfont, "small", turn % 2 == 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    goBack = True
                if event.key == pygame.K_SPACE:
                    countdown()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i,x in enumerate(ans_bounds):
                    if x.right >= current_pos[0] >= x.left and x.bottom >= current_pos[1] >= x.top:
                        if i == correct - 1:
                            result(cell, True)
                        elif i != correct - 1:
                            result(cell, False)
        pygame.display.update()
        clock.tick(FPS)

MainMenu()