import pygame
import time
import os
import sys

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

# consts
WIDTH = 1080
HEIGHT = 840
FPS = 60
SPEED = 8

# vars
playerSpeed = 0
enemySpeed = 10
bullets, enemies, enemyBullets = [], [], []

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT * 0.85)

    def update(self):
        if self.rect.left > 0 and self.rect.right < WIDTH:
            self.rect.x += playerSpeed
        elif self.rect.left <= 0:
            self.rect.x += 1
        elif self.rect.right >= WIDTH:
            self.rect.x -= 1


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(
            os.path.join(img_folder, 'bullet.png')).convert(), (8, 8))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (player.rect.x + player_img.get_rect(
        ).size[0] / 2, HEIGHT * 0.85 - player_img.get_rect().size[0] / 2)

    def update(self):
        self.rect.y -= SPEED


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(img_folder, 'enemy.png')).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT * 0.15 +
                            HEIGHT * len(enemies) * 0.15)

    def update(self):
        self.rect.x += enemySpeed


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(
            os.path.join(img_folder, 'bullet.png')).convert(), (8, 8))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (
            enemy1.rect.x, enemy1.rect.y + enemy1.rect.size[0])

    def update(self):
        self.rect.y += SPEED


def collideBullets():
    for bullet in bullets:
        for enemy in enemies:
            if enemy.rect.collidepoint(bullet.rect.center):
                bullet.kill()
                enemy.kill()
                enemies.remove(enemy)

    for enemyBullet in enemyBullets:
        if player.rect.collidepoint(enemyBullet.rect.center):
            enemyBullet.kill()
            player.kill()


def createEnemy():
    enemy = Enemy()
    enemy.update()
    all_sprites.add(enemy)
    enemies.append(enemy)
    return enemy


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
player_img = pygame.image.load(os.path.join(img_folder, 'bts.png')).convert()
background = pygame.image.load(os.path.join(
    img_folder, "background.jpg")).convert()
background = pygame.transform.smoothscale(background, screen.get_size())

pygame.display.set_caption("Speteg")
pygame.display.set_icon(pygame.image.load(
    os.path.join(img_folder, "icon.ico")).convert())
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

player = Player()
player.update()
all_sprites.add(player)

enemy1 = createEnemy()

running = True
pause = False
shootTime = 0
enemyShoutTime = 0
while running:
    clock.tick(FPS)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and time.perf_counter() - shootTime > 1:
                bullet = PlayerBullet()
                bullet.update()
                all_sprites.add(bullet)
                bullets.append(bullet)
                shootTime = time.perf_counter()

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            playerSpeed = SPEED
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            playerSpeed = -SPEED
        else:
            playerSpeed = 0

    for enemy in enemies:
        if enemy.rect.right >= WIDTH:
            enemySpeed = -enemySpeed
        if enemy.rect.left <= 0:
            enemySpeed = -enemySpeed

        startTime = time.perf_counter()
        while (time.perf_counter() - startTime < 0.01) and (enemy in all_sprites):
            if time.perf_counter() - startTime >= 0.01:
                collideBullets()

        while enemy in all_sprites:
            if time.perf_counter() - enemyShoutTime > 1:
                enemyBullet = EnemyBullet()
                enemyBullet.update()
                all_sprites.add(enemyBullet)
                enemyBullets.append(enemyBullet)
                enemyShoutTime = time.perf_counter()
            if ~(enemy in all_sprites):
                break

    # update
    all_sprites.update()

    # visuals
    screen.blit(background, (0, 0))
    if len(enemies) == 0:
        pause = True
        text = pygame.font.Font(None, 64).render("YOU WIN!", True, GREEN)
        screen.blit(text, (WIDTH / 2 - 96, HEIGHT / 2 - 32))
        pygame.display.flip()
    elif (player in all_sprites) == False:
        pause = True
        text = pygame.font.Font(None, 64).render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH / 2 - 128, HEIGHT / 2 - 32))
        pygame.display.flip()
    else:
        text = pygame.font.Font(None, 64).render("", True, [255, 255, 0])
    screen.blit(text, (WIDTH / 2 - 96, HEIGHT / 2 - 32))
    screen.blit(pygame.font.Font(None, 32).render(
        "Version 1.3", True, WHITE), (WIDTH - 128, HEIGHT - 32))
    all_sprites.draw(screen)

    if pause == False:
        pygame.display.flip()
pygame.quit()