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

def text_objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color):
    textSurf, textRect = text_objects(msg, color)
    # screen_text = font.render(msg, True, color)
    # gameDisplay.blit(screen_text, [display_width/2, display_height/2])
    textRect.center = (display_width/2), (display_height/2)
    gameDisplay.blit(textSurf, textRect)

def GameLoop():
    # gameOver = False
    gameExit = False



    while not gameExit:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                gameExit = True


        screen.fill(white)

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

        pygame.display.update()

        clock.tick(60)

    pygame.quit()
    quit()

GameLoop()