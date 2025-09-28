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
# pygbag 환경에서는 파일 경로를 현재 폴더 기준으로 단순하게 작성합니다.
# 이 코드를 실행하는 main.py 파일과 같은 위치에 이미지 폴더와 폰트 파일이 있어야 합니다.

# 폰트 파일 경로 (예: 'font.ttf' 파일을 프로젝트 폴더에 추가해야 합니다)
# 만약 'font'라는 폴더를 만들었다면 'font/font.ttf' 와 같이 경로를 지정합니다.
font_path = "font.ttf" 
# 이미지 파일들이 있는 폴더 경로
assets_path = "images" 

try:
    # 폰트 로드
    font = pygame.font.Font(font_path, 40)

    # --- 이미지 로드 및 크기 조절 ---
    # os.path.join을 사용하여 각 운영체제에 맞는 경로를 만들어줍니다.
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

except pygame.error as e:
    print(f"파일 로딩 중 오류 발생: {e}")
    # 웹 환경에서는 quit()을 호출하면 브라우저가 멈출 수 있으므로 루프를 중단합니다.
    running = False 


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

# --- ⭐️ 메인 게임 루프 (asyncio 제거) ---
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 모바일 터치 또는 마우스 클릭으로 이동 (간단하게 구현)
        if event.type == pygame.MOUSEBUTTONDOWN:
            touch_pos = pygame.mouse.get_pos()
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

    # 아이템 그리기
    for item in items:
        screen.blit(item['img'], item['rect'])
    
    # 플레이어 그리기
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

    # 화면 업데이트
    pygame.display.flip()
    
    # FPS 설정
    clock.tick(FPS)

# 웹 환경에서는 아래 두 줄이 필요 없습니다.
# pygame.quit()