import pygame
import os.path
from math import floor
from random import randint

from pygimg import * 
from game_locals import *


from player import Player
from enmy import Enmy
from sheild import Sheild
from ui import UI

def playerBulletCollition(collided):
	if not (collided and player.sprite.bullet): return
	if collided[0].isDestroyed: return 

	collided[0].destroy(dt)
	setGameScore(getGameScore() + collided[0].type * 10)
	player.sprite.bullet.kill()
	getSound("shoot").stop()
	getSound("bullet_hit").play()
def sheildCollistion(collided,obj_type):
	if not collided: return
	for sheild , objs in collided.items():
		if sheild.isDestroyed: continue
		for obj in objs:
			if obj_type == "enmy":
				if not obj.isDestroyed: 
					obj.destroy()
					sheild.damage()				
			elif obj_type == "enmy_bullet":  
				obj.kill()
				sheild.damage()
			elif obj_type == "player_bullet" and player.sprite.bullet:
				player.sprite.bullet.kill()
				sheild.damage()
				getSound("shoot").stop()
def playerCollision(collided,obj_type):
	if not collided: return
	if obj_type == "enmy":
		if not collided[0].isDestroyed: 
			collided[0].isDestroyed = True
			if not player.sprite.isInvisible:
				player.sprite.takeDamage()
				player.sprite.isInvisible = True
	elif obj_type == "enmy_bullet":
		collided[0].kill()
		if not player.sprite.isInvisible:
			player.sprite.takeDamage()
			player.sprite.isInvisible = True
			





def initEnmys():
	offset = 4   
	row_count = 8
	enmy_sprits = getEnmySprites()
	for y in range(len(enmy_sprits)):
		for x in range(row_count):
			enmy_group.add(Enmy( enmy_sprits[y]
								,( x * 48 + ((44 - enmy_sprits[y][0].get_rect().w) / 2) + x*offset,(32 + offset) * y)
								,3-y,floor(getGameDifficulty()))) 
def initSheilds():
	sheild_count = 3
	offset = 90
	sheild_x_dis = screen.get_rect().w / sheild_count
	for i in range(sheild_count):
		sheild_group.add(Sheild((sheild_x_dis * i + offset,screen.get_rect().h - 150)))
def initValues():
	global restart_game
	if not restart_game: return

	restart_game = False
	setGameScore(0)
	setGameDifficulty(0)
	player.sprite.hitpoints = 3
	if player.sprite.bullet: 
		player.sprite.bullet.kill()

	enmy_group.empty()
	initEnmys()
	sheild_group.empty()
	initSheilds()

	enmy_bullet_group.empty()
def init():
	pygame.init()
	pygame.font.init()
	pygame.mixer.init()


	setScreen(pygame.display.set_mode(display_size)) 
	setClock(pygame.time.Clock())
	
	loadHeightScore()	
	loadSpriteSheet()
	loadEnmySprits()
	loadSound()

	pygame.display.set_caption("kind of Space Invaders")

	random_icon = randint(0,len(getEnmySprites())-2)
	icon = getEnmySprites()[random_icon][randint(0,1)]
	icon.set_colorkey("Black")
	pygame.display.set_icon(icon)




init()
screen = getScreen()

max_difficulty = len(GAME_SETTING)

enmy_group = pygame.sprite.Group()
enmy_bullet_group = pygame.sprite.Group() 
sheild_group = pygame.sprite.Group()

player = pygame.sprite.GroupSingle(Player( )) 


game_ui = UI()




def updateGamePlayState():
	def upTheDifficulty():
		if len(enmy_group): return
		initEnmys()	

		setGameDifficulty(min(getGameDifficulty() + 0.5 , max_difficulty-1))
		print(floor(getGameDifficulty()))

		player.sprite.setGameDifficulty(floor(getGameDifficulty()))

		random_sheild = randint(0,len(sheild_group) - 1)
		if sheild_group.sprites()[random_sheild].frame_index > 0: sheild_group.sprites()[random_sheild].frame_index -= 1
	if getCurrState() != "game_play": return
	if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:	pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
	upTheDifficulty()

	######################## Enmy boundary #######################
	sprites = enmy_group.sprites() 
	shouldRest = False
	for sprite in sprites:
		if shouldRest: break 
		shouldRest = sprite.rect.topright[0] > screen.get_rect().w
		if sprite.rect.y > 400: 
			player.sprite.hitpoints = 0
			player.sprite.takeDamage()

	######################## Sheilds ###########################
	sheild_group.draw(screen)
	sheild_group.update(screen)

	######################## Enmy #############################
	enmy_bullet_group.update(dt)
	enmy_bullet_group.draw(screen)
	enmy_group.update(dt,len(enmy_group),shouldRest,enmy_bullet_group)
	enmy_group.draw(screen)

	######################## Player ###########################
	player.sprite.bullet_group.update(dt)
	player.sprite.bullet_group.draw(screen)
	player.update(dt) 
	player.draw(screen)
	
	######################### Collotion #########################
	if player.sprite.bullet: playerBulletCollition(pygame.sprite.spritecollide(player.sprite.bullet,enmy_group,False))
	playerCollision(pygame.sprite.spritecollide(player.sprite,enmy_bullet_group,False),"enmy_bullet")
	playerCollision(pygame.sprite.spritecollide(player.sprite,enmy_group,False),"enmy")
	sheildCollistion(pygame.sprite.groupcollide(sheild_group,enmy_bullet_group,False,False),"enmy_bullet") 
	sheildCollistion(pygame.sprite.groupcollide(sheild_group,player.sprite.bullet_group,False,False),"player_bullet") 
	sheildCollistion(pygame.sprite.groupcollide(sheild_group,enmy_group,False,False),"enmy")

global restart_game
restart_game = True

global isRunning
isRunning = True

def eventLoop():
	global isRunning
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
while isRunning:
	eventLoop()
	dt = getClock().tick(60)


	# whene statring new game
	initValues()
	# game play state
	updateGamePlayState()
	

			
	state_changed , prev_state = game_ui.update(player.sprite.hitpoints)
	if state_changed:
		if prev_state != "game_play" and getCurrState() == "game_play" and not restart_game:
			restart_game = True


	pygame.display.update()
	screen.fill((0,0,0))

pygame.font.quit()
pygame.quit()
