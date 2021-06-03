import pygame
import os
import time
import random
import os

pygame.font.init()

# SIZE OF THE GAME WINDOW
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and icon
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load(os.path.join("assets1", "gameicon.ico"))
pygame.display.set_icon(icon)

# Import Images/ Load  Images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets1", "alien1.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets1", "alien2.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets1", "alien3.png"))
PINK_SPACE_SHIP = pygame.image.load(os.path.join("assets1", "alien4.png"))
ORANGE_SPACE_SHIP = pygame.image.load(os.path.join("assets1", "alien5.png"))
NUT_SPACE_SHIP = pygame.image.load(os.path.join("assets1", "alien6.png"))
NAT_SPACE_SHIP = pygame.image.load(os.path.join("assets1", "alien7.png"))

# PLAYER/ USER SHIP
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets1", "pixel_ship_yellow.png"))

# Lasers/ Bullets
RED_LASER = pygame.image.load(os.path.join("assets1", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets1", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets1", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets1", "pixel_laser_yellow.png"))
PINK_LASER = pygame.image.load(os.path.join("assets1", "pixel_laser_pink.png"))
ORANGE_LASER = pygame.image.load(os.path.join("assets1", "pixel_laser_orange.png"))

# BACKGROUND
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets1", "background3.png")), (WIDTH, HEIGHT))


# creating laser object
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)


# DEFINING THE ATTRIBUTES OF THE SHIPS
class Ship:
    COOLDOWN = 20

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 7
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser.off_screen(HEIGHT):
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (
        self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health),
        10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "pink": (PINK_SPACE_SHIP, PINK_LASER),
        "orange": (ORANGE_SPACE_SHIP, ORANGE_LASER),
        "nut": (NUT_SPACE_SHIP, PINK_LASER),
        "nat": (NAT_SPACE_SHIP, RED_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    # Tells us the point of intersection (x, y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def getHighScore():
    with open("highscore.txt", "r")as f:
        return f.read()

def main():
    run = True
    FPS = 60
    level = 0
    lives = 6
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 70)

    enemies = []
    wave_length = 10 # number of enemies in a wave
    enemy_vel = 1 # movement speed of enemy ship

    player_vel = 6  # movement speed of player
    laser_vel = 20  # movement speed of laser

    player = Player(300, 630) # starting position of the player ship

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        '''refreshes screen'''
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (0, 55, 205))
        level_label = main_font.render(f"Level: {level}", 1, (0, 205, 55))

        try:
            highscore = int(getHighScore())
        except:
            highscore = 0

        # checking highest score
        if (highscore < level):
            highscore = level
        with open("highscore.txt", "w")as f:
            f.write(str(highscore))

        HighScore_label = main_font.render(f"HighScore: {highscore}", 1, (0, 155, 155))
        WIN.blit(HighScore_label, (10, 50))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Died!!", 1, (255, 55, 55))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # Checks if enemy is off the screen
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green", "pink", "orange", "nut", "nat"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # checks if any keys have been pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x + player_vel > 0:  # move left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # mive right
            player.x += player_vel
        if keys[pygame.K_w] and player.y + player_vel > 0:  # move up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # move down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 4 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press Mouse Button To Begin .....", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
