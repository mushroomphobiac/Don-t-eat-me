import pygame
import random
import os

# --- 진단 메시지 1: 프로그램 시작 ---
print("DEBUG: 프로그램 시작, pygame.init() 이전")

# --- 게임 설정 ---
pygame.init()

print("DEBUG: pygame.init() 성공")

# 화면 크기
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("독버섯 피하기!")

# 색상
BLACK = (0, 0, 0)
PINK_BG = (255, 224, 235)

# 이미지 파일들이 있는 폴더 경로
assets_path = "images" 
font = None
running = False

try:
    # --- 진단 메시지 2: 폰트 로딩 시도 ---
    print("DEBUG: 폰트 로딩 시도...")
    font_path = "font.ttf"
    if os.path.exists(font_path):
        font = pygame.font.Font(font_path, 40)
        print("DEBUG: font.ttf 로딩 성공")
    else:
        font = pygame.font.Font(None, 50) # Pygame 기본 폰트 사용
        print("DEBUG: font.ttf 없음. Pygame 기본 폰트 사용")

    # --- 진단 메시지 3: 이미지 로딩 시도 ---
    print("DEBUG: 플레이어 이미지 로딩 시도...")
    player_img = pygame.image.load(os.path.join(assets_path, "player.jpg"))
    player_img = pygame.transform.scale(player_img, (70, 70))
    print("DEBUG: 플레이어 이미지 로딩 성공")

    print("DEBUG: 안전한 버섯 이미지 로딩 시작...")
    safe_images = []
    for i in range(1, 13):
        image_file = os.path.join(assets_path, f"s{i}.jpg")
        safe_images.append(pygame.transform.scale(pygame.image.load(image_file), (50, 50)))
    print("DEBUG: 안전한 버섯 이미지 로딩 완료")

    print("DEBUG: 독버섯 이미지 로딩 시작...")
    poison_images = []
    for i in range(1, 4):
        image_file = os.path.join(assets_path, f"p{i}.jpg")
        poison_images.append(pygame.transform.scale(pygame.image.load(image_file), (50, 50)))
    print("DEBUG: 독버섯 이미지 로딩 완료")

    running = True # 모든 파일 로딩 성공

except Exception as e:
    # --- 진단 메시지 4: 파일 로딩 중 에러 발생 ---
    print(f"FATAL_ERROR: 파일 로딩 중 치명적 오류 발생: {e}")
    running = False 


# --- 게임 요소 생성 ---
if running:
    player_rect = player_img.get_rect(centerx=screen_width // 2, bottom=screen_height - 20)
    player_speed = 10
    items = []

    # 게임 변수
    score = 0
    lives = 3
    start_time = pygame.time.get_ticks()
    game_duration = 60000

    # FPS 설정
    clock = pygame.time.Clock()
    FPS = 60
    print("DEBUG: 게임 변수 초기화 완료. 메인 루프 시작.")

# --- 메인 게임 루프 ---
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
    clock.tick(FPS)

# --- 진단 메시지 5: 프로그램 종료 ---
print("DEBUG: 메인 루프 종료. 프로그램 끝.")