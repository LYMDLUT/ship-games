import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):    #Sprite为了统一处理一系列显示对象 子弹
    """一个对飞船发射的子弹进行管理的类"""

    def __init__(self,al_settings,screen,ship):
        """在飞船所处的位置创建一个子弹对象"""
        super().__init__()  #调用父类Sprite的__init__函数.
        self.screen = screen

        #在（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0,0,al_settings.bullet_width,al_settings.bullet_height)  #由于子弹不是图像，所以我们必须使用pygame.Rect()类从空白开始创建一个矩形
        self.rect.centerx = ship.rect.centerx  #将子弹的centerx设置为飞船的rect.centerx
        self.rect.top = ship.rect.top   #将子弹的top设置为飞船的top

        #c存储用小数点表示子弹位置
        self.y = float(self.rect.y)

        self.color = al_settings.bullet_color
        self.speed_factor = al_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        #更新表示子弹位置的小数值
        self.y -= self.speed_factor   #子弹发射出去后，子弹在屏幕中向上移动，意味着y坐标将不断减小，因此为更新子弹的位置
        #更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)