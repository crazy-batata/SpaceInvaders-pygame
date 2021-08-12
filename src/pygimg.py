import pygame

def scale(img,x):
	return(pygame.transform.scale(img,
								 (img.get_rect().w * x, 
								  img.get_rect().h * x)))
def split_sheet(sheet,rect):
	surf =  pygame.Surface(rect.size).convert_alpha()
	surf.blit(sheet,(0,0),rect)
	return surf