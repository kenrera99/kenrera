import pygame
import sys
import time
import random

# 初期化
pygame.init()
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("カップシャッフルゲーム")

hime_img = pygame.image.load("hime.png")
kerai_img = pygame.image.load("kerai.png")
# 必要に応じてサイズ調整
hime_img = pygame.transform.scale(hime_img, (60, 60))
kerai_img = pygame.transform.scale(kerai_img, (60, 60))

def draw_cups(pos, show_contents=False, reveal=False, selected=None, cup_map=None):
    screen.fill((240, 230, 210))
    font = pygame.font.SysFont(None, 36)
    for i in range(3):
        # カップの中身（姫・家来）を画像で表示
        if show_contents and cup_map:
            if cup_map[i] == "hime":
                screen.blit(hime_img, (pos[i] + CUP_WIDTH//2 - 30, CUP_Y + CUP_HEIGHT//2 - 80))
            elif cup_map[i] == "kerai":
                screen.blit(kerai_img, (pos[i] + CUP_WIDTH//2 - 30, CUP_Y + CUP_HEIGHT//2 - 80))
        # ...（以下省略）...
        # reveal時も同様に画像を表示したい場合は同じように書き換え

# カップの設定
CUP_WIDTH, CUP_HEIGHT = 80, 100
CUP_Y = 150
positions = [100, 260, 420]  # カップのX座標
colors = [(200, 150, 100), (180, 120, 80), (160, 100, 60)]  # カップの色

# 姫と家来の配置
hime_index = random.randint(0, 2)
kerai_indices = [i for i in range(3) if i != hime_index]

def draw_cups(pos, show_contents=False, reveal=False, selected=None, cup_map=None):
    screen.fill((240, 230, 210))
    font = pygame.font.SysFont(None, 36)
    for i in range(3):
        # カップの中身（姫・家来）を表示
        if show_contents and cup_map:
            if cup_map[i] == "hime":
                label = font.render("姫", True, (255, 0, 200))
                screen.blit(label, (pos[i] + CUP_WIDTH//2 - 20, CUP_Y + CUP_HEIGHT//2 - 60))
            elif cup_map[i] == "kerai":
                label = font.render("家来", True, (0, 100, 255))
                screen.blit(label, (pos[i] + CUP_WIDTH//2 - 20, CUP_Y + CUP_HEIGHT//2 - 60))
        # カップ本体
        pygame.draw.ellipse(screen, colors[i], (pos[i], CUP_Y, CUP_WIDTH, CUP_HEIGHT))
        # カップの番号
        num = font.render(str(i+1), True, (0, 0, 0))
        screen.blit(num, (pos[i] + CUP_WIDTH//2 - 10, CUP_Y + CUP_HEIGHT + 5))
        # 選択されたカップを強調
        if selected == i:
            pygame.draw.rect(screen, (255, 0, 0), (pos[i], CUP_Y, CUP_WIDTH, CUP_HEIGHT), 3)
        # 結果表示
        if reveal and cup_map:
            if cup_map[i] == "hime":
                label = font.render("姫", True, (255, 0, 200))
                screen.blit(label, (pos[i] + CUP_WIDTH//2 - 20, CUP_Y + CUP_HEIGHT//2 - 20))
            elif cup_map[i] == "kerai":
                label = font.render("家来", True, (0, 100, 255))
                screen.blit(label, (pos[i] + CUP_WIDTH//2 - 20, CUP_Y + CUP_HEIGHT//2 - 20))
    pygame.display.flip()

def animate_swap(pos, i, j, duration=0.5, steps=30):
    x0, x1 = pos[i], pos[j]
    for step in range(steps):
        t = step / steps
        pos_copy = pos[:]
        pos_copy[i] = x0 + (x1 - x0) * t
        pos_copy[j] = x1 + (x0 - x1) * t
        draw_cups(pos_copy)
        pygame.time.delay(int(duration * 1000 / steps))
    pos[i], pos[j] = x1, x0
    draw_cups(pos)

    # シャッフル回数を5～15回のランダムに設定
    shuffle_times = random.randint(5, 15)
    cup_map = shuffle_cups(positions, cup_map, shuffle_times=shuffle_times)

def shuffle_cups(pos, cup_map, shuffle_times=5):
    for _ in range(shuffle_times):
        i, j = random.sample([0, 1, 2], 2)
        animate_swap(pos, i, j)
        cup_map[i], cup_map[j] = cup_map[j], cup_map[i]
        time.sleep(0.3)
    return cup_map

def main():
    global hime_index, kerai_indices
    running = True
    selected = None
    reveal = False
    result = ""
    font = pygame.font.SysFont(None, 48)

    # カップの中身のマッピング（0:姫, 1:家来, 2:家来 など）
    cup_map = [None, None, None]
    cup_map[hime_index] = "hime"
    for idx in kerai_indices:
        cup_map[idx] = "kerai"

    # 1. 最初に姫・家来を表示
    draw_cups(positions, show_contents=True, cup_map=cup_map)
    pygame.display.flip()
    time.sleep(2)

    # 2. カップで隠す（中身非表示）
    draw_cups(positions)
    pygame.display.flip()
    time.sleep(1)

    # 3. シャッフル
    cup_map = shuffle_cups(positions, cup_map, shuffle_times=6)

    # 4. クリックで選択
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not reveal:
                mx, my = pygame.mouse.get_pos()
                for i in range(3):
                    rect = pygame.Rect(positions[i], CUP_Y, CUP_WIDTH, CUP_HEIGHT)
                    if rect.collidepoint(mx, my):
                        selected = i
                        reveal = True
                        # 判定
                        if cup_map[i] == "hime":
                            result = "正解！姫を見つけました！"
                        else:
                            result = "残念、不正解…"
        draw_cups(positions, reveal=reveal, selected=selected, cup_map=cup_map)
        if reveal:
            # 結果表示
            label = font.render(result, True, (255, 0, 0))
            screen.blit(label, (WIDTH//2 - label.get_width()//2, 50))
            pygame.display.flip()
        pygame.time.delay(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()