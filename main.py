#sprite
import pygame
import os
import random

FPS = 60
Width = 500
Height = 600

White  = (255, 255, 255)
Black  = (0, 0, 0)
Green  = (0, 255, 0)
Red    = (255, 0, 0)
Yellow = (255, 255, 0)

# 遊戲初始化 and 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("第一個遊戲")
clock = pygame.time.Clock()

#載入圖片
background_img = pygame.image.load(os.path.join('img', 'background.png')).convert()
player_img = pygame.image.load(os.path.join('img', 'player.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(Black)
pygame.display.set_icon(player_mini_img)
bullet_img = pygame.image.load(os.path.join('img', 'bullet.png')).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join('img', f'rock{i}.png')).convert())
#rock_img = pygame.image.load(os.path.join('img', 'rock.png')).convert()
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join('img', f'expl{i}.png')).convert()
    expl_img.set_colorkey(Black)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))

    player_expl_img = pygame.image.load(os.path.join('img', f'player_expl{i}.png')).convert()
    player_expl_img.set_colorkey(Black)
    expl_anim['player'].append(expl_img)
power_imgs = { }
power_imgs['shield'] = pygame.image.load(os.path.join('img', 'shield.png')).convert()
power_imgs['gun'] = pygame.image.load(os.path.join('img', 'gun.png')).convert()

#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join('sound', 'shoot.wav'))
die_sound = pygame.mixer.Sound(os.path.join('sound', 'rumble.ogg'))
expl_sounds= [
    pygame.mixer.Sound(os.path.join('sound', 'expl0.wav')),
    pygame.mixer.Sound(os.path.join('sound', 'expl1.wav'))
]
pygame.mixer.music.load(os.path.join('sound', 'background.ogg'))
pygame.mixer.music.set_volume(0.3)



font_name = os.path.join('font.ttf')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, White)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    rocks.add(r)
    all_sprites.add(r)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, Green, fill_rect)       #血條
    pygame.draw.rect(surf, White, outline_rect, 2) #外框

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, '太空生存戰', 64, Width/2 , Height/4)
    draw_text(screen, '← →:移動飛船 空白鍵:發射子彈', 22, Width/2 , Height/2)
    draw_text(screen, '按任意鍵開始遊戲', 18, Width/2 , Height*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS) #一秒內只能最多被執行10次
        #取得輸入
        for event in pygame.event.get(): #取得畫面裡的所有事件
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

#飛船
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(Black) #黑色變透明
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = Width/2
        self.rect.bottom = Height - 10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
 
    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = Width / 2
            self.rect.bottom = Height - 10
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        if self.rect.right > Width:
            self.rect.right = Width
        if self.rect.right < 0:
            self.rect.left = 0
    
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >=2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (Width / 2, Height + 500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

#石頭
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(Black)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.x = random.randrange(0, Width - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > Height or self.rect.left > Width or self.rect.right < 0:
            self.rect.x = random.randrange(0, Width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)

#子彈
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(Black) #黑色變透明
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#爆炸
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 #控制速度

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

#寶物
#子彈
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > Height:
            self.kill()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
for i in range(8):
    new_rock()
score = 0
pygame.mixer.music.play(-1) #無限播放

#遊戲迴圈
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break   
        draw_init()
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0
    clock.tick(FPS) #一秒內只能最多被執行10次
    #取得輸入
    for event in pygame.event.get(): #取得畫面裡的所有事件
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #更新遊戲
    all_sprites.update()

    #石頭子彈相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) #利用兩個sprites 判斷碰撞到是否刪掉
    for hit in hits:
        random.choice(expl_sounds).play()
        new_rock()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers .add(pow)
        score += hit.radius #石頭的半徑

    #石頭飛船相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        new_rock()

        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

        if player.lives == 0 and not(death_expl.alive()):
            show_init = True

    #寶物飛船相撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
        elif hit.type == 'gun':
            player.gunup()

    #畫面顯示
    screen.fill(Black)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, Width/2, 10)
    draw_health(screen, player.health, 5, 10)
    draw_lives(screen, player.lives, player_mini_img, Width-100, 15)
    pygame.display.update()

pygame.quit()