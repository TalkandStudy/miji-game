import pygame
import sys
import random
import math
import os
import urllib.request
import zipfile
import shutil

# ===================== 资源下载解压配置 =====================
# 替换为你自己的资源压缩包URL
RESOURCE_URL = "https://github.com/TalkandStudy/miji-game/raw/refs/heads/main/mj.data.zip"  # 自定义URL
RESOURCE_ZIP_NAME = "mj_data_temp.zip"  # 临时压缩包文件名
TARGET_DIR = "mj_data"  # 目标文件夹

# ===================== 自动下载解压资源函数 =====================
def download_and_extract_resources():
    """检测资源文件夹，不存在则下载压缩包并解压"""
    # 检查目标文件夹是否存在
    if os.path.exists(TARGET_DIR):
        print(f"资源文件夹 {TARGET_DIR} 已存在，跳过下载")
        return True
    
    try:
        print(f"正在下载资源包：{RESOURCE_URL}")
        # 下载压缩包
        urllib.request.urlretrieve(RESOURCE_URL, RESOURCE_ZIP_NAME)
        print("下载完成，开始解压...")
        
        # 创建目标文件夹
        os.makedirs(TARGET_DIR, exist_ok=True)
        
        # 解压压缩包
        with zipfile.ZipFile(RESOURCE_ZIP_NAME, 'r') as zip_ref:
            zip_ref.extractall(TARGET_DIR)
        
        print("解压完成")
        
        # 删除临时压缩包
        if os.path.exists(RESOURCE_ZIP_NAME):
            os.remove(RESOURCE_ZIP_NAME)
            print(f"已删除临时压缩包：{RESOURCE_ZIP_NAME}")
        
        return True
    
    except Exception as e:
        print(f"资源下载/解压失败：{e}")
        # 清理临时文件
        if os.path.exists(RESOURCE_ZIP_NAME):
            os.remove(RESOURCE_ZIP_NAME)
        return False

# ===================== 初始化Pygame =====================
# 先下载解压资源
if not download_and_extract_resources():
    print("资源加载失败，游戏无法运行！")
    sys.exit(1)

pygame.init()
pygame.font.init()
pygame.mixer.init()  # 音频初始化

# 游戏窗口设置 - 1920x1220大窗口
WIDTH, HEIGHT = 1920, 1220
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MIJI-GAME")

# 颜色定义
BLUE = (98, 202, 255)    # 浅蓝色海洋背景
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (253, 85, 0)    # 鼠标发射子弹颜色
GREEN = (253, 85, 0)         # 1键发射子弹颜色
YELLOW = (255, 255, 0)      # 防空导弹颜色
GRAY = (150, 150, 150)      # 备用阴影色
BROWN = (139, 69, 19)       # 陆地颜色
GREEN_CAMP = (34, 139, 34)  # 军营颜色
ORANGE = (255, 165, 0)      # 主炮炮弹颜色

# ===================== 加载图片资源（路径改为mj_data/） =====================
try:
    # 近防炮图片
    cannon_img = pygame.image.load(f"{TARGET_DIR}/jfp.png").convert_alpha()
    cannon_img = pygame.transform.rotate(cannon_img, -90)
    cannon_img = pygame.transform.scale(cannon_img, (80, 80))
    # 导弹图片
    missile_img = pygame.image.load(f"{TARGET_DIR}/dd.png").convert_alpha()
    missile_img = pygame.transform.scale(missile_img, (40, 20))
    # 发射箱图片 - 旋转90度
    launcher_img = pygame.image.load(f"{TARGET_DIR}/fsx.png").convert_alpha()
    launcher_img = pygame.transform.rotate(launcher_img, 90)  # 旋转90度
    launcher_img = pygame.transform.scale(launcher_img, (60, 60))
    # 防空导弹图片 - 放大至100x40
    anti_missile_img = pygame.image.load(f"{TARGET_DIR}/fkdd.png").convert_alpha()
    anti_missile_img = pygame.transform.scale(anti_missile_img, (100, 40))
    # 加载船底图片
    ship_img = pygame.image.load(f"{TARGET_DIR}/c.png").convert_alpha()
    ship_img = pygame.transform.scale(ship_img, (800, 150))
    # 加载主炮图片
    main_cannon_img = pygame.image.load(f"{TARGET_DIR}/zp.png").convert_alpha()
    main_cannon_img = pygame.transform.rotate(main_cannon_img, -90)
    main_cannon_img = pygame.transform.scale(main_cannon_img, (120, 100))
    # 加载近防炮音效
    cannon_sound = pygame.mixer.Sound(f"{TARGET_DIR}/sounds/jfp.mp3")
    cannon_sound.set_volume(0.5)
    # 加载主炮音效
    main_cannon_sound = pygame.mixer.Sound(f"{TARGET_DIR}/sounds/zp.mp3")
    main_cannon_sound.set_volume(0.7)
