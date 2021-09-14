#存储让游戏‘外星人入侵’运行的函数
import sys
import pygame
from ship import Ship
from alien import Alien
from bullet import Bullet
from time import sleep    #用于暂停游戏


def check_keydown_events(event,al_settings,screen,ship,bullets):
    """按下按键判断"""
    if event.key == pygame.K_RIGHT:  # 检查按下的是否是右箭头键
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(al_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:   #当按Q键时，关闭游戏
        sys.exit()


def check_keyup_events(event,ship):
    """松开按键判断"""
    if event.key == pygame.K_RIGHT:  # 确定此次松开的按键是否为右箭头键
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(al_settings,screen,stats,play_button,ship,aliens,bullets,sb):
    """监控键盘和鼠标事件"""
    for event in pygame.event.get():  # 为访问pygame检测到的事件，使用方法pygame.event.get() 所有键盘和鼠标事件都将促使for循环运行
        if event.type == pygame.QUIT:   #单击窗口的关闭按钮，会检测到pygame.QUIT事件
            sys.exit()   #退出游戏
        elif event.type == pygame.KEYDOWN:  #每次按键都会被注册为一个KEYDOWN事件
            check_keydown_events(event,al_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:  #松开按键
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:   #鼠标点击事件
            mouse_x,mouse_y = pygame.mouse.get_pos()  #pygame.mouse.get_pos()返回一个元祖，其中包含玩家单击时鼠标的x和y坐标
            check_play_button(al_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y,sb)  #将x和y轴坐标传递给check_play_button函数

def check_play_button(alien_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y,sb):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)  #collidepoint（x,y）函数会检查x和yd所得到的坐标 是否在play_button.rect里面
    if  button_clicked and not stats.game_active:
        #重置游戏设置
        alien_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，让飞船居中
        create_aliens_group(alien_settings,screen,aliens,ship)
        ship.center_ship()

def update_screen(alien_settings,screen,ship,bullets,aliens,stats,play_button,sb):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(alien_settings.background_color)  # 每次循环时都重绘屏幕,用背景色填充屏幕
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():  #bullets.sprites()返回一个列表，其中包含编组bullets中的所有精灵
        bullet.draw_bullet()   #将所有精灵绘制出来
    ship.ship_location()
    aliens.draw(screen)   #自动绘制编组内的每个外星人
    #显示得分
    sb.show_score()
    #如果游戏处于非活动状态，就绘制Play按钮.为让Play按钮位于其他所有屏幕元素上面，我们在绘制其他所有游戏元素后再绘制这个按钮，然后切换到新屏幕
    if not stats.game_active :
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()  # 每次执行while循环时，都会绘制一个空屏幕，并擦去旧屏幕，使得只有新屏幕显示 。
    # 在我们移动游戏元素时，pygame.display.flip()将不断更新屏幕，以显示元素的新位置，并在原来的位置隐藏元素，从而营造平滑移动的效果

def update_bullets(alien_settings,screen,ship,aliens,bullets,stats,sb):
    """更新子弹的位置，并删除已消失的子弹"""
    #更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():  # 在for循环中，不应从列表或编组中删除条目，因此必须遍历编组的副本
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(alien_settings, screen, ship, aliens, bullets,stats,sb)

def check_bullet_alien_collisions(alien_settings,screen,ship,aliens,bullets,stats,sb):
    """响应子弹和外星人的碰撞"""
    # collisions ：下面这行代码遍历编组bullets中的没每颗子弹，再遍历编组aliens中的每个外星人。每当有子弹和外星人的rect重叠时，groupcollide（）就
    # 在它返回的字典中添加一个键-值对。两个实参True告诉Pygame删除发生碰撞的子弹和外星人

    collisions = pygame.sprite.groupcollide(bullets,aliens,True,stats.delete)
    #stats.delete = False
    if collisions:
        stats.i = stats.i + 1
        if stats.i == 2:
            for aliens in collisions.values():
                stats.score += alien_settings.alien_points
                sb.prep_score()
            check_high_score(stats,sb)
            stats.delete=True
            #print(stats.delete)
            #pygame.sprite.groupcollide(bullets, aliens, True, True)
            stats.i=0;
        else:
            stats.delete = False
    if len(aliens) == 0:
        #如果整群外星人都被消灭，就提高一个等级
        bullets.empty()   #删除编组中余下的所有精灵
        alien_settings.increase_speed()
        #提高等级
        stats.level +=1
        sb.prep_level()
        create_aliens_group(alien_settings, screen, aliens, ship)

def fire_bullet(al_settings,screen,ship,bullets):
    "如果没达到子弹限制，则发射一颗子弹"
    if len(bullets) < al_settings.bullets_allowed:  # 保证屏幕上最多 al_settings.bullets_allowed 颗子弹
        # 创建一颗子弹，并将其加入到编组bullets中
        new_bullet = Bullet(al_settings, screen,ship)  # 编组bullets传递给了check_keydown_events（）.玩家按空格键时，创建一颗子弹，并用方法add()将其加入到编组bullets中
        bullets.add(new_bullet)

def create_aliens_group(alien_settings,screen,aliens,ship):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien = Alien(alien_settings,screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(alien_settings, alien_width)
    number_rows = get_number_rows(alien_settings,ship.rect.height,alien.rect.height)
    #创建第一行外星人
    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建一个外星人并将其加入当前行
            create_alien(alien_settings, screen, aliens, alien_number,number_row)

def get_number_aliens_x(alien_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = alien_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))  # 确保为整数
    return number_aliens_x

def create_alien(alien_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(alien_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 2*alien.rect.height + 3 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(alien_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = alien_settings.screen_height - ship_height -alien_height * 9  #10是为了缩小y的值，拉大和飞船的距离
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets,sb):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):  #spritecollideany()接受两个实参：一个精灵和一个编组。检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生碰撞的成员后就停止遍历编组。
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)    #在这里，spritecollideany()遍历编组aliens，并返回它找到的第一个与飞船发生了碰撞的外星人，如果没有发生碰撞。则会返回None，即print不会执行
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets,sb)

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites() : #遍历外星人群，对每个外星人调用check_edges()
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0 :
        #将ship_left减1
        stats.ships_left -= 1
        #更新记分牌
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_aliens_group(ai_settings, screen, aliens, ship)
        ship.center_ship()
        #暂停
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb):
    """检查是否有外星人达到了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets,sb)
            break

def check_high_score(stats,sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()