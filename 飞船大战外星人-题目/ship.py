#飞船
import pygame
from settings import Settings
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, screen ,al_settings):
        """初始化飞船并设置其初始化"""
        super().__init__()
        self.screen = screen
        self.al_settings = al_settings
        #加载飞船图像并获取其外接矩形
        image = pygame.image.load('images/ship.jpg') #返回一个表示飞船的surface
        self.image = pygame.transform.scale(image,(40,40))
        self.rect = self.image.get_rect()   #get_rect() 获取相应的suiface的属性rect(矩形？)
        self.screen_rect = screen.get_rect()  #将表示屏幕的矩形存储在self.screen_rect中

        #将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx   #设置飞船x轴方向位于屏幕中间
        self.rect.bottom = self.screen_rect.bottom    #设置飞船y 轴位于屏幕底部

        self.center = float(self.rect.centerx) #在飞船的属性center中存储小数值
        #移动标志
        self.moving_right = False
        self.moving_left = False
    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:  #保证点击右箭头键和飞船未触及屏幕右边缘
            self.center +=self.al_settings.ship_speed_factor #1.5
        if self.moving_left and self.rect.left >0:
            self.center -=self.al_settings.ship_speed_factor  #两个if保证了如果玩家同时按下了左右键，将先增大飞船的rect.centerx的值，在降低这个值，即飞船的位置保持不变

        #根据self.center更新rect对象,self.rect.centerx 将只存储self.center的整数部分
        self.rect.centerx = self.center

    def ship_location(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)  #根据飞船图片和矩形位置，设置好位置点，在屏幕上通过blit方法绘制出来

    def center_ship(self):
        """让飞船在屏幕中居中"""
        self.center = self.screen_rect.centerx