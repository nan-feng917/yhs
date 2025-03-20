import pygame
import random
import os
import json

# 初始化pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)    # I型方块
YELLOW = (255, 255, 0)  # O型方块
PURPLE = (128, 0, 128)  # T型方块
BLUE = (0, 0, 255)     # J型方块
ORANGE = (255, 165, 0)  # L型方块
GREEN = (0, 255, 0)    # S型方块
RED = (255, 0, 0)      # Z型方块

# 游戏设置
BLOCK_SIZE = 30  # 每个方块的大小
GRID_WIDTH = 10  # 游戏区域宽度（以方块数计）
GRID_HEIGHT = 20 # 游戏区域高度（以方块数计）
MARGIN = 20      # 边距
SIDE_PANEL = 200 # 侧边栏宽度
SCREEN_WIDTH = BLOCK_SIZE * GRID_WIDTH + MARGIN * 3 + SIDE_PANEL  # 增加一个MARGIN的间距
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT + MARGIN * 2

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('俄罗斯方块')

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1],        # O
     [1, 1]],
    [[0, 1, 0],     # T
     [1, 1, 1]],
    [[0, 0, 1],     # J
     [1, 1, 1]],
    [[1, 0, 0],     # L
     [1, 1, 1]],
    [[0, 1, 1],     # S
     [1, 1, 0]],
    [[1, 1, 0],     # Z
     [0, 1, 1]]
]

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.game_over = False
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        # 初始化第一个方块和下一个方块
        self.next_piece = self.generate_piece()
        self.current_piece = self.generate_piece()
        self.high_score = self.load_high_score()  # 加载最高分

    def generate_piece(self):
        """生成一个新的方块"""
        shape = random.choice(SHAPES)
        color = SHAPE_COLORS[SHAPES.index(shape)]
        # 初始位置在顶部中间
        x = GRID_WIDTH // 2 - len(shape[0]) // 2
        y = 0
        return {'shape': shape, 'x': x, 'y': y, 'color': color}

    def new_piece(self):
        """获取下一个方块并生成新的下一个方块"""
        self.current_piece = self.next_piece
        self.next_piece = self.generate_piece()
        return self.current_piece

    def load_high_score(self):
        """从文件加载最高分"""
        try:
            if os.path.exists('highscore.json'):
                with open('highscore.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0

    def save_high_score(self):
        """保存最高分到文件"""
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open('highscore.json', 'w') as f:
                    json.dump({'high_score': self.high_score}, f)
            except:
                pass

    def draw(self):
        screen.fill(BLACK)
        
        # 绘制游戏区域边框
        pygame.draw.rect(screen, WHITE, 
                        [MARGIN-2, MARGIN-2, 
                         BLOCK_SIZE * GRID_WIDTH + 4,
                         BLOCK_SIZE * GRID_HEIGHT + 4], 2)
        
        # 绘制已固定的方块
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x],
                                   [MARGIN + x * BLOCK_SIZE, 
                                    MARGIN + y * BLOCK_SIZE,
                                    BLOCK_SIZE-1, BLOCK_SIZE-1])
        
        # 绘制当前方块
        if self.current_piece:
            for y, row in enumerate(self.current_piece['shape']):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.current_piece['color'],
                                       [MARGIN + (self.current_piece['x'] + x) * BLOCK_SIZE,
                                        MARGIN + (self.current_piece['y'] + y) * BLOCK_SIZE,
                                        BLOCK_SIZE-1, BLOCK_SIZE-1])

        # 绘制右侧信息面板
        info_panel_x = MARGIN + BLOCK_SIZE * GRID_WIDTH + MARGIN
        info_x = info_panel_x + 10  # 减小左边距

        # 游戏标题
        title_text = self.font.render('TETRIS', True, WHITE)
        screen.blit(title_text, (info_x, MARGIN))

        # 分数信息
        score_y = MARGIN + 50
        high_score_text = self.font.render(f'HIGH: {self.high_score}', True, WHITE)
        score_text = self.font.render(f'SCORE: {self.score}', True, WHITE)
        level_text = self.font.render(f'LEVEL: {self.level}', True, WHITE)
        lines_text = self.font.render(f'LINES: {self.lines_cleared}', True, WHITE)
        
        screen.blit(high_score_text, (info_x, score_y))
        screen.blit(score_text, (info_x, score_y + 40))
        screen.blit(level_text, (info_x, score_y + 80))
        screen.blit(lines_text, (info_x, score_y + 120))

        # 下一个方块预览
        next_piece_y = score_y + 140
        next_text = self.font.render('NEXT', True, WHITE)
        screen.blit(next_text, (info_x, next_piece_y))
        
        # 预览区域边框
        preview_box_y = next_piece_y + 30
        pygame.draw.rect(screen, WHITE,
                        [info_panel_x, preview_box_y,
                         SIDE_PANEL - MARGIN, BLOCK_SIZE * 4], 2)
        
        # 绘制下一个方块
        if self.next_piece:
            shape = self.next_piece['shape']
            color = self.next_piece['color']
            
            # 计算预览方块的居中位置
            preview_x = info_panel_x + (SIDE_PANEL - MARGIN - len(shape[0]) * BLOCK_SIZE) // 2
            preview_y = preview_box_y + (4 * BLOCK_SIZE - len(shape) * BLOCK_SIZE) // 2
            
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, color,
                                       [preview_x + x * BLOCK_SIZE,
                                        preview_y + y * BLOCK_SIZE,
                                        BLOCK_SIZE-1, BLOCK_SIZE-1])

        # 操作说明
        controls_y = next_piece_y + BLOCK_SIZE * 4 + 40
        controls = [
            'CONTROLS:',
            'LEFT/RIGHT: Move',
            'UP: Rotate',
            'DOWN: Soft drop',
            'SPACE: Hard drop'
        ]
        
        for i, text in enumerate(controls):
            control_text = self.small_font.render(text, True, WHITE)
            screen.blit(control_text, (info_x, controls_y + i * 25))

        # 游戏结束界面
        if self.game_over:
            # 创建半透明的黑色遮罩
            end_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            end_surface.set_alpha(128)
            end_surface.fill(BLACK)
            screen.blit(end_surface, (0, 0))

            # 绘制游戏结束信息
            game_over_text = self.font.render('GAME OVER', True, WHITE)
            final_score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
            restart_text = self.small_font.render('Press R to Restart', True, WHITE)

            # 计算文本位置使其居中
            game_over_x = (SCREEN_WIDTH - game_over_text.get_width()) // 2
            score_x = (SCREEN_WIDTH - final_score_text.get_width()) // 2
            restart_x = (SCREEN_WIDTH - restart_text.get_width()) // 2

            # 绘制文本
            screen.blit(game_over_text, (game_over_x, SCREEN_HEIGHT // 2 - 60))
            screen.blit(final_score_text, (score_x, SCREEN_HEIGHT // 2 - 20))
            screen.blit(restart_text, (restart_x, SCREEN_HEIGHT // 2 + 20))

            # 如果打破最高分，显示新纪录
            if self.score > self.high_score:
                new_record_text = self.font.render('NEW RECORD!', True, WHITE)
                record_x = (SCREEN_WIDTH - new_record_text.get_width()) // 2
                screen.blit(new_record_text, (record_x, SCREEN_HEIGHT // 2 + 60))
            
            # 保存最高分
            self.save_high_score()

    def valid_move(self, piece, x, y):
        """检查移动是否有效"""
        for i, row in enumerate(piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + j
                    new_y = y + i
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True

    def rotate_piece(self):
        """旋转当前方块"""
        if not self.current_piece:
            return
        
        # 获取当前形状的矩阵
        current_shape = self.current_piece['shape']
        # 创建新的旋转后的形状
        new_shape = [[current_shape[y][x] 
                     for y in range(len(current_shape)-1, -1, -1)]
                     for x in range(len(current_shape[0]))]
        
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = new_shape
        
        # 如果旋转后位置无效，则恢复原状
        if not self.valid_move(self.current_piece, 
                             self.current_piece['x'], 
                             self.current_piece['y']):
            self.current_piece['shape'] = old_shape

    def move(self, dx, dy):
        """移动方块"""
        if not self.current_piece:
            return
        
        new_x = self.current_piece['x'] + dx
        new_y = self.current_piece['y'] + dy
        
        if self.valid_move(self.current_piece, new_x, new_y):
            self.current_piece['x'] = new_x
            self.current_piece['y'] = new_y
            return True
        return False

    def drop_piece(self):
        """将方块放置到底部"""
        if not self.move(0, 1):
            self.freeze_piece()
            self.current_piece = self.new_piece()
            if not self.valid_move(self.current_piece, 
                                 self.current_piece['x'], 
                                 self.current_piece['y']):
                self.game_over = True
                self.save_high_score()  # 游戏结束时保存最高分

    def clear_lines(self):
        """检查并清除已填满的行"""
        lines_to_clear = []
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):  # 检查是否所有格子都被填充
                lines_to_clear.append(i)
        
        for line in lines_to_clear:
            # 删除已填满的行
            del self.grid[line]
            # 在顶部添加新的空行
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        # 计算得分
        cleared = len(lines_to_clear)
        if cleared > 0:
            self.lines_cleared += cleared
            # 根据消除的行数计算得分
            points = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += points.get(cleared, 0) * self.level
            # 每消除10行升一级
            self.level = self.lines_cleared // 10 + 1
            return True
        return False

    def freeze_piece(self):
        """将方块固定到网格中"""
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        # 在固定方块后检查是否可以消行
        self.clear_lines()

def main():
    def reset_game():
        nonlocal game, fall_time
        game = Tetris()
        fall_time = 0

    game = Tetris()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 1000
    
    while True:
        delta_time = clock.tick(60)
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                # 游戏结束状态的按键处理
                if game.game_over:
                    if event.key == pygame.K_r:  # R键重新开始
                        reset_game()
                    continue

                # 游戏控制键
                if not game.game_over:
                    if event.key == pygame.K_LEFT:
                        game.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.move(0, 1)
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        while game.move(0, 1):
                            continue
                        game.drop_piece()
                        fall_time = 0

        # 更新游戏状态
        if not game.game_over:
            fall_time += delta_time
            fall_speed = max(1000 - (game.level - 1) * 100, 100)
            
            if fall_time >= fall_speed:
                game.drop_piece()
                fall_time = 0
        
        # 绘制游戏状态
        game.draw()
        pygame.display.update()

if __name__ == '__main__':
    main() 