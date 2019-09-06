#!/usr/bin/env python

"""Snake-like pygame."""

import pygame
import time
import pickle

# start pygame
pygame.init()

# set screen size
display_width = 800
display_height = 600

# setting rgb colour values
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grass = (107, 138, 81)
blue = (0, 0, 255)
brown = (51, 42, 18)
button_grey = (66, 87, 49)
button_hover = brown
initial = (71, 92, 54)

# set images location and sizes
cowImg = pygame.image.load('images/cow.png')
wocImg = pygame.image.load('images/woc.png')
cow_width = 64
cow_height = 64

# pygame boilerplate
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('poopie cow')  # set screen's title
pygame.display.set_icon(cowImg)  # set icon for taskbar
clock = pygame.time.Clock()

# sound(s)
# make a moo sound
moo_file = "sounds/moo1.wav"
moo_sound = pygame.mixer.music.load(moo_file)


def get_best_scores():
    """Get previous high scores."""
    with open('pickled_scores', 'rb') as ps:
        best_scores = pickle.load(ps)
    return best_scores


def cow(x, y, facing_right):
    """Draw the appropriate cow."""
    if facing_right:
        cow_img = cowImg
        gameDisplay.blit(cow_img, (x + 2, y + 2))
    else:
        cow_img = wocImg
        x = x - cow_width
        gameDisplay.blit(cow_img, (x - 2, y - 2))


def cow_bounds(x, y, facing_right):
    """Return contact points to check for stepping in poo trail."""
    """x,y as well as poos are multiples of 5 given start position
    and move_delta.  Will ignore x,y itself(?) and return other possible
    bounds for checking against poo_trail."""

    bounds = []
    if not facing_right:
        x -= 65
    # bottom and top sides
    for i in range(x + 5, x + 60, 5):
        bounds.append((i, y))
        bounds.append((i, y - 60))
    # left and right sides
    for j in range(y - 5, y - 60, -5):
        bounds.append((x + 5, j))
        bounds.append((x + 60, j))
    return bounds


def poo(x, y, color):
    """Draw a poop."""
    poox = int(x - 2)
    pooy = int(y + cow_height - 10)
    pygame.draw.circle(gameDisplay, color, (poox, pooy), 5)


def text_objects(text, font):
    """Render text into pygame friendly format.  Messy."""
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def moo(x, y):
    """Draw 'moo' in the appropriate spot."""
    moo_font = pygame.font.Font('freesansbold.ttf', int(cow_height / 4))
    TextSurf, TextRect = text_objects('moo', moo_font)

    if y < display_height * 0.45:
        top_half = True
    else:
        top_half = False
    moo_y = y
    if top_half:
        moo_y += cow_height
    TextRect.center = ((x + cow_width), (moo_y))

    gameDisplay.blit(TextSurf, TextRect)


def score(count):
    """Display score."""
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("poops: " + str(count), True, white)
    gameDisplay.blit(text, (10, 10))


def best_score(count):
    """Display best score of session."""
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("most poops: " + str(count), True, white)
    gameDisplay.blit(text, (display_width - 180, 10))


def q_to_quit():
    """Display quit key message.  Was 'q' now 'enter'."""
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render("press 'space' to quit", True, white)
    gameDisplay.blit(text, (display_width / 2 - 60, 20))


def show_instructions():
    """Display instructions prior to beginning game."""
    font = pygame.font.Font('freesansbold.ttf', 20)

    instructions1 = "Use arrow keys to change direction"
    instructions2 = "Don't touch the poop!"
    textSurf1, textRect1 = text_objects(instructions1, font)
    textSurf2, textRect2 = text_objects(instructions2, font)
    textRect1.center = (display_width / 2, display_height / 2 - 120)
    textRect2.center = (display_width / 2, display_height / 2 - 80)
    gameDisplay.blit(textSurf1, textRect1)
    gameDisplay.blit(textSurf2, textRect2)


