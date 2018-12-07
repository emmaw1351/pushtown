
import pygame
import gamebox
import random
import urllib

camera_width = 800
camera_height = 600
camera = gamebox.Camera(camera_width, camera_height)

#This is the title page
to_draw = []
image1 = gamebox.load_sprite_sheet('blue_noback.png', 1, 2)
p1 = gamebox.from_image(400, 300, image1[0])


image2 = gamebox.load_sprite_sheet('red_noback.png', 1, 2)
p2 = gamebox.from_image(400, 300, image2[0])



# p1 = gamebox.from_color(300, 300, "red", 15, 15)
# p2 = gamebox.from_color(500, 300, "blue", 15, 15)
p1.yspeed = p2.yspeed = p1.xspeed = p2.xspeed = p1_score = p2_score = 0
p1_strength = p2_strength = 4
apples = [gamebox.from_color(400, 385, "orange", 10, 10)]
platforms = [gamebox.from_color(400, 400, "white", 300, 15), gamebox.from_color(200, 300, "white", 300, 15), gamebox.from_color(600, 300, "white", 300, 15),
gamebox.from_color(200, 500, "white", 300, 15), gamebox.from_color(600, 500, "white", 300, 15), gamebox.from_color(400, 200, "white", 300, 15)]

player_data = [[p1, p1_strength, p1_score], [p2, p2_strength, p2_score]]

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
        title_1 = gamebox.from_text(200, text_height, item1, 20, "red")
        to_draw.append(title_1)
        text_height += 25
        player_title_height += 25

    text_height -= player_title_height
    for item2 in instructions[2].split("\n"):
        title_2 = gamebox.from_text(600, text_height, item2, 20, "blue")
        to_draw.append(title_2)
        text_height += 25

    to_draw.append(gamebox.from_text(400, text_height+25, instructions[3], 40, "white"))


def regular_gameplay(keys, gravity=.13):
    global game_state
    to_draw.clear()

    for player in player_data:

        # this friction still isn't working correctly :/
        for apple in apples:
            if player[0].touches(apple):
                player[1] += 1
                apples.remove(apple)
            camera.draw(apple)

        player[0].yspeed += gravity

        if player[0].yspeed != 0:
            for platform in platforms:
                if player[0].bottom_touches(platform):
                    player[0].yspeed = 0
                    player[0].move_to_stop_overlapping(platform)
                if player[0].top_touches(platform):
                    player[0].move_to_stop_overlapping(platform)
                    player[0].yspeed += .13
        if player[0].xspeed != 0:

            if player[0].xspeed > 0:
                player[0].xspeed -= player[0].xspeed/10

            if player[0].xspeed < 0:
                 player[0].xspeed += -player[0].xspeed/10


    if p1.touches(p2):
        p1.move_both_to_stop_overlapping(p2)
    if pygame.K_RIGHT in keys:
        p2.x += 3
    if pygame.K_LEFT in keys:
        p2.x -= 3
    if pygame.K_UP in keys and (p2.yspeed == 0 or p2.bottom_touches(p1)):
        p2.yspeed -= 6
    if pygame.K_DOWN in keys:
        if p2.left_touches(p1):
            p1.xspeed -= player_data[1][1]
        if p2.right_touches(p1):
            p1.xspeed += player_data[1][1]

    if pygame.K_d in keys:
        p1.x += 3
    if pygame.K_a in keys:
        p1.x -= 3
    if pygame.K_w in keys and (p1.yspeed == 0 or p1.bottom_touches(p2)):
        p1.yspeed -= 6
    if pygame.K_s in keys:
        if p1.left_touches(p2):
            p2.xspeed -= player_data[0][1]
        if p1.right_touches(p2):
            p2.xspeed += player_data[0][1]

    for player in player_data:
        player[0].y += player[0].yspeed
        player[0].x += player[0].xspeed

    if game_state % 60 == 0:
        apple_x = camera.x + random.randint(-400, 400)
        apple_y = camera.y + random.randint(-300, 300)

        for platform in platforms:
            if platform.x - 5 < apple_x < platform.x + 5:
                apple_x += 20
            if platform.y -5 < apple_y < platform.y - 5:
                apple_y += 20

        apples.append(gamebox.from_color(apple_x, apple_y, "orange", 10, 10))
    tick_count = 0
    p1.image = image1[tick_count // 2 % len(image1)]
    p2.image = image2[tick_count // 2 % len(image2)]
    tick_count += 1
    to_draw.append(p1)
    to_draw.append(p2)

def camera_movement(time):

    period = time/4

    if game_state < period:
        camera.y -= camera_height/period

    elif game_state < period*2:
        camera.x += camera_width/period

    elif game_state < period*3:
        camera.y += camera_height/period

    elif game_state < period*4:
        camera.x -= camera_width/period

def tick(keys, seconds=30):

    global game_state
    duration = seconds * ticks_per_second
    camera.clear("black")
    if game_state == -1:
        draw_title()
        if pygame.K_SPACE in keys:
            game_state = 0

    if game_state >= 0:

        regular_gameplay(keys)
        game_state += 1
        score_and_timer(player_data[0][2], player_data[1][2], (duration - game_state) // 60)
        if camera.x - 400 > p2.x or p2.x > camera.x + 400 or  camera.y - 300 > p2.y or p2.y > camera.y + 300:
            p2.x = camera.x
            p2.y = camera.y
            p2.yspeed = p2.xspeed = 0
            player_data[0][2] += 1

        if camera.x - 400 > p1.x or p1.x > camera.x + 400 or camera.y - 300 > p1.y or p1.y > camera.y + 300:
            p1.x = camera.x
            p1.y = camera.y
            p1.yspeed = p1.xspeed = 0
            player_data[1][2] += 1

        for platform in platforms:
            camera.draw(platform)

        """if game_state == seconds * 60:
            game_state = -2
            to_draw.clear()"""

        camera_movement(duration)

    if game_state == -2:

        if player_data[0][2] == player_data[1][2]:

            winner = "It's a tie!"
            color = "white"

        else:
            if player_data[0][2] > player_data[1][2]:
                winner = "Player 1 wins!"
                color = "red"

            else:
                color = "blue"
                winner = "Player 2 wins!"

        win_statement = gamebox.from_text(400, 300, winner, 50, color)

        to_draw.append(win_statement)



    for box in to_draw:
        camera.draw(box)

    camera.display()


def score_and_timer(death_count_2, death_count_1, time):

    score1 = gamebox.from_text(camera.x - camera_width/4, camera.y - camera_height/3, "Death count: " + str(death_count_1), 20, "red")
    score2 = gamebox.from_text(camera.x + camera_width/4, camera.y - camera_height/3, "Death count: " + str(death_count_2), 20, "blue")
    timer = gamebox.from_text(camera.x, camera.y - camera_height/3, str(time), 20, "white")

    camera.draw(score1)
    camera.draw(score2)
    camera.draw(timer)

ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)



'''      
Optional features:
1. 2 players simultaneously| check!#############################
2. respawn to middle of screen when character gets pushed off screen| basic respawning is possible####################
3. Scrolling level
4. Animation
5. timer/death count| Basic time and death count has been implemented ###########################
6. Collectibles to make character stronger#############################
'''