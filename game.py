import pygame
import csv

anime = csv.DictReader(open('50animequestions.csv', encoding="utf8"))
vg = csv.DictReader(open('50videogamequestions.csv', encoding="utf8"))
myDict = []
for row in anime:
    # print(row)
    myDict.append(row)
for row in vg:
    myDict.append(row)

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (155, 0, 0)
green = (0, 155 ,0)
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

def cell_button(text, cell, fc, fs, ac, ic):
    mouse = pygame.mouse.get_pos()
    bounds = get_cell(cell)
    print(bounds)
    if bounds[1] >= mouse[0] >= bounds[0] and bounds[3] >= mouse[1] >= bounds[2]:
        screen.fill(ac, rect=[bounds[0], bounds[2], cell_width, cell_height])
    else:
        screen.fill(ic, rect=[bounds[0], bounds[2], cell_width, cell_height])
    message_to_screen(text, fc, cell, fs)


def GameLoop():
    # gameOver = False
    gameExit = False


    while not gameExit:
        for event in pygame.event.get():
            screen.fill(white)
            message_to_screen("TIC", black, 1, size="large")
            message_to_screen("TAC", black, 2, size="large")
            message_to_screen("TRIVIA", black, 3, size="large")

            cell_button("New Game", 4, white, "medium", bright_red, red)
            cell_button("Demo", 5, white, "medium", bright_red, red)
            cell_button("Options", 6, white, "medium", bright_red, red)
            cell_button("Quit", 8, white, "medium", bright_red, red)

            print(event)


            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if quitBounds[1] >= pos[0] >= quitBounds[0] and quitBounds[3] >= pos[1] >= quitBounds[2]:
                # if pos[0] >= quitBounds[0] and pos[0] <= quitBounds[1]:
                #     if pos[1] >= quitBounds[2] and pos[1] <= quitBounds[3]:
                        gameExit = True
            if event.type == pygame.QUIT:
                gameExit = True



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

        clock.tick(60)

    pygame.quit()
    quit()

GameLoop()