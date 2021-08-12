import pygame
from random import randint
from pygimg import *
from game_locals import *
class Sheild(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		frame1 = scale(split_sheet(getSpriteSheet(),pygame.Rect(27,0,26,12)),4)
		frame2 = scale(split_sheet(getSpriteSheet(),pygame.Rect(27,13,26,12)),4)
		frame3 = scale(split_sheet(getSpriteSheet(),pygame.Rect(27,26,26,8)),4)
		
		hidden_frame = pygame.Surface((0,0))
		hidden_frame.fill((0,0,0))
		hidden_frame.set_colorkey((0,0,0))

		self.frames = [frame1,frame2,frame3,hidden_frame]
		self.frame_index = 0

		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect()
		self.start_pos = pos
		self.rect.bottomleft = self.start_pos
		self.isDestroyed = False

	def update(self,screen):
		if self.image != self.frames[self.frame_index]:
			self.image = self.frames[self.frame_index]
			self.rect = self.image.get_rect()
			self.rect.bottomleft = self.start_pos
			if self.frame_index == 3: self.isDestroyed = True
			else: self.isDestroyed = False

	def damage(self):
		self.frame_index += 1
		self.frame_index = min(self.frame_index,3)
		getSound("bullet_hit").play()

