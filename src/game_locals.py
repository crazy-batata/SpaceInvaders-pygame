import pygame
from pygimg import *
import os.path

GAME_SETTING = [
	{
		"player_speed":0.2,
		"player_bullet_speed":0.2,
		"enmy_speed":1/60,
		"enmy_bullet_speed":0.25,
	},
	{
		"player_speed":0.25,
		"player_bullet_speed":0.25,
		"enmy_speed":1/50,
		"enmy_bullet_speed":0.3,
	},
	{
		"player_speed":0.3,
		"player_bullet_speed":0.3,
		"enmy_speed":1/35,
		"enmy_bullet_speed":0.4,
	},		

]
display_size = (855,450)
green_color = (101, 255, 26, 255)
 
global screen
def setScreen(_screen):	global screen;	screen = _screen
def getScreen(): return screen

global clock
def setClock(_clock): global clock; clock = _clock
def getClock():  return clock

global curr_state
curr_state = "main_menu"
def setCurrState(state): global curr_state; curr_state = state
def getCurrState():return curr_state 

global game_score
game_score = 0
def setGameScore(score): global game_score; game_score = score
def getGameScore(): return game_score

global height_score

def loadHeightScore():
	global height_score
	height_score = 0

	if os.path.isfile("score.txt"): 
		data = ""
		with open("score.txt","r") as f: data = f.read()
		try:
			if data: height_score = int(data)
		except:
			pass
	else:
		with open("score.txt","w") as f: pass

	
def saveHeightScore():
	with open("score.txt","w") as f:
		f.write(str(game_score))
def getHeightScore(): return height_score


global game_difficulty
game_difficulty = 0
def setGameDifficulty(difficulty): global game_difficulty; game_difficulty = difficulty
def getGameDifficulty(): return game_difficulty

global sprite_sheet
def loadSpriteSheet(): global sprite_sheet;	sprite_sheet = pygame.image.load("assest/sprite_sheet.png").convert_alpha()
def getSpriteSheet(): return sprite_sheet 



global enmy_sprits
def loadEnmySprits():
	global enmy_sprits
	enmy_11 = split_sheet(sprite_sheet,pygame.Rect(0,0,11,8))
	enmy_12 = split_sheet(sprite_sheet,pygame.Rect(16,0,11,9))

	enmy_21 = split_sheet(sprite_sheet,pygame.Rect(0,10,8,8 ))
	enmy_22 = split_sheet(sprite_sheet,pygame.Rect(16,10,8,8))

	enmy_31 = split_sheet(sprite_sheet,pygame.Rect(0,19,9,8))
	enmy_32 = split_sheet(sprite_sheet,pygame.Rect(16,19,9,8))

	enmy_sprits = [[enmy_31,enmy_32],
				  [enmy_21,enmy_22],
			 	  
			 	  [enmy_11,enmy_12]]		 
def getEnmySprites(): return enmy_sprits


global sound
def loadSound():
	global sound

	shoot_sound = pygame.mixer.Sound("assest/sound/shoot.wav")
	shoot_sound.set_volume(0.3)
	player_dead = pygame.mixer.Sound("assest/sound/player_dead.wav")
	player_hit = pygame.mixer.Sound("assest/sound/player_hit.wav")
	bullet_hit = pygame.mixer.Sound("assest/sound/bullet_hit.wav")

	sound = {
		"shoot":shoot_sound,
		"bullet_hit":bullet_hit,
		"hit":player_hit,
		"dead":player_dead
	}
def getSound(value): return sound[value]

