import pygame
import csv
import random
import fileinput

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

go_back = 0


board_state = { 1: [-1, False],
                2: [-1, False],
                3: [-1, False],
                4: [-1, False],
                5: [-1, False],
                6: [-1, False],
                7: [-1, False],
                8: [-1, False],
                9: [-1, False] }
                # [question index, is answered]

o_state = [ False,
              False,
              False,
              False,
              False,
              False,
              False,
              False,
              False ]

x_state = [ False,
              False,
              False,
              False,
              False,
              False,
              False,
              False,
              False ]

win_conditions = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                [1, 5, 9],
                [1, 4, 7],
                [2, 5, 8],
                [3, 6, 9],
                [3, 5, 7]]

FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)
red = (155, 0, 0)
green = (0, 155 ,0)
bright_green = (0, 255, 0)
bright_red = (255,0, 0)

display_width = 1280
display_height = 720
cell_width = round(display_width/3)
cell_height = round(display_height/3)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('TicTacTrivia')

clock = pygame.time.Clock()
# smallfont = pygame.font.SysFont(None, 25)
smallfont = pygame.font.SysFont("tahoma", 25)
medfont = pygame.font.SysFont("tahoma", 50)
largefont = pygame.font.SysFont("tahoma", 80)

def quitgame():
    pygame.quit()
    quit()

def goback():
    global go_back
    go_back = 1

def question(index):
    global board_state


    # for i in board_state:
    #     board_state[0] = random.randint(0,99
    # screen.fill(white)
    # cell_button("Yes", 4, black, "medium", white, white, )

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, cell, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    if cell is 0:
        textRect.center = (display_width / 2), (display_height / 2)
    elif cell <= 3 and cell >= 1:
        textRect.center = (((cell_width * ((cell - 1) % 3)) + (cell_width / 2)), (cell_height / 2))
    elif cell <= 6 and cell >= 4:
        textRect.center = (((cell_width * ((cell - 1) % 3)) + (cell_width / 2)), (cell_height + (cell_height / 2)))
    elif cell <= 9 and cell >= 7:
        textRect.center = (((cell_width * ((cell - 1) % 3)) + (cell_width / 2)), (cell_height + cell_height + (cell_height / 2)))
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

def MainMenu():
    # gameOver = False
    gameExit = True


    while gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(white)
        message_to_screen("TIC", black, 1, size="large")
        message_to_screen("TAC", black, 2, size="large")
        message_to_screen("TRIVIA", black, 3, size="large")

        cell_button("New Game", 4, white, "medium", bright_red, red, gamescreen)
        cell_button("Demo", 5, white, "medium", bright_red, red)
        cell_button("Options", 6, white, "medium", bright_red, red)
        cell_button("Quit", 8, white, "medium", bright_red, red, quitgame)

        print(event)



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

def gamescreen():
    gameOver = False
    # global go_back
    # global board_state, o_state, x_state
    qindex = random.sample(range(1,100), 10)
    print(qindex)
    for i,q in enumerate(qindex):
        print(i,q)
        print(dupecheck[q])
        if dupecheck[q] == 0:
            dupecheck[q] = 1
            # with open('dupecheck.txt', 'w') as file:
            #     for line in file:
            #         if line == q:
            #             file.writelines('1\n')
            #         else:
            #             file.writelines('0\n')
        else:
            while dupecheck[q] != 1:
                qindex[i] = random.randint(1, 100)
                if dupecheck[q] == 0:
                    dupecheck[q] = 1
                    # with open('dupecheck.txt', 'w') as file:
                    #     for line in file:
                    #         if line == q:
                    #             file.writelines('1\n')
                    #         else:
                    #             file.writelines('0\n')
        print(dupecheck[q])
    print(qindex)
    for x,i in enumerate(dupecheck):
        if i == 1:
            print(x)
    # with open('dupecheck.txt', 'a') as file:
    #     for line in file:
    #             file.write(str(line)+'\n')
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameOver = True
        screen.fill(white)
        # for i in range(1,10):

        # for i in board_state:
        #     if board_state[0] == False:
        #         cell_button("?", i, black, "large", white, white, question)
        #     else

        # cell_button("Back to Main Menu", 7, black, "medium", bright_red, red, goback)
        # if go_back == 1:
        #     gameOver = True
        #     go_back = 0
        pygame.display.update()
        clock.tick(FPS)

MainMenu()