import pygame

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (155, 0, 0)
green = (0, 155 ,0)

display_width = 1920
display_height = 1080
cell_width = round(display_width/3)
cell_height = round(display_height/3)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('TicTacTrivia')

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

def text_objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, cell):
    textSurf, textRect = text_objects(msg, color)
    if cell is 0:
        textRect.center = (display_width / 2), (display_height / 2)
    elif cell <= 3 and cell >= 1:
        textRect.center = (((cell_width * ((cell - 1) % 3)) + (cell_width / 2)), (cell_height / 2))
    elif cell <= 6 and cell >= 4:
        textRect.center = (((cell_width * ((cell - 1) % 3)) + (cell_width / 2)), (cell_height + (cell_height / 2)))
    elif cell <= 9 and cell >= 7:
        textRect.center = (((cell_width * ((cell - 1) % 3)) + (cell_width / 2)), (cell_height + cell_height + (cell_height / 2)))
    screen.blit(textSurf, textRect)

def GameLoop():
    # gameOver = False
    gameExit = False



    while not gameExit:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                gameExit = True


        screen.fill(white)

        message_to_screen("Tic", black, 1)
        message_to_screen("Tac", black, 2)
        message_to_screen("Trivia", black, 3)

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