import pygame
import csv
import random
from itertools import chain
from itertools import cycle
import math
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

image_danger = pygame.image.load('danger.png')
icon = pygame.image.load('cmicon.png')
bgimage = pygame.image.load('bg.jpg')

win_flavor = ("%s won the round!", "%s gets it!", "%s takes the cell!", "%s wins the round!", "Impressive win by %s!")
lose_flavor = ("%s steals it!", "%s grabs this one away!", "Stolen by %s!", "Effortless round for %s!", "%s, now\'s your chance!")

pygame.init()

pygame.mixer.music.load('bgm.mp3')
tick = pygame.mixer.Sound('tick.wav')
win = pygame.mixer.Sound('win.wav')
asa = pygame.mixer.Sound('asa.wav')
tbok = pygame.mixer.Sound('tbok.wav')
lol = pygame.mixer.Sound('lol.wav')
uy = pygame.mixer.Sound('uy.wav')

ongoing = False

FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
blue = (40, 79, 128)
green = (0, 155 ,0)
bright_green = (0, 255, 0)
team_o = (39, 167, 216)
team_x = (255, 154, 0)
red = (255, 0, 0)

display_width = 1920
display_height = 1080
cell_width = round(display_width/3)
cell_height = round(display_height/3)
if display_height == 720 and display_height == 1080:
    font_quotient = 1
else:
    font_quotient = 1.48

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tic Tac Trivia')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

smallerfont_frut = pygame.font.Font("frutiger.ttf", round(15 * font_quotient))
smallfont_frut = pygame.font.Font("frutiger.ttf", round(20 * font_quotient))
medfont_frut = pygame.font.Font("frutiger.ttf", round(40 * font_quotient))
largefont_frut = pygame.font.Font("frutiger.ttf", round(80 * font_quotient))

smallerfont_goth = pygame.font.Font("gotham.ttf", round(18 * font_quotient))
smallfont_goth = pygame.font.Font("gotham.ttf", round(25 * font_quotient))
medfont_goth = pygame.font.Font("gotham.ttf", round(50 * font_quotient))
largefont_goth = pygame.font.Font("gotham.ttf", round(80 * font_quotient))
superfont_goth = pygame.font.Font("gotham.ttf", round(100 * font_quotient))

BLINK_EVENT = pygame.USEREVENT + 0

win_conditions = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [1, 5, 9],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
        [3, 5, 7]]

gameOver = False

def quitgame():
    pygame.quit()
    quit()

def initvalues():
    global qindex, board_state, turn, o_state, x_state, isShuffled, order
    qindex = random.sample(range(0, len(myDict) - 1), 9)
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
    if size == "smallerfrut":
        textSurface = smallerfont_frut.render(text, True, color)
    elif size == "smallfrut":
        textSurface = smallfont_frut.render(text, True, color)
    elif size == "mediumfrut":
        textSurface = medfont_frut.render(text, True, color)
    elif size == "largefrut":
        textSurface = largefont_frut.render(text, True, color)
    elif size == "smallergoth":
        textSurface = smallerfont_goth.render(text, True, color)
    elif size == "smallgoth":
        textSurface = smallfont_goth.render(text, True, color)
    elif size == "mediumgoth":
        textSurface = medfont_goth.render(text, True, color)
    elif size == "largegoth":
        textSurface = largefont_goth.render(text, True, color)
    elif size == "supergoth":
        textSurface = superfont_goth.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, cell, size = "smallfrut", y_align = "center"):
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
    is_clicked = False
    click = pygame.mouse.get_pressed()
    bounds = get_cell(cell)
    cellRect = pygame.Rect(bounds[0], bounds[2], bounds[1] - bounds[0], bounds[3] - bounds[2])
    if cellRect.collidepoint(pygame.mouse.get_pos()):
        screen.fill(ac, cellRect)
        if click[0] == True and action != None and not is_clicked:
            # pygame.time.wait(500)
            is_clicked = True
            tick.play()
            action()


    else:
        screen.fill(ic, cellRect)
    message_to_screen(text, fc, cell, fs)