def about_screen():
    """Handle all the formatting for the About screen."""
    about = True
    while about:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(grass)

        font = pygame.font.Font('freesansbold.ttf', 20)

        version_credit = "poopie cow V0.9"
        coding_credit = "Author: benjamin.field@gmail.com"
        icon_credit = "Icon made by Freepik from www.flaticon.com"
        dedication1 = "For Libby and Julianna, whom like many pre-teens, find all"
        dedication2 = "things scatalogical to be udderly (sic) hilarious."
        dedication3 = "Uncle Ben thinks you both are the best."
        ver_surf, ver_rect = text_objects(version_credit, font)

        textSurf1, textRect1 = text_objects(coding_credit, font)
        textSurf2, textRect2 = text_objects(icon_credit, font)
        dedSurf1, dedRect1 = text_objects(dedication1, font)
        dedSurf2, dedRect2 = text_objects(dedication2, font)
        dedSurf3, dedRect3 = text_objects(dedication3, font)
        ver_rect.center = (display_width / 2, display_height / 2 - 160)
        textRect1.center = (display_width / 2, display_height / 2 - 120)
        dedRect1.center = (display_width / 2, display_height / 2 - 40)
        dedRect2.center = (display_width / 2, display_height / 2)
        dedRect3.center = (display_width / 2, display_height / 2 + 40)
        textRect2.center = (display_width / 2, display_height / 2 + 100)
        gameDisplay.blit(ver_surf, ver_rect)
        gameDisplay.blit(textSurf1, textRect1)
        gameDisplay.blit(dedSurf1, dedRect1)
        gameDisplay.blit(dedSurf2, dedRect2)
        gameDisplay.blit(dedSurf3, dedRect3)
        gameDisplay.blit(textSurf2, textRect2)

        back = button(display_width / 2 - 75, display_height * .8, 'back')

        if back:
            about = False

        pygame.display.update()
        clock.tick(15)
    intro_screen()


def letter_box(x, y, text, box_width=50, box_height=50, box_colour=button_grey, active=False):
    """Format letter boxes for best scores screen."""
    if active:
        pygame.draw.rect(gameDisplay, white, (x - 2, y - 2, box_width + 4, box_height + 4))
    pygame.draw.rect(gameDisplay, box_colour, (x, y, box_width, box_height))

    box_font = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(text, box_font)
    textRect.center = (x + (box_width / 2), y + (box_height / 2))
    gameDisplay.blit(textSurf, textRect)


