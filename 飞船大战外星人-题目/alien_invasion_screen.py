import sys
import pygame
import game_function
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()  #初始化背景设置，让pygame能够正确的工作
    alien_settings = Settings()
    screen = pygame.display.set_mode((alien_settings.screen_width,alien_settings.screen_height))  #创建显示窗口，实参（1200，800）是一个元组，指定窗口的显示尺寸
    pygame.display.set_caption("小飞船大战外星人")
    #创建Play按钮
    play_button = Button(alien_settings,screen,"Play")
    #创建存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(alien_settings)
    sb = Scoreboard(alien_settings,screen,stats)
    #创建一艘飞船、一个用于存储子弹的编组、一个外星人编组
    ship = Ship(screen,alien_settings)
    bullets = Group()
    aliens = Group()
    #创建外星人群
    game_function.create_aliens_group(alien_settings,screen,aliens,ship)
    #开始游戏的循环
    while True:
        game_function.check_events(alien_settings,screen,stats,play_button,ship,aliens,bullets,sb)
        if stats.game_active:
            ship.update()
            game_function.update_bullets(alien_settings,screen,ship,aliens,bullets,stats,sb)
            game_function.update_aliens(alien_settings,stats,screen,ship,aliens,bullets,sb)
        game_function.update_screen(alien_settings,screen,ship,bullets,aliens,stats,play_button,sb)

run_game()