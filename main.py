#!/usr/bin/env python3
"""
Super Snake - 超级贪吃蛇
一个美观、功能丰富的贪吃蛇游戏
"""

import pygame
import sys
import random
import os
from pathlib import Path

# 初始化 Pygame
pygame.init()
pygame.mixer.init()

# 颜色定义
COLORS = {
    'bg': (20, 20, 30),
    'bg_light': (30, 30, 45),
    'snake_head': (0, 255, 150),
    'snake_body': (0, 200, 120),
    'snake_body_dark': (0, 150, 100),
    'food': (255, 80, 80),
    'food_glow': (255, 100, 100),
    'special_food': (255, 215, 0),
    'text': (255, 255, 255),
    'text_dim': (150, 150, 150),
    'accent': (0, 200, 255),
    'grid': (35, 35, 50),
    'wall': (80, 80, 100),
    'button': (60, 60, 80),
    'button_hover': (80, 80, 100),
}

# 游戏设置
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE * 3
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE * 3
FPS = 60

# 方向
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0),
}


class Particle:
    """粒子特效类"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.05)
        self.size = random.randint(3, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        self.size = max(1, self.size - 0.1)

    def draw(self, surface):
        if self.life > 0:
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, int(255 * self.life)), 
                             (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))

    def is_dead(self):
        return self.life <= 0


class Snake:
    """蛇类"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
                    (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
                    (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        self.grow_pending = 0
        self.alive = True

    def update(self):
        if not self.alive:
            return

        # 更新方向
        opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if self.next_direction != opposite.get(self.direction):
            self.direction = self.next_direction

        # 计算新头部位置
        head_x, head_y = self.body[0]
        dx, dy = DIRECTIONS[self.direction]
        new_head = (head_x + dx, head_y + dy)

        # 检查碰撞
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.body):
            self.alive = False
            return

        # 移动
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def set_direction(self, direction):
        opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if direction != opposite.get(self.direction):
            self.next_direction = direction

    def grow(self, amount=1):
        self.grow_pending += amount

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            if i == 0:
                # 蛇头
                color = COLORS['snake_head']
                pygame.draw.rect(surface, color, rect, border_radius=4)
                
                # 画眼睛
                eye_size = 4
                eye_offset = 5
                dx, dy = DIRECTIONS[self.direction]
                
                if dx == 0:  # 垂直方向
                    eye_pos1 = (rect.centerx - eye_offset, rect.centery - eye_offset)
                    eye_pos2 = (rect.centerx + eye_offset, rect.centery - eye_offset)
                    if dy > 0:  # 向下
                        eye_pos1 = (rect.centerx - eye_offset, rect.centery + eye_offset - 2)
                        eye_pos2 = (rect.centerx + eye_offset, rect.centery + eye_offset - 2)
                else:  # 水平方向
                    eye_pos1 = (rect.centerx - eye_offset + (5 if dx > 0 else -5), rect.centery - eye_offset)
                    eye_pos2 = (rect.centerx - eye_offset + (5 if dx > 0 else -5), rect.centery + eye_offset)
                
                pygame.draw.circle(surface, (255, 255, 255), eye_pos1, eye_size)
                pygame.draw.circle(surface, (255, 255, 255), eye_pos2, eye_size)
                pygame.draw.circle(surface, (0, 0, 0), eye_pos1, eye_size - 1)
                pygame.draw.circle(surface, (0, 0, 0), eye_pos2, eye_size - 1)
            else:
                # 蛇身 - 渐变色
                ratio = i / len(self.body)
                color = tuple(int(c1 + (c2 - c1) * ratio) 
                             for c1, c2 in zip(COLORS['snake_body_dark'], COLORS['snake_body']))
                pygame.draw.rect(surface, color, rect, border_radius=3)


class Food:
    """食物类"""
    def __init__(self):
        self.position = self.spawn()
        self.special_timer = 0
        self.is_special = False

    def spawn(self):
        return (random.randint(1, GRID_WIDTH - 2),
                random.randint(1, GRID_HEIGHT - 2))

    def update(self):
        self.special_timer -= 1
        if self.special_timer <= 0:
            self.is_special = False
            # 30% 概率生成特殊食物
            if random.random() < 0.3:
                self.is_special = True
                self.special_timer = 600  # 10秒

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        center = rect.center
        
        if self.is_special:
            # 特殊食物 - 金色闪烁
            glow = abs(pygame.time.get_ticks() % 1000 - 500) / 500
            color = tuple(int(c + (255 - c) * glow * 0.5) for c in COLORS['special_food'])
            
            # 外发光
            for i in range(3, 0, -1):
                pygame.draw.circle(surface, (*color, 50), center, GRID_SIZE // 2 + i * 2)
            pygame.draw.circle(surface, color, center, GRID_SIZE // 2 - 2)
            
            # 星星形状
            pygame.draw.circle(surface, (255, 255, 200), center, 4)
        else:
            # 普通食物 - 红色带光晕
            for i in range(3, 0, -1):
                pygame.draw.circle(surface, (*COLORS['food_glow'], 30), center, GRID_SIZE // 2 + i)
            pygame.draw.circle(surface, COLORS['food'], center, GRID_SIZE // 2 - 2)


class Game:
    """游戏主类"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🐍 Super Snake")
        
        # 加载字体
        try:
            self.font = pygame.font.Font(None, 36)
            self.font_big = pygame.font.Font(None, 72)
            self.font_small = pygame.font.Font(None, 24)
        except:
            self.font = pygame.font.SysFont('arial', 36)
            self.font_big = pygame.font.SysFont('arial', 72)
            self.font_small = pygame.font.SysFont('arial', 24)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'MENU'  # MENU, PLAYING, PAUSED, GAMEOVER
        
        self.snake = Snake()
        self.food = Food()
        self.particles = []
        self.score = 0
        self.best_score = self.load_best_score()
        self.speed = 10  # 每秒移动次数
        
        self.last_update = pygame.time.get_ticks()
        self.update_interval = 1000 // self.speed

    def load_best_score(self):
        """加载最高分"""
        try:
            with open('.best_score', 'r') as f:
                return int(f.read())
        except:
            return 0

    def save_best_score(self):
        """保存最高分"""
        if self.score > self.best_score:
            self.best_score = self.score
            try:
                with open('.best_score', 'w') as f:
                    f.write(str(self.best_score))
            except:
                pass

    def spawn_particles(self, x, y, color, count=10):
        """生成粒子"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.state == 'MENU':
                    if event.key == pygame.K_RETURN:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                
                elif self.state == 'PLAYING':
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.set_direction('UP')
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.set_direction('DOWN')
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.set_direction('LEFT')
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.set_direction('RIGHT')
                    elif event.key == pygame.K_SPACE:
                        self.state = 'PAUSED'
                    elif event.key == pygame.K_ESCAPE:
                        self.state = 'MENU'
                
                elif self.state == 'PAUSED':
                    if event.key == pygame.K_SPACE:
                        self.state = 'PLAYING'
                    elif event.key == pygame.K_ESCAPE:
                        self.state = 'MENU'
                
                elif self.state == 'GAMEOVER':
                    if event.key == pygame.K_RETURN:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = 'MENU'

    def start_game(self):
        """开始新游戏"""
        self.snake.reset()
        self.food = Food()
        self.score = 0
        self.particles = []
        self.speed = 10
        self.update_interval = 1000 // self.speed
        self.state = 'PLAYING'

    def update(self):
        if self.state != 'PLAYING':
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update < self.update_interval:
            return

        self.last_update = current_time
        
        # 更新蛇
        self.snake.update()
        
        # 检查是否吃到食物
        if self.snake.body[0] == self.food.position:
            # 粒子特效
            fx = self.food.position[0] * GRID_SIZE + GRID_SIZE // 2
            fy = self.food.position[1] * GRID_SIZE + GRID_SIZE // 2
            color = COLORS['special_food'] if self.food.is_special else COLORS['food']
            self.spawn_particles(fx, fy, color, 15)
            
            # 加分
            if self.food.is_special:
                self.score += 50
                self.speed = min(20, self.speed + 1)
            else:
                self.score += 10
                self.speed = min(15, self.speed + 0.5)
            
            self.update_interval = 1000 // self.speed
            self.snake.grow()
            self.food = Food()
        
        # 检查游戏结束
        if not self.snake.alive:
            self.state = 'GAMEOVER'
            self.save_best_score()
            # 死亡粒子
            for x, y in self.snake.body[:5]:
                px = x * GRID_SIZE + GRID_SIZE // 2
                py = y * GRID_SIZE + GRID_SIZE // 2
                self.spawn_particles(px, py, COLORS['snake_head'], 5)
        
        # 更新食物
        self.food.update()
        
        # 更新粒子
        self.particles = [p for p in self.particles if not p.is_dead()]
        for p in self.particles:
            p.update()

    def draw_grid(self):
        """绘制背景网格"""
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLORS['grid'], (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLORS['grid'], (0, y), (SCREEN_WIDTH, y), 1)

    def draw_menu(self):
        """绘制菜单"""
        # 背景
        self.screen.fill(COLORS['bg'])
        self.draw_grid()
        
        # 标题
        title = self.font_big.render("🐍 SUPER SNAKE", True, COLORS['snake_head'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)
        
        # 最高分
        if self.best_score > 0:
            best_text = self.font.render(f"Best Score: {self.best_score}", True, COLORS['special_food'])
            best_rect = best_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60))
            self.screen.blit(best_text, best_rect)
        
        # 提示
        start_text = self.font.render("Press ENTER to Start", True, COLORS['text'])
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)
        
        controls = [
            "Controls:",
            "↑↓←→ or WASD - Move",
            "SPACE - Pause",
            "ESC - Menu"
        ]
        for i, line in enumerate(controls):
            text = self.font_small.render(line, True, COLORS['text_dim'])
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120 + i * 30))
            self.screen.blit(text, rect)

    def draw_playing(self):
        """绘制游戏画面"""
        # 背景
        self.screen.fill(COLORS['bg'])
        self.draw_grid()
        
        # 绘制食物
        self.food.draw(self.screen)
        
        # 绘制蛇
        self.snake.draw(self.screen)
        
        # 绘制粒子
        for p in self.particles:
            p.draw(self.screen)
        
        # UI - 分数
        score_text = self.font.render(f"Score: {self.score}", True, COLORS['text'])
        self.screen.blit(score_text, (20, 20))
        
        best_text = self.font.render(f"Best: {self.best_score}", True, COLORS['special_food'])
        self.screen.blit(best_text, (20, 60))
        
        # 速度指示
        speed_text = self.font_small.render(f"Speed: {self.speed:.1f}x", True, COLORS['accent'])
        self.screen.blit(speed_text, (SCREEN_WIDTH - 120, 20))

    def draw_paused(self):
        """绘制暂停画面"""
        self.draw_playing()
        
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # 暂停文字
        text = self.font_big.render("PAUSED", True, COLORS['text'])
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)
        
        sub_text = self.font.render("Press SPACE to Continue", True, COLORS['text_dim'])
        sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(sub_text, sub_rect)

    def draw_gameover(self):
        """绘制游戏结束画面"""
        self.screen.fill(COLORS['bg'])
        
        # 标题
        text = self.font_big.render("GAME OVER", True, COLORS['food'])
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(text, rect)
        
        # 分数
        score_text = self.font.render(f"Score: {self.score}", True, COLORS['text'])
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        if self.score >= self.best_score and self.score > 0:
            new_best = self.font.render("🎉 New Best Score! 🎉", True, COLORS['special_food'])
            new_rect = new_best.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(new_best, new_rect)
        
        # 提示
        hint_text = self.font.render("Press ENTER to Play Again", True, COLORS['text_dim'])
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(hint_text, hint_rect)

    def draw(self):
        if self.state == 'MENU':
            self.draw_menu()
        elif self.state == 'PLAYING':
            self.draw_playing()
        elif self.state == 'PAUSED':
            self.draw_paused()
        elif self.state == 'GAMEOVER':
            self.draw_gameover()
        
        pygame.display.flip()

    def run(self):
        """游戏主循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()
