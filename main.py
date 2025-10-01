import pygame
import random
import os
import asyncio # asyncio를 다시 사용합니다.

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

# --- 파일 경로 설정 (웹 호환 최종) ---
# 웹에서는 os.path.join만 사용해도 기본 경로에서 잘 찾아줍니다.
assets_path = "images"
font = None
player_img = None
safe_images = []
poison_images = []
running = False

try:
    font_path = "font.ttf"
    # 웹 환경에서는 폰트가 없으면 에러가 날 수 있으므로, 기본 폰트를 우선 사용합니다.
    try:
        font = pygame.font.Font(font_path, 40)
    except pygame.error:
        print(f"'{font_path}' 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")
        font = pygame.font.Font(None, 50)

    player_img = pygame.image.load(os.path.join(assets_path, "player.jpg"))
    player_img = pygame.transform.scale(player_img, (70, 70))

    for i in range(1, 13):
        image_file = os.path.join(assets_path, f"s{i}.jpg")
        safe_images.append(pygame.transform.scale(pygame.image.load(image_file), (50, 50)))

    for i in range(1, 4):
        image_file = os.path.join(assets_path, f"p{i}.jpg")
        poison_images.append(pygame.transform.scale(pygame.image.load(image_file), (50, 50)))

    running = True

except Exception as e:
    print(f"파일 로딩 중 치명적 오류 발생: {e}")
    running = False

# --- 메인 게임 함수 ---
async def main():
    global running
    
    if not running:
        print("파일 로딩 실패로 게임을 시작할 수 없습니다.")
        return # 파일 로딩 실패 시 함수 종료

    player_rect = player_img.get_rect(centerx=screen_width // 2, bottom=screen_height - 20)
    player_speed = 10
    items = []
    score = 0
    lives = 3
    start_time = pygame.time.get_ticks()
    game_duration = 60000
    clock = pygame.time.Clock()
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_pos = event.pos
                else: 
                    touch_pos = (event.x * screen_width, event.y * screen_height)

                if touch_pos[0] > screen_width // 2:
                    player_rect.x += player_speed * 3
                else:
                    player_rect.x -= player_speed * 3
        
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: player_rect.x -= player_speed
            if keys[pygame.K_RIGHT]: player_rect.x += player_speed
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
                    if item['type'] == 'safe': score += 10
                    else: lives -= 1
                elif item['rect'].top > screen_height: items.remove(item)
            
            elapsed_time = pygame.time.get_ticks() - start_time
            remaining_time = (game_duration - elapsed_time) // 1000
            if remaining_time < 0: remaining_time = 0
            if lives <= 0 or remaining_time <= 0: game_over = True
        
        screen.fill(PINK_BG)
        for item in items: screen.blit(item['img'], item['rect'])
        screen.blit(player_img, player_rect)
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        time_text = font.render(f"Time: {remaining_time}", True, BLACK)
        
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (screen_width - 150, 10))
        screen.blit(time_text, (screen_width // 2 - 60, 10))

        if game_over:
            end_text = font.render("Game Over", True, BLACK)
            final_score_text = font.render(f"Final Score: {score}", True, BLACK)
            screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 50))
            screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2))

        pygame.display.flip()
        await asyncio.sleep(0) # asyncio 루프를 위해 추가

# --- asyncio 실행 ---
if __name__ == "__main__":
    asyncio.run(main())