#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_x, player_y, player_speed, player_image, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_speed = player_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.player_speed
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.player_speed

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.y, 5, 'bullet.png', 10, 20)
        bullets.add(bullet)
        shoot.play()
        


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.player_speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(100, 600)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.player_speed
        if self.rect.y > 500:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.player_speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(100, 600)
    


monsters = sprite.Group()
for i in range(5):
    monster = Enemy(randint(100, 600), 0, randint(1, 2), 'ufo.png', 100, 75)
    monsters.add(monster)

lost = 0
count = 0


asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid(randint(100, 600), 0, randint(1, 2), 'asteroid.png', 75, 75)
    asteroids.add(asteroid)


player = Player(325, 350, 3, 'rocket.png', 55, 95)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()

window = display.set_mode((700, 500))
FPS = 60
clock = time.Clock()

background = transform.scale(image.load('galaxy.jpg'), (700, 500))

game = True
finish = False

font.init()
font1 = font.SysFont('Arial', 70)
win_text = font1.render('YOU WIN!', True, (0, 255, 0))
lose_text = font1.render('YOU LOSE!', True, (245, 0, 0))
font2 = font.SysFont('Arial', 35)

bullets = sprite.Group()

shoot = mixer.Sound('fire.ogg')
shoot.set_volume(0.1)

while game:
    if not finish:
        window.blit(background, (0, 0))
        clock.tick(FPS)
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        miss_text = font2.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        window.blit(miss_text, (10, 10))
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        for enemy in sprite.groupcollide(monsters, bullets, True, True):
            count += 1
            monster = Enemy(randint(100, 600), 0, randint(1, 2), 'ufo.png', 100, 75)
            monsters.add(monster)
        count_text = font2.render('Счёт: ' + str(count), True, (255, 255, 255))
        window.blit(count_text, (10, 50))
        sprite.groupcollide(bullets, asteroids, True, False)
        if sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(lose_text, (250, 250))
        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(lose_text, (250, 250))
        if lost > 3:
            finish = True
            window.blit(lose_text, (250, 250))
        if count > 10:
            finish = True
            window.blit(win_text, (250, 250))
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
        if e.type == QUIT:
            game = False
    display.update()

