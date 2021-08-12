import pygame

class Bullet(pygame.sprite.Sprite):
	def __init__(self,image,pos,speed,shouldDei):
		super().__init__()
		
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.midbottom = pos
		self.speed = speed
		self.shouldDei = shouldDei

	
	def update(self,dt):
		self.rect.move_ip(0,-self.speed * dt)
		if self.shouldDei(self.rect.y): self.kill()
	def destroy(self):
		self.kill()

