import pygame
import random
import sys
import os
import asyncio

# --- ⭐️ 경로 설정 (가장 중요!) ---
# 이 파이썬 파일이 있는 폴더의 절대 경로를 가져옵니다.
# 웹에서는 이 경로를 기준으로 이미지와 폰트를 찾게 됩니다.
try:
    # PyInstaller로 실행 파일을 만들었을 때의 경로 설정
    base_path = sys._MEIPASS
except AttributeError:
    # 일반 파이썬 환경일 때의 경로 설정
    base_path = os.path.abspath(".")

# --- 게임 설정 ---
pygame.init()

# 화면 크기
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("독버섯 피하기!")

# 색상
BLACK = (0, 0, 0)
PINK_BG = (255, 224, 235)

# 폰트 설정 (웹 안전 폰트로 수정)
font = pygame.font.SysFont("sans", 40)

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# --- 이미지 로드 및 크기 조절 ---
try:
    # ⭐️ 이미지 경로 수정 (os.path.join 사용)
    player_img = pygame.image.load(os.path.join(base_path, "player.jpg"))
    player_img = pygame.transform.scale(player_img, (70, 70))

    safe_item_files = [os.path.join(base_path, f"s{i}.jpg") for i in range(1, 13)]
    poison_item_files = [os.path.join(base_path, f"p{i}.jpg") for i in range(1, 4)]

    safe_images = [pygame.transform.scale(pygame.image.load(f), (50, 50)) for f in safe_item_files]
    poison_images = [pygame.transform.scale(pygame.image.load(f), (50, 50)) for f in poison_item_files]

except pygame.error as e:
    print("이미지 파일을 불러오는 중 오류가 발생했습니다.")
    print(e)
    pygame.quit()
    sys.exit()


# --- 게임 요소 생성 ---
player_rect = player_img.get_rect(centerx=screen_width // 2, bottom=screen_height - 20)
player_speed = 10
items = []

# 게임 변수
score = 0
lives = 3
start_time = pygame.time.get_ticks()
game_duration = 60000

# --- 메인 게임 함수 ---
async def main():
    global score, lives, start_time, player_rect, items

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_pos = pygame.mouse.get_pos()
                if touch_pos[0] > screen_width // 2:
                    player_rect.x += player_speed * 3
                else:
                    player_rect.x -= player_speed * 3

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_rect.x += player_speed

            player_rect.left = max(0, player_rect.left)
            player_rect.right = min(screen_width, player_rect.right)

            if random.randint(1, 35) == 1:
                item_type = 'poison' if random.randint(1, 4) == 1 else 'safe'
                item_x = random.randint(0, screen_width - 50)
                item_rect = pygame.Rect(item_x, -50, 50, 50)
                item_img = random.choice(poison_images) if item_type == 'poison' else random.choice(safe_images)
                items.append({'rect': item_rect, 'img': item_img, 'type': item_type, 'speed': random.randint(2, 4)})

            for item in items[:]:
                item['rect'].y += item['speed']
                if player_rect.colliderect(item['rect']):
                    items.remove(item)
                    if item['type'] == 'safe':
                        score += 10
                    else:
                        lives -= 1
                elif item['rect'].top > screen_height:
                    items.remove(item)
            
            elapsed_time = pygame.time.get_ticks() - start_time
            remaining_time = (game_duration - elapsed_time) // 1000

            if lives <= 0 or remaining_time < 0:
                lives = 0
                game_over = True

        screen.fill(PINK_BG)
        for item in items:
            screen.blit(item['img'], item['rect'])
        screen.blit(player_img, player_rect)
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        time_text = font.render(f"Time: {remaining_time if not game_over else 0}", True, BLACK)
        
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (screen_width - 150, 10))
        screen.blit(time_text, (screen_width // 2 - 60, 10))

        if game_over:
            end_text = font.render("Game Over", True, BLACK)
            final_score_text = font.render(f"Final Score: {score}", True, BLACK)
            screen.blit(end_text, (screen_width // 2 - 100, screen_height // 2 - 50))
            screen.blit(final_score_text, (screen_width // 2 - 120, screen_height // 2))

        pygame.display.flip()
        await asyncio.sleep(0)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())