except FileNotFoundError as e:
    print(f"警告：未找到文件 - {e}，使用默认替代")
    # 近防炮默认图形
    cannon_img = pygame.Surface((80, 80), pygame.SRCALPHA)
    pygame.draw.circle(cannon_img, (100, 100, 100), (40, 40), 40)
    # 来袭导弹默认图形
    missile_img = pygame.Surface((40, 20), pygame.SRCALPHA)
    pygame.draw.rect(missile_img, RED, (0, 0, 40, 20))
    # 发射箱默认图形（旋转90度）
    launcher_img = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.rect(launcher_img, (50, 50, 50), (0, 0, 60, 60))
    launcher_img = pygame.transform.rotate(launcher_img, 90)
    # 防空导弹默认图形
    anti_missile_img = pygame.Surface((100, 40), pygame.SRCALPHA)
    pygame.draw.rect(anti_missile_img, YELLOW, (0, 0, 100, 40))
    # 船底默认图形
    ship_img = pygame.Surface((800, 150), pygame.SRCALPHA)
    pygame.draw.rect(ship_img, WHITE, (0, 0, 800, 150), border_radius=20)
    pygame.draw.circle(ship_img, WHITE, (0, 75), 75)
    pygame.draw.circle(ship_img, WHITE, (800, 75), 75)
    # 主炮默认图形
    main_cannon_img = pygame.Surface((120, 100), pygame.SRCALPHA)
    pygame.draw.rect(main_cannon_img, (80, 80, 80), (0, 0, 120, 100))
    # 音效默认空
    cannon_sound = None
    main_cannon_sound = None

# ===================== 子弹类（寿命改为30） =====================
class Bullet:
    def __init__(self, x, y, angle, color=LIGHT_BLUE):
        self.x = x
        self.y = y
        self.speed = 15
        self.angle = angle
        self.radius = 3
        self.lifetime = 80  # 子弹寿命改为30
        self.active = True
        self.color = color

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1
        if (self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT or 
            self.lifetime <= 0):
            self.active = False

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# ===================== 主炮炮弹类（范围攻击） =====================
class MainCannonShell:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 8
        self.angle = angle
        self.active = True
        self.radius = 8  # 炮弹半径
        self.explode_radius = 60  # 爆炸范围
        self.lifetime = 150  # 飞行寿命
        self.has_exploded = False

    def update(self, targets):
        if self.has_exploded:
            self.active = False
            return
        
        # 飞行逻辑
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1

        # 触边/超时爆炸
        if (self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT or 
            self.lifetime <= 0):
            self.explode(targets)
            return

        # 碰撞检测（爆炸）
        for target in targets:
            if target.active:
                distance = math.hypot(target.x - self.x, target.y - self.y)
                if distance < self.radius + target.radius:
                    self.explode(targets)
                    break

    def explode(self, targets):
        """范围爆炸，摧毁范围内所有目标"""
        self.has_exploded = True
        # 攻击范围内目标
        for target in targets:
            if target.active:
                distance = math.hypot(target.x - self.x, target.y - self.y)
                if distance < self.explode_radius:
                    target.active = False

    def draw(self):
        if self.has_exploded:
            # 绘制爆炸效果
            pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.explode_radius, 2)
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.explode_radius//2, 1)
        else:
            # 绘制炮弹
            pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), self.radius)

