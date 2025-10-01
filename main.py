import pygame
import random
import os
import asyncio

# --- 전역 변수 초기화 ---
screen = None
font = None
player_img = None
safe_images = []
poison_images = []
is_ready = False  # 모든 리소스가 로드되었는지 확인하는 플래그

# --- 게임 설정 ---
screen_width = 800
screen_height = 600
BLACK = (0, 0, 0)
PINK_BG = (255, 224, 235)

# --- 리소스 로딩 함수 ---
def load_resources():
    global screen, font, player_img, safe_images, poison_images, is_ready
    try:
        # pygame 초기화
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("독버섯 피하기!")

        # 경로 설정
        assets_path = "images"
        
        # 폰트 로딩
        font_path = "font.ttf"
        try:
            font = pygame.font.Font(font_path, 40)
        except pygame.error:
            font = pygame.font.Font(None, 50)

        # 이미지 로딩
        player_img = pygame.image.load(os.path.join(assets_path, "player.jpg")).convert_alpha()
        player_img = pygame.transform.scale(player_img, (70, 70))

        safe_images = [pygame.transform.scale(pygame.image.load(os.path.join(assets_path, f"s{i}.jpg")).convert_alpha(), (50, 50)) for i in range(1, 13)]
        poison_images = [pygame.transform.scale(pygame.image.load(os.path.join(assets_path, f"p{i}.jpg")).convert_alpha(), (50, 50)) for i in range(1, 4)]
        
        is_ready = True # 모든 리소스 로딩 성공
        print("모든 리소스 로딩 성공. 게임 준비 완료.")

    except Exception as e:
        print(f"리소스 로딩 중 심각한 오류 발생: {e}")
        is_ready = False

# --- 메인 게임 루프 ---
async def main():
    load_resources() # 게임 루프 시작 전에 리소스 로딩

    if not is_ready:
        # 리소스 로딩 실패 시 에러 메시지 표시
        screen.fill(BLACK)
        error_font = pygame.font.Font(None, 50)
        error_text = error_font.render("Resource Loading Failed!", True, (255, 0, 0))
        screen.blit(error_text, (screen_width // 2 - error_text.get_width() // 2, screen_height // 2 - error_text.get_height() // 2))
        pygame.display.flip()
        await asyncio.sleep(5)
        return

    # 게임 변수 초기화
    player_rect = player_img.get_rect(centerx=screen_width // 2, bottom=screen_height - 20)
    player_speed = 10
    items = []
    score = 0
    lives = 3
    start_time = pygame.time.get_ticks()
    game_duration = 60000
    clock = pygame.time.Clock()
    game_over = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # PC/모바일 터치 이벤트 처리
            if not game_over and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touch_pos = event.pos
                else: 
                    touch_pos = (event.x * screen_width, event.y * screen_height)

                if touch_pos[0] > screen_width // 2:
                    player_rect.x += player_speed * 3
                else:
                    player_rect.x -= player_speed * 3
        
        if not game_over:
            # 키보드 입력 (PC용)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: player_rect.x -= player_speed
            if keys[pygame.K_RIGHT]: player_rect.x += player_speed
            player_rect.left = max(0, player_rect.left)
            player_rect.right = min(screen_width, player_rect.right)

            # 아이템 생성 로직
            if random.randint(1, 35) == 1:
                item_type = 'poison' if random.randint(1, 4) == 1 else 'safe'
                item_x = random.randint(0, screen_width - 50)
                item_rect = pygame.Rect(item_x, -50, 50, 50)
                item_img = random.choice(poison_images) if item_type == 'poison' else random.choice(safe_images)
                items.append({'rect': item_rect, 'img': item_img, 'type': item_type, 'speed': random.randint(2, 4)})

            # 아이템 이동 및 충돌 처리
            for item in items[:]:
                item['rect'].y += item['speed']
                if player_rect.colliderect(item['rect']):
                    items.remove(item)
                    if item['type'] == 'safe': score += 10
                    else: lives -= 1
                elif item['rect'].top > screen_height: items.remove(item)
            
            # 시간 및 게임 종료 조건
            elapsed_time = pygame.time.get_ticks() - start_time
            remaining_time = (game_duration - elapsed_time) // 1000
            if remaining_time < 0: remaining_time = 0
            if lives <= 0 or remaining_time <= 0: game_over = True
        
        # 화면 그리기
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
        await asyncio.sleep(0) # 웹 환경을 위한 필수 코드

# asyncio로 main 함수 실행
if __name__ == "__main__":
    asyncio.run(main())