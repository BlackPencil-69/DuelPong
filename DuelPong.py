import pygame
import sys
import random
import math

# Ініціалізація Pygame
pygame.init()

# Отримання розмірів екрана
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Pong Game")

# Кольори
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)

# Параметри гри
FPS = 60
BALL_RADIUS = 15
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 120
PADDLE_OFFSET = 30
BALL_SPEED = 7
PADDLE_SPEED = 10

# Налаштування відбивання
bounce_strength = 1.0
MIN_BOUNCE = 0.5
MAX_BOUNCE = 2.0

# Стан гри
game_paused = False

class Paddle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = PADDLE_SPEED
        self.score = 0

    def move(self, up=False, down=False):
        if not game_paused:
            if up and self.rect.top > 0:
                self.rect.y -= self.speed
            if down and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        # Випадковий початковий напрямок (вправо або вліво)
        angle = random.uniform(-math.pi/4, math.pi/4)
        if random.choice([True, False]):
            angle += math.pi
        self.dx = math.cos(angle) * BALL_SPEED
        self.dy = math.sin(angle) * BALL_SPEED
        self.original_speed = BALL_SPEED

    def move(self):
        if not game_paused:
            self.x += self.dx
            self.y += self.dy

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (int(self.x), int(self.y)), self.radius)

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        # Випадковий початковий напрямок (вправо або вліво)
        angle = random.uniform(-math.pi/4, math.pi/4)
        if random.choice([True, False]):
            angle += math.pi
        speed = self.original_speed
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def check_collision(self, left_paddle, right_paddle):
        # Перевірка зіткнення з верхньою та нижньою стінами
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.dy = -self.dy

        # Перевірка, чи м'яч попав на ліву або праву стіну
        if self.x - self.radius <= 0:
            right_paddle.score += 1
            self.reset()
            return

        if self.x + self.radius >= WIDTH:
            left_paddle.score += 1
            self.reset()
            return

        # Перевірка зіткнення з ракетками
        if (self.x - self.radius <= left_paddle.rect.right and
            self.y >= left_paddle.rect.top and
            self.y <= left_paddle.rect.bottom and
            self.dx < 0):
            # Відбивання від лівої ракетки
            self.dx = -self.dx * bounce_strength
            # Зміна кута відбивання в залежності від точки зіткнення з ракеткою
            relative_y = (self.y - left_paddle.rect.centery) / (PADDLE_HEIGHT / 2)
            self.dy += relative_y * 5

        if (self.x + self.radius >= right_paddle.rect.left and
            self.y >= right_paddle.rect.top and
            self.y <= right_paddle.rect.bottom and
            self.dx > 0):
            # Відбивання від правої ракетки
            self.dx = -self.dx * bounce_strength
            # Зміна кута відбивання в залежності від точки зіткнення з ракеткою
            relative_y = (self.y - right_paddle.rect.centery) / (PADDLE_HEIGHT / 2)
            self.dy += relative_y * 5

        # Обмеження швидкості м'яча для стабільності гри
        speed = math.sqrt(self.dx**2 + self.dy**2)
        max_speed = BALL_SPEED * 2  # Максимальна швидкість м'яча
        if speed > max_speed:
            self.dx = (self.dx / speed) * max_speed
            self.dy = (self.dy / speed) * max_speed

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.SysFont(None, 30)
        
    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(SCREEN, color, self.rect)
        pygame.draw.rect(SCREEN, WHITE, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        SCREEN.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.knob_rect = pygame.Rect(x, y, 20, height + 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        self.update_knob_position()
        
    def draw(self):
        # Малювання слайдера
        pygame.draw.rect(SCREEN, GRAY, self.rect)
        pygame.draw.rect(SCREEN, WHITE, self.rect, 2)
        pygame.draw.rect(SCREEN, WHITE, self.knob_rect)
        
        # Відображення значення
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Відбивання: {self.value:.1f}", True, WHITE)
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.y - 15))
        SCREEN.blit(text, text_rect)
        
    def update_knob_position(self):
        value_ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.knob_rect.centerx = self.rect.left + int(value_ratio * self.rect.width)
        self.knob_rect.centery = self.rect.centery
        
    def check_drag(self, pos, click, release):
        if self.knob_rect.collidepoint(pos) and click:
            self.dragging = True
        if release:
            self.dragging = False
            
        if self.dragging:
            x = min(max(pos[0], self.rect.left), self.rect.right)
            value_ratio = (x - self.rect.left) / self.rect.width
            self.value = self.min_val + value_ratio * (self.max_val - self.min_val)
            self.knob_rect.centerx = x
            return True
        return False

