import pygame
import os.path
from pygimg import *
from game_locals import *
class UI():
	def __init__(self):
		self.line = { "rect": pygame.Rect(0,400,855,4) , "color": green_color }
		self.sprite = scale(split_sheet(getSpriteSheet(),pygame.Rect(0,36,15,8)),4)
		self.sprite.fill(green_color,special_flags=pygame.BLEND_MULT)
		self.font37 = pygame.font.Font("assest/fonts/unifont.ttf",37)
		self.font37.bold = True

		self.font54 = pygame.font.Font("assest/fonts/unifont.ttf",54)
		self.font54.bold = True
		self.title_surf = self.font54.render("SPACE INVADERS",False,"White") 

		_10points = self.font54.render("= 10 POINTS",False,"White")

		# _10points_sprite = split_sheet(getSpriteSheet(),pygame.Rect(0,0,11,8))
		_10points_sprite = getEnmySprites()[2][0]

		_20points = self.font54.render("= 20 POINTS",False,"White")
		#_20points_sprite = split_sheet(getSpriteSheet(),pygame.Rect(0,16,8,8))
		_20points_sprite = getEnmySprites()[1][0]


		_30points = self.font54.render("= 30 POINTS",False,"White")
		# _30points_sprite = split_sheet(getSpriteSheet(),pygame.Rect(0,32,9,8))
		_30points_sprite = getEnmySprites()[0][0]

		scale_v = 7
		self.pointUI = [(scale(_10points_sprite,scale_v),_10points),(scale(_20points_sprite,scale_v),_20points),(scale(_30points_sprite,scale_v),_30points)] 
		self.score_checked = False
		self.game_over_surf = self.font54.render("GAME OVER",False,"White")


		self.best_score = getHeightScore()
	
	def update(self,hitpoints = 0):
		if getCurrState() == "main_menu":
			return self.mainMenuUI()
		elif getCurrState() == "game_over":
			return self.gameOverUI()
		elif getCurrState() == "game_play":
			return self.gamePlayUI(hitpoints)

	def mainMenuUI(self):
		screen = getScreen()
		screen.blit(self.title_surf,((screen.get_rect().w - self.title_surf.get_rect().w) / 2,45))

		start_btn =  self.font54.render("CLICK HERE TO PLAY",False,"White").convert_alpha()

		start_btn_rect = start_btn.get_rect()
		start_btn_rect.topleft = ((screen.get_rect().w - start_btn.get_rect().w)/2,100)


		if start_btn_rect.collidepoint(pygame.mouse.get_pos()): 
			start_btn.fill(green_color,special_flags=pygame.BLEND_MULT)
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
			if pygame.mouse.get_pressed(num_buttons=3)[0]:
				setCurrState("game_play")
				return ( True , "main_menu" )
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

			
		screen.blit(start_btn,start_btn_rect.topleft)
			
		for i in range(len(self.pointUI)):
			screen.blit(self.pointUI[i][1],(300,200 + (54 + 10) * i))
			screen.blit(self.pointUI[i][0],(220 + (44 - self.pointUI[i][0].get_rect().w) / 2,210 + (54 + 10) * i))	


		# if not self.score_checked:
			# self.score_checked = True
		if self.best_score:
			best_score_surf = self.font37.render(f"BEST SCORE: {self.best_score}",False,"White").convert_alpha()
			screen.blit(best_score_surf,(300,400))
		return ( False , "" )	
	def gameOverUI(self):
		screen = getScreen()
		rect = pygame.Rect((screen.get_rect().w - 380) / 2,(screen.get_rect().h - 320) / 2,380,320)
		pygame.draw.rect(screen,"Black",rect)
		pygame.draw.rect(screen,green_color,rect,4)
		screen.blit(self.game_over_surf,(rect.x + ( rect.w - self.game_over_surf.get_rect().w) / 2 , rect.y + 50))

		play_again_surf = self.font37.render("PLAY AGAIN",False,"White").convert_alpha()
		play_again_rect = play_again_surf.get_rect()
		play_again_rect.topleft = (rect.x + ( rect.w - play_again_surf.get_rect().w) / 2 , rect.y + 150)
		if play_again_rect.collidepoint(pygame.mouse.get_pos()):
			play_again_surf.fill(green_color,special_flags=pygame.BLEND_MULT)
			if pygame.mouse.get_pressed(num_buttons = 3)[0] == True:
				setCurrState("game_play")
				return ( True , "game_over")			

		screen.blit(play_again_surf,play_again_rect.topleft)

		main_menu_surf = self.font37.render("MAIN MENU",False,"White").convert_alpha()
		main_menu_rect = main_menu_surf.get_rect()
		main_menu_rect.topleft = (rect.x + ( rect.w - main_menu_surf.get_rect().w) / 2 , rect.y + 200)
		if main_menu_rect.collidepoint(pygame.mouse.get_pos()):
			main_menu_surf.fill(green_color,special_flags=pygame.BLEND_MULT)
			if pygame.mouse.get_pressed(num_buttons = 3)[0] == True:
				setCurrState("main_menu")
				return ( True , "game_over")			
		screen.blit(main_menu_surf,main_menu_rect.topleft)

		score_surf = self.font37.render(f"SCORE: {getGameScore()}",False,"White").convert_alpha()
		screen.blit(score_surf,(rect.x + ( rect.w - self.game_over_surf.get_rect().w) / 2 , rect.y + 270))
		if getGameScore() > self.best_score:
			self.best_score = getGameScore()
			saveHeightScore()

		return ( False , "")
	def gamePlayUI(self,hitpoints):
		screen = getScreen()
		pygame.draw.rect(screen,self.line["color"],self.line["rect"])
		text_surf = self.font37.render(f"{hitpoints}",False,(green_color)).convert_alpha()
		screen.blit(text_surf,(10,408))
		for x in range(hitpoints):
			screen.blit(self.sprite,( 40 +  ( 10 + self.sprite.get_rect().w ) * x,410))
		
		score_surf = self.font37.render(str(getGameScore()),False,green_color).convert_alpha()
		screen.blit(score_surf,(screen.get_rect().w - score_surf.get_rect().w - 40,400))

		return ( False , "")