def best_screen(better_than=0):
    """Format and logic for best scores screen."""
    best = True
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_']

    best_scores = get_best_scores()

    horiz_gap = 20
    vert_gap = 20

    letter_delta = 0

    space_pressed = False
    red_button = False

    tl_index = 0
    inits_2b_saved = False

    while best:

        # where to start displaying letter boxes
        letters_top_left_y = 175

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # deal with keypresses to scroll through alphabet
            if event.type == pygame.KEYDOWN:

                # vertical
                if event.key == pygame.K_UP:
                    letter_delta += 1
                    if letter_delta > 26:
                        letter_delta -= 27
                elif event.key == pygame.K_DOWN:
                    letter_delta -= 1
                    if letter_delta < 0:
                        letter_delta += 27
                elif event.key == pygame.K_SPACE:
                    space_pressed = True

            # This section not needed for constant movement
            # deal with keyrelease (no longer held down)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    # letter_delta = 0
                    pass

        gameDisplay.fill(grass)

        font = pygame.font.Font('freesansbold.ttf', 30)
        msg_font = pygame.font.Font('freesansbold.ttf', 15)

        coding_credit = "Best Scores"
        icon_credit = "Uncle Ben: Infinity!"
        textSurf1, textRect1 = text_objects(coding_credit, font)
        textSurf2, textRect2 = text_objects(icon_credit, font)
        textRect1.center = (display_width / 2, display_height / 2 - 120)
        textRect2.center = (display_width / 2, display_height / 2 - 80)

        new_best_row = 6 - better_than
        row_num = 1
        for bs in best_scores:
            letters_top_left_x = 200

            for j in range(0, 3):
                if new_best_row != row_num:
                    letter_box(letters_top_left_x, letters_top_left_y,
                               alphabet[bs[j]], active=False)
                    letters_top_left_x += 50 + horiz_gap
                else:
                    letter_box(letters_top_left_x, letters_top_left_y, alphabet[bs[j]],
                               box_colour=initial, active=True)
                    letters_top_left_x += 50 + horiz_gap
                    if j == 2:
                        red_button = button2(letters_top_left_x + 35, letters_top_left_y + 25, 25)

            score_surf, score_rect = text_objects(str(bs[3]), font)
            score_rect.center = (letters_top_left_x + 125, letters_top_left_y + 23)
            gameDisplay.blit(score_surf, score_rect)
            letters_top_left_y += 50 + vert_gap
            row_num += 1

        if new_best_row <= 5:
            inits_2b_saved = True
            nbrow_y = 125 + (new_best_row * (50 + vert_gap))
            enter_surf, enter_rect = text_objects("use up/down arrow keys", msg_font)
            enter_rect.center = (100, nbrow_y - 6)
            msg_surf, msg_rect = text_objects("to enter your intials", msg_font)
            msg_rect.center = (100, nbrow_y + 10)
            press_surf, press_rect = text_objects("press button or", msg_font)
            press_rect.center = (690, nbrow_y - 6)
            bar_surf, bar_rect = text_objects("spacebar to accept", msg_font)
            bar_rect.center = (690, nbrow_y + 10)
            gameDisplay.blit(enter_surf, enter_rect)
            gameDisplay.blit(msg_surf, msg_rect)
            gameDisplay.blit(press_surf, press_rect)
            gameDisplay.blit(bar_surf, bar_rect)

            # cycle through letters
            new_row = best_scores[new_best_row - 1]
            letters_top_left_x = 200

            this_letter = new_row[tl_index]
            this_letter = this_letter + letter_delta
            if this_letter > 26:
                this_letter -= 27
            if this_letter < 0:
                this_letter += 27

            letter_box(letters_top_left_x + tl_index * (50 + horiz_gap), nbrow_y - vert_gap,
                       alphabet[this_letter], box_colour=black, active=True)

            if space_pressed or red_button:
                # print("space pressed")
                new_row[tl_index] = this_letter
                letter_delta = 0
                space_pressed = False
                red_button = False
                tl_index += 1
                # print(tl_index)
                if tl_index > 2:
                    inits_2b_saved = False
                    with open('pickled_scores', 'wb') as pt:
                            pickle.dump(best_scores, pt, protocol=2)
                    best_screen()
                    tl_index = 0

        name_surf, name_rect = text_objects("pooper", font)
        name_rect.center = (295, 125)
        gameDisplay.blit(name_surf, name_rect)

        poops_surf, poops_rect = text_objects("poops", font)
        poops_rect.center = (535, 125)
        gameDisplay.blit(poops_surf, poops_rect)

        title_surf, title_rect = text_objects("SOOPER POOPERS", font)
        title_rect.center = (display_width / 2, 75)
        gameDisplay.blit(title_surf, title_rect)

        if not inits_2b_saved:
            back = button(display_width / 2 - 75, display_height * .88, 'back')

            if back:
                best = False

        pygame.display.update()
        clock.tick(15)
    intro_screen()


