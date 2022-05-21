import pygame
import os
import sys
import random
import math


pygame.init()


#### fps ####
clock = pygame.time.Clock()
fps = 60


#### screen ####
screen_X = 800
screen_Y = 600
screen = pygame.display.set_mode((screen_X, screen_Y))


#### background ####
background2 = pygame.image.load('bg.jpg')
background1 = pygame.transform.scale(background2, (screen_X, screen_Y))
def background():
	screen.blit(background1,(0, 0))

	
#### player ####
player_sizeX = 64
player_sizeY = 55
player_posX	= 370
player_posY = 480
player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img,(player_sizeX,player_sizeY))

def player_show(x, y):
	screen.blit(player_img, (x, y))


#### enemy ####
enemy_img = []
enemy_posX = []
enemy_posY = []
enemy_ran_move = []
enemy_sizeX = 55
enemy_sizeY = 50
move_left = -2
move_right = 2
move = (move_left, move_right)
enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (enemy_sizeX, enemy_sizeY))
for i in range(6):		
	enemy_posX.append(random.randint(0, screen_X - enemy_sizeX - 1))
	enemy_posY.append(random.randint(0, 150))	
	enemy_ran_move.append(random.choice(move))

def enemy_show(x, y):
	screen.blit(enemy_img,(x, y))


#### bullet ####
bullet_sizeX = 50
bullet_sizeY = 50
bullet_posX = player_posX
bullet_posY = player_posY
bullet_img = pygame.image.load('bullet.png') 
bullet_img = pygame.transform.scale(bullet_img, (bullet_sizeX, bullet_sizeY))
bullet_shoot = False
bullet_speed = 13

def bullet_show(x, y):
	screen.blit(bullet_img,(x + 12, y - 30))


#### collision enemy bullet ####
def collision(x1, x2, y1, y2):
	crash = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)) 	
	print(crash)
	if crash < 40:
		return True
	else:
		return False
		

#### score ####
scores = 0			
font = pygame.font.Font('freesansbold.ttf', 25)			
textX = 10
textY = 10

def show_score(x, y):	
	score = font.render(f'score : {scores}', True,(255,255,255))
	screen.blit(score, (x, y))


#### game over ####
game_over = pygame.font.Font('freesansbold.ttf', 50)
over_text = font.render('GAME OVER', True,(255,255,255))

def game_over_text():
	screen.blit(over_text, (300, 250))


#### sound ####
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)
bullet_sound = pygame.mixer.Sound('laser.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')


#### main loop  ####
running = True
start_game = True
while running:
	background()
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			if event.key == pygame.K_SPACE and bullet_shoot == False:				
				if start_game == False:
					start_game = True
					for i in range(6):
						enemy_posX[i] =  random.randint(0, screen_X - enemy_sizeX - 1)
						enemy_posY[i] = random.randint(0, 150)
					player_posX = 370
					player_posY = 480
					scores = 0
				else:	
					bullet_posX = player_posX
					bullet_shoot = True
					bullet_sound.play()
	
	player_show(player_posX, player_posY)				
	#### player move ####
	press = pygame.key.get_pressed()
	if press[pygame.K_LEFT] and player_posX >= 0:
		player_posX -= 5
	if press[pygame.K_RIGHT] and player_posX <= screen_X - player_sizeX:
		player_posX += 5
	if press[pygame.K_UP] and player_posY >= 0:
		player_posY -= 5
	if press[pygame.K_DOWN] and player_posY <= screen_Y - player_sizeY - 10:
		player_posY += 5


	#### enemy move ####
	if start_game == True:
		
		for i in range(6):
							
			if enemy_posY[i] > screen_Y - enemy_sizeY:
				for j in range(6):
					enemy_posY[j] = 2000				
					start_game = False					

			if enemy_posX[i] <= 0:
				enemy_ran_move[i] = move_right
				enemy_posY[i] += 40
			elif enemy_posX[i] >= screen_X - enemy_sizeX:
				enemy_ran_move[i] = move_left
				enemy_posY[i] += 40	
			enemy_posX[i] += enemy_ran_move[i]
			
			_collision_enemy_bullet = collision(enemy_posX[i], bullet_posX, enemy_posY[i], bullet_posY)	
			if _collision_enemy_bullet:
				explosion_sound.play()
				bullet_posY = player_posY
				bullet_shoot = False
				enemy_posX[i] =  random.randint(0, screen_X - enemy_sizeX - 1)
				enemy_posY[i] = random.randint(0, 150)
				scores += 1

			_collision_player_enemy = collision(enemy_posX[i], player_posX, enemy_posY[i], player_posY)	
			if _collision_player_enemy:
				explosion_sound.play()
				for j in range(6):
					enemy_posY[j] = 2000							
				
				start_game = False			
				
				
			enemy_show(enemy_posX[i], enemy_posY[i])	
	else:
		game_over_text()
		show_score(325, 280)


	#### player shoot ####\
	if bullet_posY <= 0:
		bullet_posY = player_posY
		bullet_shoot = False

	if bullet_shoot == True:
		bullet_posY -= bullet_speed
		bullet_show(bullet_posX, bullet_posY)	
	
	if start_game == True:
		show_score(textX, textY)
	clock.tick(fps)
	pygame.display.update()			
	
pygame.quit()
sys.exit()			