def draw_score(left_score, right_score):
    font = pygame.font.SysFont(None, 74)
    # Лівий рахунок (зелений)
    left_text = font.render(str(left_score), True, GREEN)
    SCREEN.blit(left_text, (WIDTH // 4, 30))
    # Правий рахунок (синій)
    right_text = font.render(str(right_score), True, BLUE)
    SCREEN.blit(right_text, (3 * WIDTH // 4, 30))

def draw_borders():
    # Верхня та нижня стіни
    pygame.draw.rect(SCREEN, WHITE, (0, 0, WIDTH, 10))  # Верхня стіна
    pygame.draw.rect(SCREEN, WHITE, (0, HEIGHT - 10, WIDTH, 10))  # Нижня стіна

def main():
    global game_paused, bounce_strength
    
    clock = pygame.time.Clock()
    
    # Створення об'єктів гри
    left_paddle = Paddle(PADDLE_OFFSET, HEIGHT // 2 - PADDLE_HEIGHT // 2, 
                         PADDLE_WIDTH, PADDLE_HEIGHT, GREEN)
    right_paddle = Paddle(WIDTH - PADDLE_OFFSET - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, 
                          PADDLE_WIDTH, PADDLE_HEIGHT, BLUE)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, RED)
    
    # Кнопки
    pause_button = Button(20, 20, 100, 40, "Пауза", (100, 100, 100), (150, 150, 150))
    settings_button = Button(WIDTH - 160, 20, 150, 40, "Налаштування", (100, 100, 100), (150, 150, 150))
    
    # Налаштування
    settings_open = False
    bounce_slider = Slider(WIDTH // 2 - 150, HEIGHT // 2, 300, 20, MIN_BOUNCE, MAX_BOUNCE, bounce_strength)
    
    running = True
    mouse_down = False
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        click = False
        release = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    mouse_down = True
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    release = True
                    mouse_down = False
        
        # Перевірка натискання кнопок
        pause_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        
        if pause_button.is_clicked(mouse_pos, click):
            game_paused = not game_paused
            
        if settings_button.is_clicked(mouse_pos, click):
            settings_open = not settings_open
        
        # Керування слайдером в налаштуваннях
        if settings_open and bounce_slider.check_drag(mouse_pos, click, release):
            bounce_strength = bounce_slider.value
        
        # Керування ракетками
        keys = pygame.key.get_pressed()
        
        # Лівий гравець (W/S або Ц/І для української розкладки)
        if keys[pygame.K_w]:
            left_paddle.move(up=True)
        if keys[pygame.K_s]:
            left_paddle.move(down=True)
            
        # Правий гравець (стрілки)
        if keys[pygame.K_UP]:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN]:
            right_paddle.move(down=True)
        
        # Оновлення позиції м'яча
        ball.move()
        ball.check_collision(left_paddle, right_paddle)
        
        # Відображення
        SCREEN.fill(BLACK)
        draw_borders()
        draw_score(left_paddle.score, right_paddle.score)
        
        left_paddle.draw()
        right_paddle.draw()
        ball.draw()
        
        pause_button.draw()
        settings_button.draw()
        
        # Відображення налаштувань, якщо відкриті
        if settings_open:
            # Напівпрозорий фон для налаштувань
            surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 180))
            SCREEN.blit(surface, (0, 0))
            
            # Текст заголовка
            font = pygame.font.SysFont(None, 50)
            title_text = font.render("Налаштування", True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            SCREEN.blit(title_text, title_rect)
            
            # Слайдер для відбивання м'яча
            bounce_slider.draw()
        
        # Відображення повідомлення про паузу, якщо гра на паузі
        if game_paused:
            font = pygame.font.SysFont(None, 74)
            pause_text = font.render("ПАУЗА", True, WHITE)
            pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            SCREEN.blit(pause_text, pause_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()