def intro_screen(first_time=True, poop_count=0, most_poops=0, x=-100, y=-100, facing_right=True):
    """Handle formatting and logic for intro_screen."""
    intro = True
    right_cow_x = display_width * 0.75
    exiting = False
    poo_trail = []

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(grass)
        large_text = pygame.font.Font('freesansbold.ttf', 90)
        text_surf, text_rect = text_objects("poopie cow", large_text)
        text_rect.center = ((display_width / 2), (display_height / 5))
        gameDisplay.blit(text_surf, text_rect)

        # if not coming from a played game display the two cows
        if first_time:
            cow(display_width / 4 + 5, display_height / 2, True)
            if not exiting:
                cow(right_cow_x, display_height / 2, False)
            else:
                cow(right_cow_x, display_height / 2, True)
        else:  # display cow at game co-ords as well and scores
            cow(x, y, facing_right)
            score(poop_count)
            best_score(most_poops)

        start = button(display_width / 2 - 75, 200, 'poop')
        if start:
            print("Poop!!!")
            intro = False
            option = 'start'

        about = button(display_width / 2 - 75, 275, 'about')
        if about:
            print("I'm udderly outta here!")
            option = "about"
            intro = False

        best = button(display_width / 2 - 75, 350, 'best poops')
        if best:
            print("Best poop!!!")
            option = 'best'
            intro = False

        exit = button(display_width / 2 - 75, 425, 'exit')
        if exit:
            print("I'm udderly outta here!")
            exiting = True
            option = 'exit'

        if exiting:
            if first_time is True:
                right_cow_x += 5
                moo(right_cow_x, display_height / 2)
                if len(poo_trail) == 1:
                    pygame.mixer.music.play()
                poo_trail.append((right_cow_x, display_height / 2))
                for poop in poo_trail:
                    poo(poop[0], poop[1], brown)
                if right_cow_x > display_width + 10:
                    exiting = False
                    print("Exited.")
                    # return "exit"
                    option = 'exit'
                    intro = False
            else:
                if x > display_width / 2:
                    facing_right = True
                    x += 5

                else:
                    facing_right = False
                    x -= 5

                poo_trail.append((x, y))
                for poop in poo_trail:
                    poo(poop[0], poop[1], brown)
                if x < -10 or x > display_width + 10:
                    exiting = False
                    print("Exited!")
                    # pygame.quit()
                    # quit()
                    option = 'exit'
                    intro = False

        pygame.display.update()
        clock.tick(15)
    if option == "start":
        option == ''
        game_loop()
    elif option == "about":
        about_screen()
    elif option == 'best':
        best_screen()
    elif option == "exit":
        intro = False
        pygame.quit()
    else:
        print("Shouldn't be here.")


def button(x, y, text, button_width=150, button_height=50):
    """Format and draw button."""
    clicked = False
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # check if mouse is over button
    if (x < mouse[0] < x + button_width) and (y < mouse[1] < y + button_height):
        button_colour = button_hover
        if click[0] == 1:
            clicked = True

    else:
        button_colour = button_grey
    pygame.draw.rect(gameDisplay, white, (x - 2, y - 2, button_width + 4, button_height + 4))
    pygame.draw.rect(gameDisplay, button_colour, (x, y, button_width, button_height))

    button_font = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(text, button_font)
    textRect.center = (x + (button_width / 2), y + (button_height / 2))
    gameDisplay.blit(textSurf, textRect)
    return clicked


def button2(x, y, radius=50):
    """Draw circular button."""
    clicked = False
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if (mouse[0] - x)**2 < radius**2 and (mouse[1] - y)**2 < radius**2:
        button_colour = (175, 0, 0)
        if click[0] == 1:
            clicked = True
    else:
        button_colour = (220, 0, 0)
    pygame.draw.circle(gameDisplay, white, (x, y), radius + 4)
    pygame.draw.circle(gameDisplay, button_colour, (x, y), radius)
    return clicked


