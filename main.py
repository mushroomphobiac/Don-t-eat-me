async def main():
    # --- 게임 설정 (메인 함수 안에서 실행) ---
    print("--- DEBUG: main 함수 시작 ---")
    pygame.init()
    print("--- DEBUG: pygame.init() 성공 ---")
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    print("--- DEBUG: screen 설정 성공 ---")
    pygame.display.set_caption("독버섯 피하기!")

    # 색상
    BLACK = (0, 0, 0)
    PINK_BG = (255, 224, 235)

    # --- 리소스 로딩 (메인 함수 안에서 실행) ---
    try:
        assets_path = "images"
        print(f"--- DEBUG: assets_path = {assets_path} ---")
        
        # 폰트 로딩
        print("--- DEBUG: 폰트 로딩 시도 ---")
        try:
            font = pygame.font.Font("font.ttf", 40)
            print("--- DEBUG: font.ttf 로딩 성공 ---")
        except pygame.error:
            font = pygame.font.Font(None, 50) # 기본 폰트
            print("--- DEBUG: 기본 폰트 로딩 성공 ---")

        # 이미지 로딩
        print("--- DEBUG: 플레이어 이미지 로딩 시도 ---")
        player_img = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "player.jpg")), (70, 70))
        print("--- DEBUG: 플레이어 이미지 로딩 성공 ---")
        
        print("--- DEBUG: 안전한 버섯 이미지 로딩 시도 ---")
        safe_images = [pygame.transform.scale(pygame.image.load(os.path.join(assets_path, f"s{i}.jpg")), (50, 50)) for i in range(1, 13)]
        print("--- DEBUG: 안전한 버섯 이미지 로딩 성공 ---")

        print("--- DEBUG: 독버섯 이미지 로딩 시도 ---")
        poison_images = [pygame.transform.scale(pygame.image.load(os.path.join(assets_path, f"p{i}.jpg")), (50, 50)) for i in range(1, 4)]
        print("--- DEBUG: 독버섯 이미지 로딩 성공 ---")
    
    except Exception as e:
        print(f"--- FATAL ERROR: 리소스 로딩 실패: {e} ---")