from pygame import * # библеотека программирования игр на python
font.init()
fontn = font.Font(None, 35)

# Класс-родитель для всех спрайтов:
class GameSprite(sprite.Sprite):
    def __init__(self, image_name, x, y, speed, width, height):
        super().__init__() # супер?

        self.image = transform.scale(image.load(image_name), (width, height))
        self.rect = self.image.get_rect(x = x, y = y)

        self.speed = speed

    def draw(self):
        wd.blit(self.image, self.rect)

# Класс-наследник для спрайтов-игроков (управление):
class Player(GameSprite):
    # Управление первого-левого игрока (W - вверх; S - вниз):
    def update_first(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < HEIGHT - 5:
            self.rect.y += self.speed
    
    # Управление второго-правого игрока (стрелка вверх; стрелка вниз):
    def update_second(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < HEIGHT - 5:
            self.rect.y += self.speed

WIDTH, HEIGHT = 600, 500
FPS = 60
bg_color = (200, 255, 255)

wd = display.set_mode((WIDTH, HEIGHT))
display.set_caption('Ping-Pong')
wd.fill(bg_color)
clock = time.Clock()

RUN = True
FINISH = False
speed_x, speed_y = 3, 3 # Скорость мяча по координатам x и y:

# Создание игровых спрайтов:
racket1 = Player('racket.png', 30, 200, 4, 50, 150)
racket2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('ball.png', 200, 200, 4, 50, 50)

# Создание текстов для проигрышей игроков:
lose_text1 = fontn.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose_text2 = fontn.render('PLAYER 2 LOSE!', True, (180, 0, 0))

while RUN:
    for e in event.get():
        if e.type == QUIT: RUN = False

    if not FINISH:
        wd.fill(bg_color)

        # Обновление событий:
        racket1.update_first()
        racket2.update_second()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # Отталкивание мяча при сталкновении с ракетками:
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
        if ball.rect.y < 0 or ball.rect.bottom > HEIGHT:
            speed_y *= -1

        # Проигрыш игрока 1/2 при пропуске мяча об левый/правый края окна:
        if ball.rect.x < 0:
            wd.blit(lose_text1, (200, 200))
            FINISH = True
            LOSE = True
        if ball.rect.right > WIDTH:
            wd.blit(lose_text2, (200, 200))
            FINISH = True
            LOSE = True

        # Отрисовка изображений спрайтов в новом положений
        racket1.draw()
        racket2.draw()
        ball.draw()
    
    display.update()
    clock.tick(FPS)