def game_loop():
    """Handle all game play."""
    # start position, ensure evenly divisible by 5
    x = int(display_width / 4)
    y = int(display_height / 2)

    # don't change this, collision array uses numbers div by 5
    move_delta = 5

    # start movement direction
    x_change = 5
    y_change = 0

    # frame rate and game speed
    game_speed = 60

    # how long a moo stays on the screen
    moo_time = 61

    poo_trail = []
    poop_count = 0
    poo_length = 150
    max_poo_length = 2000

    facing_right = True

    # display instructions if starting game
    game_init = True

    game_exit = False

    most_poops = 0

    while not game_exit:

        poopy_foot = False  # Not sure about this

        # mooving_up = False
        # mooving_down = False

        at_screen_edge = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            # deal with keypresses
            if event.type == pygame.KEYDOWN:

                # exit game
                if event.key == pygame.K_SPACE:
                    # check for new high score
                    best_scores = get_best_scores()
                    if most_poops > best_scores[4][3]:
                        better_than = 0
                        for bs in best_scores:
                            if most_poops > bs[3]:
                                better_than += 1
                        # construct new best scores array
                        fb = best_scores[:-better_than]
                        mb = [[0, 0, 0, most_poops]]
                        lb = best_scores[-better_than:]
                        best_scores = fb + mb + lb
                        best_scores.pop(5)
                        with open('pickled_scores', 'wb') as pt:
                            pickle.dump(best_scores, pt, protocol=2)
                        # so, we've got a new high score, let's go there
                        best_screen(better_than)
                    intro_screen(False, poop_count, most_poops, x, y, facing_right)

                # moo test
                if event.key == pygame.K_m:
                    print(event)
                    moo_time = 0
                    # moo(x,y)

                # horizontal
                if event.key == pygame.K_LEFT:
                    x_change = -1 * move_delta
                    facing_right = False
                    # kill vertical delta
                    y_change = 0

                elif event.key == pygame.K_RIGHT:
                    facing_right = True
                    x_change = move_delta
                    # kill vertical
                    y_change = 0

                # vertical
                if event.key == pygame.K_UP:
                    y_change = -1 * move_delta
                    # mooving_up = True
                    # kill horizontal
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = move_delta
                    # mooving_down = True
                    # kill horizontal
                    x_change = 0

            ''' This section not needed for constant movement
            # deal with keyrelease (no longer held down)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
            '''

        # Code below works nicely if wall acts as barrier
        # Would be good for fencing too.
        '''
        # change (x,y) and make sure cow doesn't leave field (set boundary)
        x = max(cow_width,x + x_change)
        x = min(x,display_width - cow_width)
        # y += y_change
        y = max(0,y + y_change)
        y = min(y, display_height - cow_height)
        '''
        # move cow w/o walls/borders/fences
        x += x_change
        y += y_change

        # check for overlap on left/right
        if x < cow_width and not facing_right:
            at_screen_edge = True
            cow2x = x + display_width
        elif x + cow_width > display_width and facing_right:
            # check for overlap on right
            at_screen_edge = True
            cow2x = -1 * display_width + x
        else:
            cow2x = x

        # check for overlap top/bottom
        if y < cow_height:
            at_screen_edge = True
            cow2y = y + display_height
        elif y + cow_height > display_height:
            at_screen_edge = True
            cow2y = -1 * display_height + y
        else:
            cow2y = y

        gameDisplay.fill(grass)

        q_to_quit()  # display space to quit message

        if (x, y) in poo_trail:
            poopy_foot = True
        poo_trail.append((int(x), int(y)))
        poop_count += 1

        # truncate poo_trail
        if len(poo_trail) > poo_length:
            poo_trail = poo_trail[-poo_length:]
        for poop in poo_trail:
            poo(poop[0], poop[1], brown)
        # test
        # print(poo_trail)
        if moo_time < 60:
            moo(x, y)
            if moo_time == 1:
                pygame.mixer.music.play()
        moo_time += 1
        cow(x, y, facing_right)

        # if at screen edge draw second cow
        if at_screen_edge:
            cow(cow2x, cow2y, facing_right)
            if x < 0 or x > display_width:
                x = cow2x
            if y < 0 or y > display_height - cow_height:
                y = cow2y

        # check for overlap with poo_trail
        cow_edges = cow_bounds(x, y, facing_right)
        for edge in cow_edges:
            if edge in poo_trail:
                poopy_foot = True  # or break

        if poopy_foot:
            moo(x, y)
            if poop_count > most_poops:
                most_poops = poop_count
            poop_count = 0
            poo_length = 150
            moo_time = 0
            game_speed = 60

        score(poop_count)
        best_score(most_poops)
        # increase length of poo_trail
        if poop_count > 300:
            poo_length = min(int(poop_count * .5), max_poo_length)
            # increase game speed
            game_speed = 60 + int(poop_count / 15)

        # display instructions if game is beginning
        if game_init:
            show_instructions()

        pygame.display.update()

        if game_init:
            # show instructions for three seconds
            time.sleep(2.2)
            game_init = False  # don't do this again

        clock.tick(game_speed)

intro_screen()

pygame.quit()
# quit()
