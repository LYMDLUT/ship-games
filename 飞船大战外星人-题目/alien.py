import pygame
from pygame.sprite import Sprite

class Alien(Sprite):  ##Sprite为了统一处理一系列显示对象 子弹
    """表示单个外星人的类"""

    def __init__(self,ai_settings,screen):
        super().__init__()       #调用父类Sprite的__init__函数.
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人图像，并设置其rect属性
        image = pygame.image.load('images/alien.jpg')  # 返回一个表示外星人的surface
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()  # get_rect() 获取相应的suiface的属性rect(矩形？)

        #每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height  #把screen长当作x正轴，宽当作y正轴，左上角作为原点

        #存储外星人的准确位置
        self.x = float(self.rect.x)
        self.health = 0
    def alien_location(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image,self.rect)  #根据外星人图片和矩形位置，设置好位置点，在屏幕上通过blit方法绘制出来

    def update(self):
        """向左或向右移动外星人"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction  #将移动量设置为外星人速度和fleet_direction的乘积，让外星人向左或向右移
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()  #通过get_rect()可以返回一个Rect实例
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0 :
            return True

