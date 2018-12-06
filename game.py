
import pygame
import gamebox
import random
import urllib

camera_width = 800
camera_height = 600
camera = gamebox.Camera(camera_width, camera_height)

#This is the title page
to_draw = []
'''image1 = gamebox.load_sprite_sheet('sprite_blue_walking.png', 1, 2)
p1 = gamebox.from_image(0, 0, image1[0])
#p1.right = camera.left
p1.y = 50


image2 = gamebox.load_sprite_sheet('sprite_walking_red.png', 1, 2)
p2 = gamebox.from_image(0, 0, image2[0])
#p2.right = camera.left
p2.y = 50'''

p1 = gamebox.from_color(300, 300, "red", 15, 15)
p2 = gamebox.from_color(500, 300, "blue", 15, 15)

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


def world_physics(player, gravity):
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
                player[0].yspeed += gravity
    if player[0].xspeed != 0:

        if player[0].xspeed > 0:
            player[0].xspeed -= player[0].xspeed / 10

        if player[0].xspeed < 0:
            player[0].xspeed += -player[0].xspeed / 10


def user_control(this_player, that_player, right, left, up, down, keys, jump_velocity):

    if getattr(pygame, right) in keys:
        this_player[0].x += 3
    if getattr(pygame, left) in keys:
        this_player[0].x -= 3
    if getattr(pygame, up) in keys and (this_player[0].yspeed == 0 or this_player[0].bottom_touches(that_player[0])):
        this_player[0].yspeed += jump_velocity
    if getattr(pygame, down) in keys:
        if this_player[0].left_touches(that_player[0]):
            that_player[0].xspeed -= this_player[1]
        if this_player[0].right_touches(that_player[0]):
            that_player[0] += this_player[1]

    this_player[0].y += this_player[0].yspeed
    this_player[0].x += this_player[0].xspeed


def add_apple():

        apple_x = camera.x + random.randint(-400, 400)
        apple_y = camera.y + random.randint(-300, 300)

        for platform in platforms:
            if platform.x - 5 < apple_x < platform.x + 5:
                apple_x += 20
            if platform.y - 5 < apple_y < platform.y - 5:
                apple_y += 20

        apples.append(gamebox.from_color(apple_x, apple_y, "orange", 10, 10))


def respawn(this_player, that_player):
    this_player[0].x = camera.x
    this_player[0].y = camera.y
    this_player[0].yspeed = this_player[0].xspeed = 0
    that_player[2] += 1

    print(0)


def remove_off_screen(this_object, removal_behavior):
    print(1)
    width = camera_width/2
    height = camera_height/2
    if camera.x - width > this_object.x or this_object.x > camera.x + width or camera.y - height > this_object.y or this_object.y > camera.y + height:
        removal_behavior()


def regular_gameplay(keys, gravity=.13, jump_velocity=-6):
    global game_state
    to_draw.clear()

    to_draw.append(p1)
    to_draw.append(p2)

    for player in player_data:

        world_physics(player, gravity)

    if p1.touches(p2):
        p1.move_both_to_stop_overlapping(p2)

    user_control(player_data[1], player_data[0], 'K_RIGHT', 'K_LEFT', 'K_UP', 'K_DOWN', keys, jump_velocity)
    user_control(player_data[0], player_data[1], 'K_d', 'K_a', 'K_w', 'K_d', keys, jump_velocity)

    if game_state % 60 == 0:

        add_apple()

    platform_create_destroy(jump_velocity, gravity)


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

        for apple in apples:
             remove_off_screen(apple, lambda: apples.remove(apple))

        for platform in platforms:
             remove_off_screen(platform, lambda: platforms.remove(platform))

        remove_off_screen(player_data[0][0], lambda: respawn(player_data[0], player_data[1]))

        remove_off_screen(player_data[1][0], lambda: respawn(player_data[1], player_data[0]))

        camera_movement(duration)
     # remember to uncomment this out

    """if game_state == duration
    game_state = -2
    to_draw.clear()"""


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


def platform_create_destroy(jump_velocity, gravity):

    ticks_to_ground = jump_velocity/gravity
    max_dist_y = 6*ticks_to_ground - (.13/2)*ticks_to_ground
    max_dist_x = 5 * ticks_to_ground

    for platform in platforms:
        camera.draw(platform)

    return max_dist_x, max_dist_y


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