def print_question(text, color, font, size):
    qwrap = wrapline(text, font, display_width)
    height = 0
    for x in qwrap:
        textSurf, textRect = text_objects(x, color, size)
        textRect.center = (display_width // 2), ((display_height // 8) + height)
        height += (textRect.bottom - textRect.top)
        screen.blit(textSurf, textRect)

def print_answer(index, cell, color, font, size, turn=None):
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
        qwrap = wrapline(choices[i - 1][0], font, display_width // 4)
        print(qwrap)
        height = 0
        width = 0
        xRect = 0
        yRect = 0
        tempSurf = []
        tempRect = []
        for z, y in enumerate(qwrap):
            textSurf, textRect = text_objects(y, color, size)
            textRect.center = (((display_width // 2) * (x % 2)) + (display_width // 4)), (
                (display_height // 2) + ((display_height // 4) * (x // 2)) + height)
            tempSurf.extend([textSurf])
            tempRect.extend([textRect])
            if z == 0:
                xRect = textRect.left
                yRect = textRect.top
            height += (textRect.bottom - textRect.top)
            if width < (textRect.right - textRect.left):
                width = (textRect.right - textRect.left)
            screen.blit(textSurf, textRect)
        newRect = pygame.Rect(xRect, yRect, width, height)
        print(tempSurf, tempRect, newRect)
        if choices[i - 1][1] == True:
            correct = x + 1
        answer_bound.append(newRect)
        if newRect.collidepoint(pygame.mouse.get_pos()):
            if turn == True:
                screen.fill(team_o, newRect)
            elif turn == False:
                screen.fill(team_x, newRect)
        for i in range(0, len(tempSurf)):
            screen.blit(tempSurf[i], tempRect[i])
    pygame.display.update()
    return correct, answer_bound

def countdown():
    counter = 15
    loop = True
    pygame.mixer.music.set_volume(0.2)
    tbok.play()
    while loop:
        if counter == 0:
            tbok.stop()
            asa.play()
            textSurf, textRect = text_objects("Time's up!", (255, 0, 0), "largegoth")
            textRect.center = ((display_width // 2), ((display_height // 8) * 7))
            offSurf = pygame.Surface(textRect.size)
            offSurf.fill(blue)
            blink_surfaces = cycle([textSurf, offSurf])
            blink_surface = next(blink_surfaces)
            pygame.time.set_timer(BLINK_EVENT, 300)
            time = 0
            print(BLINK_EVENT)
            while True:
                for event in pygame.event.get():
                    time += clock.get_time()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return
                    if event.type == BLINK_EVENT:
                        blink_surface = next(blink_surfaces)
                screen.blit(blink_surface, textRect)
                pygame.display.update()
                clock.tick(60)
        else:
            textSurf, textRect = text_objects(str(counter), white, "largegoth")
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
        screen.fill(blue, textRect)
        pygame.display.flip()
        counter -= 1
        if counter < 0:
            loop = False
    pygame.mixer.music.set_volume(0.5)

def result(cell, correct=None, answer=None):
    global board_state, turn, o_state, x_state, ongoing
    board_state[cell][1] = True
    screen.fill(white)
    if turn % 2 == 0:
        if correct == True:
            team = "O"
            o_state.append(cell)
            message_to_screen((random.choice(win_flavor) % team), team_o, 0, "largegoth")
        else:
            team = "X"
            x_state.append(cell)
            message_to_screen((random.choice(lose_flavor) % team), team_x, 0, "largegoth")
        turn = 1
    elif turn % 2 == 1:
        if correct == True:
            team = "X"
            x_state.append(cell)
            message_to_screen((random.choice(win_flavor) % team), team_x, 0, "largegoth")
        else:
            team = "O"
            o_state.append(cell)
            message_to_screen((random.choice(lose_flavor) % team), team_o, 0, "largegoth")
        turn = 0
    pygame.display.flip()
    clock.tick(1)
    clock.tick(1)

    for cond in win_conditions:
        if set(cond).issubset(o_state):
            win.play()
            screen.fill(team_o)
            textSurf1, textRect1 = text_objects("O Team wins the game!", black, "largegoth")
            textRect1.center = (display_width // 2), (display_height // 3)
            textSurf2, textRect2 = text_objects("Congratulations!", black, "largegoth")
            textRect2.center = (display_width // 2), ((display_height // 3) * 2)
            offSurf = pygame.Surface(screen.get_rect().size)
            offSurf.fill(team_o)
            blink_surfaces1 = cycle([textSurf1, offSurf])
            blink_surface1 = next(blink_surfaces1)
            blink_surfaces2 = cycle([textSurf2, offSurf])
            blink_surface2 = next(blink_surfaces2)
            pygame.time.set_timer(BLINK_EVENT, 300)
            print(BLINK_EVENT)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            ongoing = False
                            MainMenu()
                    if event.type == BLINK_EVENT:
                        blink_surface1 = next(blink_surfaces1)
                        blink_surface2 = next(blink_surfaces2)
                screen.blit(blink_surface1, textRect1)
                screen.blit(blink_surface2, textRect2)
                pygame.display.update()
                clock.tick(60)
        elif set(cond).issubset(x_state):
            win.play()
            for i in range(0,3):
                screen.fill(team_x)
                message_to_screen("X Team wins the game!", black, 0, "largegoth", "top")
                message_to_screen("Congratulations!", black, 0, "largegoth", "bottom")
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

def get_new_dims(sourceW, sourceH, surfW, surfH):
    surf_area = surfW * surfH

    source_ratio = float(sourceW / sourceH)
    new_h = round((math.sqrt(surf_area / source_ratio)))
    new_w = round(((new_h * source_ratio)))

    return new_h, new_w

def suddendeath():
    if dupecheck.count(1) == 100:
        print("FULL")
    else:
        q = random.randint(0, len(myDict) - 1)
        if dupecheck[q] == 1:
            q = random.randint(0, len(myDict) - 1)
        else:
            print(q)
            dupecheck[q] = 1

    with open('dupecheck.txt', 'w+') as file:
        for line in dupecheck:
            if line == 1:
                file.write('1\n')
            elif line == 0:
                file.write('0\n')
            file.truncate()

    shuffled = False
    won = False
    choices = []
    # pygame.display.update()
    while not won:
        is_clicked = False
        screen.fill(blue)
        print_question(myDict[q]['question'].capitalize(), white, medfont_frut, "mediumfrut")
        if myDict[q]['type'] == 'multiple':
            if shuffled == False:
                qset = [1, 2, 3, 4]
                random.shuffle(qset)
                shuffled = True
            choices.append([myDict[q]['correct_answer'], True])
            choices.append([myDict[q]['incorrect_answers/0'], False])
            choices.append([myDict[q]['incorrect_answers/1'], False])
            choices.append([myDict[q]['incorrect_answers/2'], False])
        if myDict[q]['type'] == 'boolean':
            if shuffled == False:
                qset = [1, 2]
                random.shuffle(qset)
                shuffled = True
            choices.append([myDict[q]['correct_answer'], True])
            choices.append([myDict[q]['incorrect_answers/0'], False])
        # qorder = qset
        answer_bound = []
        for x, i in enumerate(qset):
            qwrap = wrapline(choices[i - 1][0], smallfont_frut, display_width // 4)
            print(qwrap)
            height = 0
            width = 0
            xRect = 0
            yRect = 0
            tempSurf = []
            tempRect = []
            for z, y in enumerate(qwrap):
                textSurf, textRect = text_objects(y, white, "mediumfrut")
                textRect.center = (((display_width // 2) * (x % 2)) + (display_width // 4)), (
                    (display_height // 2) + ((display_height // 4) * (x // 2)) + height)
                tempSurf.extend([textSurf])
                tempRect.extend([textRect])
                if z == 0:
                    xRect = textRect.left
                    yRect = textRect.top
                height += (textRect.bottom - textRect.top)
                if width < (textRect.right - textRect.left):
                    width = (textRect.right - textRect.left)
                screen.blit(textSurf, textRect)
            newRect = pygame.Rect(xRect, yRect, width, height)
            print(tempSurf, tempRect, newRect)
            if choices[i - 1][1] == True:
                correct = x + 1
            answer_bound.append(newRect)
            if newRect.collidepoint(pygame.mouse.get_pos()):
                screen.fill(green, newRect)
            for i in range(0, len(tempSurf)):
                screen.blit(tempSurf[i], tempRect[i])
        pygame.display.update()
        is_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    countdown()
                if event.key == pygame.K_ESCAPE:
                    goBack = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not is_clicked:
                # pygame.time.wait(500)
                for i,x in enumerate(answer_bound):
                    if x.collidepoint(pygame.mouse.get_pos()):
                        if i == correct - 1:
                            tick.play()
                            screen.fill(blue)
                            is_clicked = True
                            message_to_screen("Correct!", green, 0, "largegoth")
                            won = True
                        elif i != correct - 1:
                            tick.play()
                            is_clicked = True
                            screen.fill(blue)
                            message_to_screen("Wrong!", green, 0, "largegoth")
                            won = False
                pygame.display.update()
                clock.tick(1)
                clock.tick(1)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
    MainMenu()

def MainMenu():
    gameExit = True
    while gameExit:
        screen.fill(blue)

        bg = bgimage.convert_alpha()
        new_h, new_w = get_new_dims(bg.get_size()[0], bg.get_size()[1], (cell_height * 2), (cell_width * 2))
        bgimg = pygame.transform.smoothscale(bg, (new_w, new_h))
        bgimageRect = bgimg.get_rect()
        minX = cell_width
        maxX = display_width
        minY = 0
        maxY = cell_height * 2
        bgimageRect.center = (minX * 2), (minY + (maxY / 2))
        screen.blit(bgimg, bgimageRect)

        if not ongoing:
            cell_button("New Game", 1, white, "mediumgoth", gray, blue, gamescreen)
            cell_button("", 9, white, "mediumgoth", gray, blue, suddendeath)
        else:
            cell_button("Resume Game", 1, white, "mediumgoth", gray, blue, gamescreen)
            cell_button("", 9, white, "mediumgoth", gray, blue)

        cell_button("Options", 4, white, "mediumgoth", gray, blue, options)
        cell_button("", 8, blue, "mediumgoth", blue, blue,)

        img = image_danger.convert_alpha()
        new_h, new_w = get_new_dims(img.get_size()[0], img.get_size()[1], (cell_height // 1.5), (cell_width // 1.5))
        danger = pygame.transform.smoothscale(img, (new_w, new_h))
        imageRect = danger.get_rect()
        minX, maxX, minY, maxY = get_cell(9)
        imageRect.center = (minX + (cell_width // 2)), (minY + (cell_height // 2))
        boundRect = pygame.Rect(get_cell(9)[0], get_cell(9)[2], get_cell(9)[1] - get_cell(9)[0], get_cell(9)[3] - get_cell(9)[2])
        if boundRect.collidepoint(pygame.mouse.get_pos()):
            if not ongoing:
                message_to_screen("SUDDEN DEATH", white, 9, "mediumgoth")
            else:
                screen.blit(danger, imageRect)
        else:
            screen.blit(danger, imageRect)

        cell_button("Quit", 7, white, "mediumgoth", gray, blue, quitgame)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
    pygame.quit()
    quit()




def gamescreen():
    global ongoing, qindex, board_state, turn, o_state, x_state, win_conditions, gameOver
    if ongoing == False:
        initvalues()
        print(qindex)
        for i,q in enumerate(qindex):
            if dupecheck[q] == 0:
                dupecheck[q] = 1
            else:
                while dupecheck[q] != 1:
                    qindex[i] = random.randint(0, len(myDict)-1)
                    if dupecheck[q] == 0:
                        dupecheck[q] = 1
        print(qindex)
        with fileinput.FileInput('dupecheck.txt', inplace=True, backup='.bak') as file:
            for i, line in enumerate(file):
                if dupecheck[i] == 1:
                    print(line.replace('0', '1'), end='')
                else:
                    print(line.replace('0', '0'), end='')
        for key, cell in board_state.items():
            cell[0] = qindex[key-1]
        ongoing = True
    else:
        is_clicked = False
        transition = False
        draw = 0
        for i in board_state:
            if board_state[i][1] == True:
                draw += 1
        while not gameOver and draw < 9:
            current_cell = cell_pos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            screen.fill(white)
            if turn % 2 == 0 and transition == False:
                message_to_screen('O\'s Turn!', team_o, 0, "largegoth")
                pygame.display.flip()
                clock.tick(1)
                transition = True
            elif turn % 2 == 1 and transition == False:
                message_to_screen('X\'s Turn!', team_x, 0, "largegoth")
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not is_clicked:
                    # pygame.time.wait(500)
                    if board_state[current_cell][1] == False:
                        tick.play()
                        question(qindex[current_cell-1], current_cell)
                    is_clicked = pygame.mouse.get_pressed()[0]
            for key, cell in board_state.items():
                if cell[1] == False:
                    bounds = get_cell(key)
                    boundRect = pygame.Rect(bounds[0], bounds[2], bounds[1] - bounds[0], bounds[3] - bounds[2])
                    if boundRect.collidepoint(pygame.mouse.get_pos()):
                        screen.fill(gray, boundRect)
                    else:
                        screen.fill(blue, boundRect)
                    message_to_screen(myDict[qindex[key - 1]]['category'].capitalize(), white, key, "smallerfrut", "top")
                    message_to_screen(myDict[qindex[key - 1]]['difficulty'].capitalize(), white, key, "mediumfrut", "bottom")
                else:
                    bounds = get_cell(key)
                    boundRect = pygame.Rect(bounds[0], bounds[2], bounds[1] - bounds[0], bounds[3] - bounds[2])
                    if key in o_state:
                        screen.fill(team_o, boundRect)
                        message_to_screen("O", black, key, "supergoth")
                    elif key in x_state:
                        screen.fill(team_x, boundRect)
                        message_to_screen("X", black, key, "supergoth")
            if turn % 2 == 0:
                textSurf, textRect = text_objects('O\'s Turn', black, "smallfrut")
                textRect.bottom = display_height
                screen.blit(textSurf, textRect)
                pygame.display.update()
            elif turn % 2 == 1:
                textSurf, textRect = text_objects('X\'s Turn', black, "smallfrut")
                textRect.bottom = display_height
                textRect.right = display_width
                screen.blit(textSurf, textRect)
                pygame.display.update()
        if draw == 9:
            is_clicked = False
            lol.play()
            screen.fill(blue)
            pygame.display.flip()
            clock.tick(1)
            message_to_screen(":(", white, 0, "largefrut")
            pygame.display.flip()
            clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                else:
                    print(event)
            screen.fill(blue)
            pygame.display.flip()
            clock.tick(1)
            message_to_screen("It\'s a stalemate", white, 0, "largegoth", "top")
            message_to_screen("No one won.", white, 0, "largegoth", )
            pygame.display.flip()
            clock.tick(1)
            while ongoing:
                textSurf, textRect = text_objects("You all suck :(", white, "smallergoth")
                textRect.bottom = display_height
                textRect.center = (display_width / 2),(display_height - 20)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            ongoing = False
                            MainMenu()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # pygame.time.wait(500)
                        if textRect.collidepoint(pygame.mouse.get_pos()) and not is_clicked:
                            tick.play()
                            ongoing = False
                            is_clicked = True
                            MainMenu()
                if textRect.collidepoint(pygame.mouse.get_pos()):
                    screen.fill(gray, textRect)
                else:
                    screen.fill(blue, textRect)
                screen.blit(textSurf, textRect)
    MainMenu()
    clock.tick(FPS)

def question(index, cell):
    goBack = False
    global board_state, x_state, o_state
    # if cell == 0:
    #     while not goBack:
    #         is_clicked = False
    #         screen.fill(blue)
    #         print_question(myDict[index]['question'].capitalize(), white, medfont_frut, "mediumfrut")
    #         correct, ans_bounds= print_answer(index, cell, white, medfont_frut, "mediumfrut")
    #
    #         pygame.display.update()
    #         clock.tick(FPS)
    # else:
    while not goBack:
        is_clicked = False
        current_pos = pygame.mouse.get_pos()
        screen.fill(blue)
        print_question(myDict[index]['question'].capitalize(), white, medfont_frut, "mediumfrut")
        correct, ans_bounds= print_answer(index, cell, white, medfont_frut, "mediumfrut", turn % 2 == 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    countdown()
                if event.key == pygame.K_ESCAPE:
                    goBack = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not is_clicked:
                # pygame.time.wait(500)
                tick.play()
                is_clicked = True
                for i,x in enumerate(ans_bounds):
                    if x.collidepoint(pygame.mouse.get_pos()):
                        if i == correct - 1:
                            result(cell, True)
                        elif i != correct - 1:
                            result(cell, False)
        # clock.tick(FPS)

def options():
    goBack = False
    while not goBack:
        screen.fill(blue)
        cell_button("Reset State", 5, white, "largefrut", gray, blue, reset)
        cell_button("Ok.", 8, white, "mediumfrut", gray, blue, MainMenu)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()

def reset():
    global dupecheck
    is_clicked = False
    save = None
    uy.play()
    while save == None:
        screen.fill(blue)
        message_to_screen("Warning: This will reset all duplicate questions!", red, 2, "mediumfrut", "top")
        message_to_screen("Are you sure?", white, 5, "largefrut", "top")
        saveSurf, saveRect= text_objects("Yes!", white, "mediumgoth")
        saveRect.center= (display_width // 4), ((display_height // 4) * 3)
        noSurf, noRect = text_objects("Go back.", white, "mediumgoth")
        noRect.center = ((display_width // 4) * 3),  ((display_height // 4) * 3)
        if saveRect.collidepoint(pygame.mouse.get_pos()):
            screen.fill(gray, saveRect)
        else:
            screen.fill(blue, saveRect)
        screen.blit(saveSurf, saveRect)
        if noRect.collidepoint(pygame.mouse.get_pos()):
            screen.fill(gray, noRect)
        else:
            screen.fill(blue, noRect)
        screen.blit(noSurf, noRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not is_clicked:
                # pygame.time.wait(500)
                if saveRect.collidepoint(pygame.mouse.get_pos()):
                    tick.play()
                    save = True
                elif noRect.collidepoint(pygame.mouse.get_pos()):
                    tick.play()
                    save = False
    if save == True:
        print(len(myDict))
        dupecheck = []
        for i in range(0, len(myDict)):
            dupecheck.extend([0])
        print(dupecheck)
        with open('dupecheck.txt', 'w+') as file:
            for line in dupecheck:
                file.write((str(line) + "\n"))
            file.truncate()
        # with fileinput.FileInput('dupecheck.txt', inplace=True, backup='.bak') as file:
        #     for i in dupecheck:
        #         print>>file, i

pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
MainMenu()