#设置类
class Settings():
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的静态配置"""
        #屏幕设置
        self.screen_width = 900
        self.screen_height = 650
        self.background_color = (40,40,40)

        #飞船的设置
        self.ship_limit = 2
        #外星人设置
        self.fleet_drop_speed = 5   #指定有外星人撞到屏幕边缘时，外星人群向下移动的速度

        #子弹设置  宽3像素、高15像素的深灰色子弹。子弹速度比飞船稍低
        self.bullet_width = 3
        self.bullet_height = 30
        self.bullet_color = 60,60,60
        self.bullets_allowed = 20   #屏幕上未消失的子弹数限制为20颗

        #加快游戏节奏的速度
        self.speedup_scale = 1.1
        #外星人点数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        #计分
        self.alien_points = 50

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.5

        # 外星人 fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置和外星人分数"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
