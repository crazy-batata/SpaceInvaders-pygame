import pygame
from math import floor
from pygimg import *
from game_locals import *

from random import randint
from bullet import Bullet
from game_locals import GAME_SETTING 


class Enmy(pygame.sprite.Sprite):
	def __init__(self,frames,pos,enmy_type,game_difficulty):
		super().__init__()
		self.frames = []
		for i in frames:
			self.frames.append(scale(i,4))
			
		self.frame_index = 0
		
		self.destroy_frame = scale(split_sheet(getSpriteSheet(),pygame.Rect(0,27,13,9)),4) 
		self.isDestroyed = False
		self.destroy_delay = 0.2
		self.destroy_counter = 0

		self.image = self.frames[0]
		self.rect = pygame.Rect(pos[0],pos[1],self.image.get_rect().w,self.image.get_rect().h)
		self.pos = pos

		self.shouldMove = False

		self.bullet  = None
		self.bullet_sprite = scale(split_sheet(getSpriteSheet(),pygame.Rect(20,27,3,7)),4) 
		self.shouldShoot = False

		self.type = enmy_type
		self.isDestroyed = False


		self.speed = GAME_SETTING[floor(getGameDifficulty())]["enmy_speed"]
		self.bullet_speed = -1 * GAME_SETTING[floor(getGameDifficulty())]["enmy_bullet_speed"]

	def update(self,dt,enmy_count,shouldRest,enmy_bullet_group):
		if shouldRest: self.rect.topleft = (self.pos[0],self.rect.y + 32)

		self.animate()

		if self.shouldMove and self.shouldShoot:
			self.shouldShoot = False
			self.shoot(enmy_count,enmy_bullet_group)
		if self.isDestroyed:
			self.destroy(dt)

	def animate(self):
		if self.frame_index >= 2 : self.frame_index = 0
		self.image = self.frames[floor(self.frame_index)]
		self.frame_index += self.speed

		if int(self.frame_index) == 1 and not self.shouldMove:
			self.shouldMove = True
			self.shouldShoot = True
			self.rect.move_ip(44,0)

		if int(self.frame_index) == 0:
			self.shouldMove = False
			
	def shoot(self,enmy_count,enmy_bullet_group):
		readyToShoot = randint(1,2 * getGameDifficulty() + enmy_count ) 
		if  readyToShoot == 1 or readyToShoot == 4:
			self.bullet = Bullet(self.bullet_sprite,
								 self.rect.midbottom,
								 self.bullet_speed,
								 lambda y: y > 400)
			enmy_bullet_group.add(self.bullet)

	def destroy(self,dt):
		self.isDestroyed = True
		if self.destroy_counter > self.destroy_delay:
			self.kill()
		self.image = self.destroy_frame
		self.destroy_counter += dt / 1000
		
		