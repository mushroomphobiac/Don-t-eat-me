import pygame
import random
import os

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

# --- ⭐️ 중요: 파일 경로 설정 (웹 호환) ---
# 이미지 파일들이 있는 폴더 경로
assets_path = "images" 

try:
    # --- ⭐️ 폰트 로딩 수정 ---
    # font.ttf 파일이 있으면 사용하고, 없으면 Pygame의 기본 폰트를 사용합니다.
    # 이렇게 하면 폰트 파일이 없어도 게임이 멈추지 않습니다.
    font_path = "font.ttf"
    if os.path.exists(font_path):
        font = pygame.font.Font(font_path, 40)
    else:
        font = pygame.font.Font(None, 50) # Pygame 기본 폰트 사용

    # --- 이미지 로드 및 크기 조절 ---
    player_img = pygame.image.load(os.path.join(assets_path, "player.jpg"))
    player_img = pygame.transform.scale(player_img, (70, 70))

    safe_images = []
    for i in range(1, 13):
        image_file = os.path.join(assets_path, f"s{i}.jpg")
        safe_images.append(pygame.transform.scale(pygame.image.load(image_file), (50, 50)))

    poison_images = []
    for i in range(1, 4):
        image_file = os.path.join(assets_path, f"p{i}.jpg")
        poison_images.append(pygame.transform.scale(pygame.image.load(image_file), (50, 50)))

    running = True # 파일 로딩 성공 시 running = True

except pygame.error as e:
    print(f"파일 로딩 중 오류 발생: {e}")
    running = False # 파일 로딩 실패 시 running = False


# --- 게임 요소 생성 ---
player_rect = player_img.get_rect(centerx=screen_width // 2, bottom=screen_height - 20)
player_speed = 10
items = []

# 게임 변수
score = 0
lives = 3
start_time = pygame.time.get_ticks()
game_duration = 60000  # 60초

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# --- 메인 게임 루프 ---
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # --- ⭐️ 모바일 터치 이벤트 추가 ---
        # 마우스 클릭 또는 화면 터치(FINGERDOWN) 시 플레이어 이동
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            # 터치/클릭 위치 가져오기
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_pos = event.pos
            else: # FINGERDOWN 이벤트의 경우
                # 화면 좌표로 변환 필요
                touch_pos = (event.x * screen_width, event.y * screen_height)

            if touch_pos[0] > screen_width // 2:
                player_rect.x += player_speed * 3
            else:
                player_rect.x -= player_speed * 3
    
    # 게임오버가 아닐 때만 게임 로직 실행
    if not game_over:
        # 키보드 입력
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        # 플레이어가 화면 밖으로 나가지 않도록 처리
        player_rect.left = max(0, player_rect.left)
        player_rect.right = min(screen_width, player_rect.right)

        # 아이템 생성
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
                if item['type'] == 'safe':
                    score += 10
                else:
                    lives -= 1
            elif item['rect'].top > screen_height:
                items.remove(item)
        
        # 시간 계산 및 게임오버 조건 확인
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = (game_duration - elapsed_time) // 1000
        if remaining_time < 0:
            remaining_time = 0

        if lives <= 0 or remaining_time <= 0:
            game_over = True
    
    # --- 화면 그리기 ---
    screen.fill(PINK_BG)
    for item in items:
        screen.blit(item['img'], item['rect'])
    screen.blit(player_img, player_rect)
    
    # 점수, 생명, 시간 텍스트 그리기
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    time_text = font.render(f"Time: {remaining_time}", True, BLACK)
    
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (screen_width - 150, 10))
    screen.blit(time_text, (screen_width // 2 - 60, 10))

    # 게임오버 화면
    if game_over:
        end_text = font.render("Game Over", True, BLACK)
        final_score_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 50))
        screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2))

    pygame.display.flip()
    clock.tick(FPS)