# ===================== 来袭导弹类 =====================
class EnemyMissile:
    def __init__(self):
        # 随机生成初始位置（屏幕边缘）
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.x = random.randint(0, WIDTH)
            self.y = -50
        elif side == "bottom":
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT + 50
        elif side == "left":
            self.x = -50
            self.y = random.randint(0, HEIGHT)
        else:
            self.x = WIDTH + 50
            self.y = random.randint(0, HEIGHT)
        
        # 目标点（船底区域随机偏移）
        target_x = WIDTH/2 + random.randint(-150, 150)
        target_y = HEIGHT // 2 + random.randint(-50, 50)
        self.angle = math.atan2(target_y - self.y, target_x - self.x)
        self.speed = random.uniform(1, 4)  # 适配大窗口，提速
        self.active = True
        self.radius = 10  # 碰撞半径

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        # 到达船底或超出屏幕失效
        if (abs(self.x - WIDTH/2) < 30 and abs(self.y - (HEIGHT // 2)) < 30 or
            self.x < -100 or self.x > WIDTH + 100 or
            self.y < -100 or self.y > HEIGHT + 100):
            self.active = False

    def draw(self):
        rotated_missile = pygame.transform.rotate(missile_img, -math.degrees(self.angle))
        rect = rotated_missile.get_rect(center=(self.x, self.y))
        screen.blit(rotated_missile, rect)

# ===================== 军营类（可攻击目标） =====================
class Camp:
    def __init__(self):
        # 军营位置（陆地区域随机）
        self.x = random.randint(100, WIDTH - 100)
        self.y = random.randint(50, 150)  # 顶部陆地区域
        self.width = 80
        self.height = 50
        self.active = True
        self.radius = 40  # 碰撞半径

    def update(self):
        # 被攻击后失效
        pass

    def draw(self):
        if self.active:
            # 绘制绿色长方体军营
            pygame.draw.rect(screen, GREEN_CAMP, 
                            (self.x - self.width//2, self.y - self.height//2, 
                             self.width, self.height), border_radius=5)
            # 军营细节
            pygame.draw.rect(screen, BLACK, 
                            (self.x - self.width//2, self.y - self.height//2, 
                             self.width, self.height), 2)

# ===================== 防空导弹类（自动锁定+放大尺寸） =====================
class AntiMissile:
    def __init__(self, x, y, target_list):
        self.x = x
        self.y = y
        self.speed = 10  # 适配大窗口，提速
        self.active = True
        self.radius = 20  # 爆炸半径
        self.lock_range = 400  # 适配大窗口，扩大锁定范围
        self.target = self.lock_target(target_list)  # 自动锁定最近目标
        self.angle = 0
        if self.target:
            self.update_angle()

    def lock_target(self, target_list):
        """锁定范围内最近的来袭导弹"""
        closest_target = None
        min_distance = float('inf')
        for target in target_list:
            if target.active:
                distance = math.hypot(target.x - self.x, target.y - self.y)
                if distance < self.lock_range and distance < min_distance:
                    min_distance = distance
                    closest_target = target
        return closest_target

    def update_angle(self):
        """更新朝向目标的角度"""
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        self.angle = math.atan2(dy, dx)

    def update(self, target_list):
        if not self.active:
            return
        
        # 目标失效则重新锁定
        if not (self.target and self.target.active):
            self.target = self.lock_target(target_list)
            if not self.target:
                # 无目标则飞行一段时间后自毁
                self.x += math.cos(self.angle) * self.speed
                self.y += math.sin(self.angle) * self.speed
                if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
                    self.active = False
                return
        
        # 跟踪目标
        self.update_angle()
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # 碰撞检测（爆炸半径）
        distance = math.hypot(self.target.x - self.x, self.target.y - self.y)
        if distance < self.radius:
            self.target.active = False
            self.active = False

    def draw(self):
        if not self.active:
            return
        rotated_am = pygame.transform.rotate(anti_missile_img, -math.degrees(self.angle))
        rect = rotated_am.get_rect(center=(self.x, self.y))
        screen.blit(rotated_am, rect)

# ===================== 近防炮类（子弹计数+装填+音效） =====================
class Cannon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        # 射速设置
        self.base_fire_rate = 5
        self.fast_fire_rate = 2
        self.fire_timer = 0
        self.current_fire_rate = self.base_fire_rate
        # 子弹计数
        self.total_ammo = 900  # 总备弹
        self.current_ammo = 900 # 当前可用子弹
        self.reload_time = 140   # 装填时间（60帧=1秒）
        self.reload_timer = 0   # 装填计时器
        self.is_reloading = False

    def update(self, mouse_pos):
        # 装填逻辑
        if self.is_reloading:
            self.reload_timer += 1
            if self.reload_timer >= self.reload_time:
                self.current_ammo = self.total_ammo
                self.is_reloading = False
                self.reload_timer = 0
        
        # 朝向鼠标
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.angle = math.atan2(dy, dx)
        
        if self.fire_timer > 0:
            self.fire_timer -= 1

    def set_fire_rate(self, is_fast):
        self.current_fire_rate = self.fast_fire_rate if is_fast else self.base_fire_rate

    def can_fire(self):
        return (not self.is_reloading) and self.current_ammo > 0 and self.fire_timer == 0

    def fire(self, is_fast=False):
        if self.can_fire():
            self.set_fire_rate(is_fast)
            self.fire_timer = self.current_fire_rate
            self.current_ammo -= 1  # 消耗子弹
            # 子弹打完开始装填
            if self.current_ammo <= 0:
                self.is_reloading = True
            
            # 播放开枪音效
            if cannon_sound is not None:
                cannon_sound.play(maxtime=100)
            
            # 生成子弹
            bullet_x = self.x + math.cos(self.angle) * 40
            bullet_y = self.y + math.sin(self.angle) * 40
            bullet_color = GREEN if is_fast else LIGHT_BLUE
            return Bullet(bullet_x, bullet_y, self.angle, bullet_color)
        return None

    def draw(self):
        # 绘制近防炮
        rotated_cannon = pygame.transform.rotate(cannon_img, -math.degrees(self.angle))
        rect = rotated_cannon.get_rect(center=(self.x, self.y))
        screen.blit(rotated_cannon, rect)
        
        # 绘制弹药状态
        font = pygame.font.SysFont(None, 20)
        ammo_text = f"Ammo: {self.current_ammo}/{self.total_ammo}"
        if self.is_reloading:
            ammo_text += " (Reloading...)"
        text_surface = font.render(ammo_text, True, WHITE)
        screen.blit(text_surface, (self.x - 50, self.y + 50))

# ===================== 主炮类（范围攻击） =====================
class MainCannon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.fire_cooldown = 60  # 冷却时间（1秒）
        self.cooldown_timer = 0
        self.total_ammo = 50
        self.current_ammo = 50
        self.reload_time = 300  # 装填时间（5秒）
        self.is_reloading = False
        self.reload_timer = 0

    def update(self, mouse_pos):
        # 装填逻辑
        if self.is_reloading:
            self.reload_timer += 1
            if self.reload_timer >= self.reload_time:
                self.current_ammo = self.total_ammo
                self.is_reloading = False
                self.reload_timer = 0
        
        # 冷却逻辑
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
        
        # 朝向鼠标
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.angle = math.atan2(dy, dx)

    def can_fire(self):
        return (not self.is_reloading) and self.current_ammo > 0 and self.cooldown_timer == 0

    def fire(self):
        if self.can_fire():
            self.cooldown_timer = self.fire_cooldown
            self.current_ammo -= 1
            if self.current_ammo <= 0:
                self.is_reloading = True
            
            # 播放主炮音效
            if main_cannon_sound is not None:
                main_cannon_sound.play()
            
            # 生成主炮炮弹
            shell_x = self.x + math.cos(self.angle) * 60
            shell_y = self.y + math.sin(self.angle) * 60
            return MainCannonShell(shell_x, shell_y, self.angle)
        return None

    def draw(self):
        # 绘制主炮
        rotated_cannon = pygame.transform.rotate(main_cannon_img, -math.degrees(self.angle))
        rect = rotated_cannon.get_rect(center=(self.x, self.y))
        screen.blit(rotated_cannon, rect)
        
        # 绘制主炮弹药状态
        font = pygame.font.SysFont(None, 24)
        ammo_text = f"Main Cannon: {self.current_ammo}/{self.total_ammo}"
        if self.is_reloading:
            ammo_text += " (Reloading...)"
        text_surface = font.render(ammo_text, True, WHITE)
        screen.blit(text_surface, (self.x - 70, self.y + 60))

# ===================== 发射箱类（防空导弹计数+装填） =====================
class Launcher:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.max_ammo = 12       # 最大备弹
        self.current_ammo = 12   # 当前可用
        self.reload_time = 450  # 装填时间（3秒）
        self.reload_timer = 0   # 装填计时器
        self.is_reloading = False

    def update(self):
        # 装填逻辑
        if self.is_reloading:
            self.reload_timer += 1
            if self.reload_timer >= self.reload_time:
                self.current_ammo = self.max_ammo
                self.is_reloading = False
                self.reload_timer = 0

    def fire_anti_missile(self, target_list):
        """发射防空导弹"""
        if not self.is_reloading and self.current_ammo > 0:
            self.current_ammo -= 1
            # 打完开始装填
            if self.current_ammo <= 0:
                self.is_reloading = True
            return AntiMissile(self.x, self.y, target_list)
        return None

    def draw(self):
        # 绘制发射箱（已旋转90度）
        screen.blit(launcher_img, (self.x - 30, self.y - 30))
        # 绘制弹药状态
        font = pygame.font.SysFont(None, 20)
        ammo_text = f"Anti-Missile: {self.current_ammo}/{self.max_ammo}"
        if self.is_reloading:
            ammo_text += " (Reloading...)"
        text_surface = font.render(ammo_text, True, WHITE)
        screen.blit(text_surface, (self.x - 60, self.y + 40))

# ===================== 绘制陆地和军营 =====================
def draw_land_and_camps(camps):
    """绘制顶部棕色陆地和绿色军营"""
    # 绘制棕色陆地（顶部长条）
    land_rect = pygame.Rect(0, 0, WIDTH, 200)
    pygame.draw.rect(screen, BROWN, land_rect)
    # 绘制陆地细节
    pygame.draw.rect(screen, (101, 67, 33), land_rect, 3)
    
    # 绘制所有军营
    for camp in camps:
        camp.draw()

# ===================== 绘制船底（带晃动动画） =====================
def draw_ship(ship_x_base, ship_y_base, shake_offset):
    """绘制船底图片（带轻微晃动）"""
    # 应用晃动偏移
    ship_x = ship_x_base + shake_offset[0]
    ship_y = ship_y_base + shake_offset[1]
    screen.blit(ship_img, (ship_x, ship_y))
    return ship_x, ship_y

# ===================== 主游戏逻辑 =====================
def main():
    clock = pygame.time.Clock()
    
    # 船底基础位置（中央）
    ship_x_base = WIDTH // 2 - ship_img.get_width() // 2
    ship_y_base = HEIGHT // 2 - ship_img.get_height() // 2
    # 船体晃动参数
    shake_amplitude = 3  # 晃动幅度
    shake_speed = 0.05   # 晃动速度
    shake_time = 0
    
    # 创建武器（基于船底位置）
    # 左近防炮
    cannon1 = Cannon(WIDTH//2 - 300, HEIGHT // 2)
    # 右近防炮
    cannon2 = Cannon(WIDTH//2 + 120, HEIGHT // 2)
    # 船头主炮（船底前部中央）
    main_cannon = MainCannon(WIDTH//2 - 200, HEIGHT // 2 - 50)
    # 发射箱（旋转90度）
    launcher = Launcher(WIDTH//2, HEIGHT // 2 - 20)
    
    # 游戏对象列表
    bullets = []
    enemy_missiles = []
    anti_missiles = []
    main_cannon_shells = []
    camps = [Camp() for _ in range(5)]  # 生成5个军营
    
    # 无限生成导弹
    missile_spawn_timer = 0
    missile_spawn_interval = 50
    
    # 按键状态
    key_1_pressed = False
    key_2_clicked = False
    key_3_clicked = False  # 主炮发射键（3键）

    running = True
    while running:
        clock.tick(60)
        screen.fill(BLUE)

        # 计算船体晃动偏移（正弦曲线模拟海浪）
        shake_time += shake_speed
        shake_x = math.sin(shake_time) * shake_amplitude
        shake_y = math.cos(shake_time) * shake_amplitude
        shake_offset = (shake_x, shake_y)
        
        # 绘制顶部陆地和军营
        draw_land_and_camps(camps)
        
        # 绘制船底（带晃动）
        ship_x, ship_y = draw_ship(ship_x_base, ship_y_base, shake_offset)
        
        # 更新武器位置（跟随船体晃动）
        cannon1.x = WIDTH//2 - 300 + shake_x
        cannon1.y = HEIGHT // 2 + shake_y
        cannon2.x = WIDTH//2 + 120 + shake_x
        cannon2.y = HEIGHT // 2 + shake_y
        main_cannon.x = WIDTH//2 - 200 + shake_x
        main_cannon.y = HEIGHT // 2 - 50 + shake_y
        launcher.x = WIDTH//2 + shake_x
        launcher.y = HEIGHT // 2 - 20 + shake_y

        # 获取输入
        mouse_pos = pygame.mouse.get_pos()
        mouse_left_pressed = pygame.mouse.get_pressed()[0]

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key_1_pressed = True
                if event.key == pygame.K_2:
                    key_2_clicked = True
                if event.key == pygame.K_3:
                    key_3_clicked = True  # 3键发射主炮
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    key_1_pressed = False

        # 更新所有游戏对象
        # 武器更新
        cannon1.update(mouse_pos)
        cannon2.update(mouse_pos)
        main_cannon.update(mouse_pos)
        launcher.update()
        
        # 无限生成来袭导弹
        missile_spawn_timer += 1
        if missile_spawn_timer >= missile_spawn_interval:
            enemy_missiles.append(EnemyMissile())
            missile_spawn_timer = 0
            missile_spawn_interval = random.randint(30, 70)
        
        # 防空导弹更新
        for am in anti_missiles:
            am.update(enemy_missiles)
        
        # 主炮炮弹更新（可攻击导弹+军营）
        active_shells = []
        for shell in main_cannon_shells:
            shell.update(enemy_missiles + camps)
            if shell.active:
                shell.draw()
                active_shells.append(shell)
        main_cannon_shells = active_shells

        # 发射逻辑
        # 1. 近防炮发射（仅攻击导弹）
        if mouse_left_pressed:
            for cannon in [cannon1, cannon2]:
                bullet = cannon.fire(is_fast=False)
                if bullet:
                    bullets.append(bullet)
        if key_1_pressed:
            for cannon in [cannon1, cannon2]:
                bullet = cannon.fire(is_fast=True)
                if bullet:
                    bullets.append(bullet)
        
        # 2. 防空导弹发射（2键）
        if key_2_clicked:
            am = launcher.fire_anti_missile(enemy_missiles)
            if am:
                anti_missiles.append(am)
            key_2_clicked = False
        
        # 3. 主炮发射（3键）
        if key_3_clicked:
            shell = main_cannon.fire()
            if shell:
                main_cannon_shells.append(shell)
            key_3_clicked = False

        # 更新子弹
        active_bullets = []
        for bullet in bullets:
            bullet.update()
            if bullet.active:
                bullet.draw()
                active_bullets.append(bullet)
        bullets = active_bullets

        # 更新来袭导弹（碰撞检测）
        active_enemy_missiles = []
        for em in enemy_missiles:
            em.update()
            hit = False
            # 检测近防炮子弹碰撞（仅导弹）
            for bullet in bullets:
                dx = bullet.x - em.x
                dy = bullet.y - em.y
                if math.hypot(dx, dy) < (bullet.radius + em.radius):
                    bullet.active = False
                    hit = True
                    break
            if not hit and em.active:
                em.draw()
                active_enemy_missiles.append(em)
        enemy_missiles = active_enemy_missiles

        # 保留军营（仅主炮可攻击）
        active_camps = []
        for camp in camps:
            if camp.active:
                active_camps.append(camp)
        camps = active_camps

        # 绘制防空导弹
        for am in anti_missiles:
            am.draw()
        anti_missiles = [am for am in anti_missiles if am.active]

        # 绘制武器
        launcher.draw()
        cannon1.draw()
        cannon2.draw()
        main_cannon.draw()

        pygame.display.flip()

        # 绘制操作提示

        font = pygame.font.SysFont(None, 36)

                    
        missile_text = f"Try to use 1 2 3"
        screen.blit(font.render(missile_text, True, WHITE), (20, 220))
 
        
        hints = [
                "Made by WaspSquidW (c) 2025 WaspSquidW MIJI-Game",
                "WikiWaspWang@outlook.com",
                "v1.01"
                
            ]
        for i, hint in enumerate(hints):
            screen.blit(font.render(hint, True, WHITE), (20, HEIGHT - 80 + i*30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()