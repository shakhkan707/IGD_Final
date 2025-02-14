# -*- coding: utf-8 -*-
from pygame import Rect
from pygame.sprite import Sprite

from singleton import Singleton
import settings as config



class Camera(Singleton):
	# constructor called on new instance: Camera()
	def __init__(self, lerp=5,width=config.XWIN, height=config.YWIN):
		self.state = Rect(0, 0, width, height)
		self.lerp = lerp
		self.center = height//2
		self.maxheight = self.center

	def reset(self) -> None:
		" Called only when game restarts (after player death)."
		self.state.y = 0
		self.maxheight = self.center
	
	def apply_rect(self,rect:Rect) -> Rect:

		return rect.move((0,-self.state.topleft[1]))
	
	def apply(self, target:Sprite) -> Rect:
		return self.apply_rect(target.rect)
	
	def update(self, target:Rect) -> None:
		# updating maxheight
		if(target.y<self.maxheight):
			self.lastheight = self.maxheight
			self.maxheight = target.y
		# calculate scrolling speed required
		speed = ((self.state.y+self.center)-self.maxheight)/self.lerp
		self.state.y-=speed

