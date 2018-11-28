#The game is going to be like Smash Bros, with two players that can move around obstacles and when one player “hits” the other, they gain points.

import pygame
import gamebox
camera = gamebox.Camera(800, 600)

#This is the title page
to_draw = []
player_1 = []
player_2 = []
game_state = -1


def draw_title():
    instructions = ['''
    Welcome to PUSHTOWN!!!\n Stay in bounds, or die.\n  Push other players offscreen, move to stay within the scrolling screen and eat apples to make your pushes stronger.
    Whoever has the least deaths when time is up wins.
    ''',
    "Player 1: \nPress 'w' to jump. \nPress 'a' to move left. \nPress 'd' to move right. \nPress 's' to push.",
    "Player 2: \nPress the up arrow key to jump. \nPress the left arrow key to move left. \nPress the right arrow key to move right. \nPress the down arrow key to push.",
    "Press space to start."]

    text_height = 100
    player_title_height = 0
    for item in instructions[0].split("\n"):
        title_box = gamebox.from_text(400, text_height, item, 20, "white")
        to_draw.append(title_box)
        text_height += 25
    for item1 in instructions[1].split("\n"):
        title_1 = gamebox.from_text(200, text_height, item1, 20, "white")
        to_draw.append(title_1)
        text_height += 25
        player_title_height += 25

    text_height -= player_title_height
    for item2 in instructions[2].split("\n"):
        title_2 = gamebox.from_text(600, text_height, item2, 20, "white")
        to_draw.append(title_2)
        text_height += 25

    to_draw.append(gamebox.from_text(400, text_height+25, instructions[3], 40, "white"))



#drawing the instructions

#These are the things we need to draw for the game
# p1 = gamebox.
# p2 = gamebox.
def regular_gameplay():

    background = gamebox.from_color(400, 300, 'green', 800, 600)
def draw_game(keys):
    to_draw = []
    to_draw.append(background)


#This is how the characters will move
def tick(keys):
    global game_state
    camera.clear("black")
    if game_state == -1:
        draw_title()
        if pygame.K_SPACE in keys:
            game_state = 0

    if game_state >= 0:

        regular_gameplay()

    game_state += 1
    for box in to_draw:
        camera.draw(box)
    camera.display()
    # if pygame.K_RIGHT in keys:
    #     p2.x += 5
    # if pygame.K_LEFT in keys:
    #     p2.x -= 5
    # if pygame.K_UP in keys:
    #     p2.y -= 5
    # if pygame.K_DOWN in keys:
    #     p2.y #attack
    # if pygame.K_d in keys:
    #     p1.x += 5
    # if pygame.K_a in keys:
    #     p1.x -= 5
    # if pygame.K_w in keys:
    #     p1.y -= 5
    # if pygame.K_s in keys:
    #     p1.y #attack



gamebox.timer_loop(60, tick)

'''      
Optional features:
1. 2 players simultaneously
2. respawn to middle of screen when character gets pushed off screen
3. Scrolling level
4. Animation
5. timer/death count
6. Collectibles to make character stronger
'''