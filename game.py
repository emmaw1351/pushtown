#The game is going to be like Smash Bros, with two players that can move around obstacles and when one player “hits” the other, they gain points.

import pygame
import gamebox
camera = gamebox.Camera(800, 600)

#This is the title page
game_on = False
instructions = '''
Welcome to PUSHTOWN!!! Stay in bounds, or die.  Push other players offscreen, move to stay within the scrolling screen and eat apples to make your pushes stronger.
Whoever has the least deaths when time is up wins.

Player 1: Press 'w' to jump. Press 'a' to move left. Press 'd' to move right. Press 's' to push.  
Player 2: Press the up arrow key to jump. Press the left arrow key to move left. Press the right arrow key to move right. Press the down arrow key to push.
'''
def draw_title(keys):
	global game_on
	if keys:
		game_on = True
	keys.clear()
	to_draw = []
	ittle_box = gamebox.from_text(x, y, ‘Game Title’, ‘color’, True)
	to_draw.append(title_box)
#drawing the instructions
for line in instructions.split(‘\n’):
	to_draw.append(gamebox.from_text(x, y, line, size, ‘color’)


#These are the things we need to draw for the game
p1 = gamebox.
p2 = gamebox.

#This is how the characters will move
def tick(keys):
    if pygame.K_RIGHT in keys:
        p2.x += 5
    if pygame.K_LEFT in keys:
        p2.x -= 5
    if pygame.K_UP in keys:
        p2.y -= 5
    if pygame.K_DOWN in keys:
        p2.y #attack
    if pygame.K_d in keys:
        p1.x += 5
    if pygame.K_a in keys:
        p1.x -= 5
    if pygame.K_w in keys:
        p1.y -= 5
    if pygame.K_s in keys:
        p1.y #attack

'''      
Optional features:
1. 2 players simultaneously
2. respawn to middle of screen when character gets pushed off screen
3. Scrolling level
4. Animation
5. timer/death count
6. Collectibles to make character stronger
'''