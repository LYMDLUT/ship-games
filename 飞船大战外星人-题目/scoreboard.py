import pygame.font  #pygame.font模块能够将文本渲染到屏幕
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """显示得分信息的类"""
    def __init__(self,alien_settings,screen,stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = alien_settings
        self.stats = stats

        #显示得分信息时使用的字体设置
        self.text_color = (130,130,130)
        self.font = pygame.font.SysFont(None,30)  #指定使用什么字体来渲染文本。实参None让Pygame使用默认字体，而48指定了文本的字号

        #准备包含最高得分和当前得分的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score,-1))  # 进行四舍五入的操作 -1 即精确到10位
        score_str = "{:,}".format(rounded_score) #:,空白插入 , 即输出eg:1,000,000而不是1000000
        self.score_image = self.font.render('score: '+str(score_str),True,self.text_color,self.ai_settings.background_color) #font.render()将文本信息转换成图像

        #将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right -20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高分转换成渲染的图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render('highest score '+high_score_str, True,self.text_color,self.ai_settings.background_color)  # font.render()将文本信息转换成图像
        # 将最高分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top =  self.score_rect.top

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image,self.score_rect) #调用screen.blit(),通过向它传递一幅图像以及与该图像相关联的rect对象，从而在屏幕上绘制文本图像
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        #绘制飞船
        self.ships.draw(self.screen)

    def prep_level(self):
        """将等级转换成渲染的图像"""
        self.level_image = self.font.render('Grade'+str(self.stats.level),True,self.text_color,self.ai_settings.background_color)

        #将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom +10

    def prep_ships(self):
        """显示还余下多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.screen,self.ai_settings)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
