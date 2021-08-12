import pygame
from pygimg import *
from game_locals import *
from bullet import Bullet
from game_locals import GAME_SETTING , green_color
import math

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = scale(split_sheet(getSpriteSheet(),pygame.Rect(0,36,15,8)),4)
		self.image.fill(green_color,special_flags=pygame.BLEND_MULT)
		self.gotHit = False
		self.invisibility_count = 0
		self.invisibility_delay = 1.4
		self.isInvisible = True
		self.invisibility_frames = ["#64fe19","Black"]
		self.invisibility_index = 0
		
		print(self.image.get_at((2,1)))		
 
		self.start_pos = 400,380
		self.rect = self.image.get_rect()
		self.rect.center = self.start_pos

		self.bullet_group = pygame.sprite.GroupSingle()
		self.bullet = None
		self.bullet_sprite = scale(split_sheet(getSpriteSheet(),pygame.Rect(17,27,1,6)),4)

		self.hitpoints = 99

		# setting
		self.setGameDifficulty(getGameDifficulty())

 

	def update(self,dt):
		self.inputHandler(dt)
		self.boundary()

		if self.bullet:
			if not self.bullet.alive():
				self.bullet = None

		if self.isInvisible:
			if self.gotHit:
				self.gotHit = False
				self.invisibility_index = 0
			self.invisibileEffect(dt)
		if self.hitpoints > 3:
			self.hitpoints = 3


	def setGameDifficulty(self,gd):
		self.speed = GAME_SETTING[gd]["player_speed"]
		self.bullet_speed = GAME_SETTING[gd]["player_bullet_speed"]

	def inputHandler(self,dt):
		keys = pygame.key.get_pressed()

		if   ( keys[pygame.K_LEFT] or keys[pygame.K_a] ) : self.rect.move_ip(-self.speed * dt,0) 
		elif ( keys[pygame.K_RIGHT] or keys[pygame.K_d] ): self.rect.move_ip(self.speed * dt,0)

		if keys[pygame.K_SPACE] and not self.bullet: 
			self.bullet = Bullet(self.bullet_sprite,
								 self.rect.midtop,
								 self.bullet_speed,
								 lambda y : y < 0)
			self.bullet_group.add(self.bullet) 
			getSound("shoot").play()
	
	def boundary(self):
		if self.rect.x < 0: self.rect.x = 0
		elif self.rect.x > (getScreen().get_rect().w - self.rect.w ): self.rect.x = (getScreen().get_rect().w - self.rect.w )

	def takeDamage(self,damage=1):
		if self.hitpoints > 0 and not self.isInvisible: 
			self.hitpoints -= damage
			self.gotHit = True
			getSound("hit").play()

		if self.hitpoints <= 0:
			setCurrState("game_over")	
			getSound("dead").play()

	def invisibileEffect(self,dt):
		self.invisibility_index += 0.035
		if math.floor(self.invisibility_index) >= 2: self.invisibility_index = 0

		if self.invisibility_count > self.invisibility_delay:
			self.isInvisible = False
			self.invisibility_count = 0
			self.invisibility_index = 1

		self.image.set_colorkey(self.invisibility_frames[math.floor(self.invisibility_index)])
		self.invisibility_count += dt / 1000



