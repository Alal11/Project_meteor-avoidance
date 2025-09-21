import pygame
from pygame.rect import *
import random

def event_process():
    """이벤트 처리 - 종료 및 재시작"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                return False
            # 게임오버 상태에서 R키로 재시작
            if event.key == pygame.K_r and is_game_over:
                restart_game()
    return True

def handle_input():
    """키보드 입력 처리 - 연속 입력"""
    # 게임오버 중에는 이동 불가
    if is_game_over:
        return
        
    # 매 프레임마다 이동값 초기화
    move.x = 0
    move.y = 0
    
    # 현재 눌린 키 상태 확인
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        move.x = -4  # 속도 약간 증가
    if keys[pygame.K_RIGHT]:
        move.x = 4
    if keys[pygame.K_UP]:
        move.y = -4
    if keys[pygame.K_DOWN]:
        move.y = 4

def move_player():
    """플레이어 이동 및 경계 처리"""
    if is_game_over:
        return
        
    rec_player.x += move.x
    rec_player.y += move.y
    
    # 경계 제한
    if rec_player.x < 0:
        rec_player.x = 0
    if rec_player.x > SCREEN_WIDTH - rec_player.width:
        rec_player.x = SCREEN_WIDTH - rec_player.width
    if rec_player.y < 0:
        rec_player.y = 0
    if rec_player.y > SCREEN_HEIGHT - rec_player.height:
        rec_player.y = SCREEN_HEIGHT - rec_player.height
    
    SCREEN.blit(player, rec_player)

def time_delay():
    """유성 생성 딜레이 관리"""
    global time_delay_counter
    if time_delay_counter > 5:  # 딜레이 줄여서 더 어렵게
        time_delay_counter = 0
        return True
    time_delay_counter += 1
    return False

def make_star():
    """유성 랜덤 생성"""
    if is_game_over:
        return
    if time_delay():
        # 비활성 유성 찾아서 활성화
        for i in range(len(star)):
            if rec_star[i].y == -1:
                rec_star[i].x = random.randint(0, SCREEN_WIDTH - 20)
                rec_star[i].y = 0
                break

def move_star():
    """유성 이동 및 렌더링"""
    make_star()
    for i in range(len(star)):
        if rec_star[i].y == -1:
            continue
        if not is_game_over:
            rec_star[i].y += 2  # 유성 속도 증가
        if rec_star[i].y > SCREEN_HEIGHT:
            rec_star[i].y = -1
        else:
            SCREEN.blit(star[i], rec_star[i])

def check_collision():
    """충돌 확인 및 점수 관리"""
    global score, is_game_over
    if is_game_over:
        return
    
    # 충돌 검사 - colliderect 사용으로 정확도 향상
    for rec in rec_star:
        if rec.y == -1:
            continue
        if rec_player.colliderect(rec):
            print('게임 오버! 충돌 발생')
            is_game_over = True
            return
    
    # 게임 진행 중에만 점수 증가
    score += 1

def set_text():
    """점수 및 상태 출력"""
    # 점수 표시
    font = pygame.font.Font(None, 32)
    score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    SCREEN.blit(score_surface, (10, 10))
    
    # 게임오버 메시지
    if is_game_over:
        # 게임오버 텍스트
        big_font = pygame.font.Font(None, 48)
        game_over_surface = big_font.render('GAME OVER', True, (255, 100, 100))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        SCREEN.blit(game_over_surface, game_over_rect)
        
        # 재시작 안내
        restart_font = pygame.font.Font(None, 28)
        restart_surface = restart_font.render('Press R to Restart', True, (255, 255, 100))
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        SCREEN.blit(restart_surface, restart_rect)
        
        # 최고 점수 표시
        best_surface = restart_font.render(f'Best: {best_score}', True, (100, 255, 100))
        best_rect = best_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        SCREEN.blit(best_surface, best_rect)

def restart_game():
    """게임 재시작"""
    global score, is_game_over, time_delay_counter, best_score
    
    # 최고 점수 업데이트
    if score > best_score:
        best_score = score
    
    # 게임 상태 초기화
    score = 0
    is_game_over = False
    time_delay_counter = 0
    
    # 플레이어 위치 초기화
    rec_player.centerx = SCREEN_WIDTH // 2
    rec_player.centery = SCREEN_HEIGHT // 2
    
    # 이동 상태 초기화
    move.x = 0
    move.y = 0
    
    # 모든 유성 비활성화
    for rec in rec_star:
        rec.y = -1
    
    print('게임 재시작!')

# === 변수 초기화 ===
is_active = True
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
move = Rect(0, 0, 0, 0)
time_delay_counter = 0
score = 0
best_score = 0  # 최고 점수 추가
is_game_over = False

# === 화면 설정 ===
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meteor Avoidance Game v2.0")

# === 플레이어 생성 ===
player = pygame.image.load('player.png')
player = pygame.transform.scale(player, (20, 30))
player.fill((255, 255, 255), special_flags=pygame.BLEND_MULT)
rec_player = player.get_rect()
rec_player.centerx = SCREEN_WIDTH // 2
rec_player.centery = SCREEN_HEIGHT // 2

# === 유성 생성 (개수 최적화) ===
star = [pygame.image.load('star.png') for i in range(20)]  # 40 → 20으로 줄임
rec_star = [None for i in range(len(star))]
for i in range(len(star)):
    star[i] = pygame.transform.scale(star[i], (20, 20))
    rec_star[i] = star[i].get_rect()
    rec_star[i].y = -1

# === 게임 루프 ===
clock = pygame.time.Clock()

print("=== Meteor Avoidance Game v2.0 시작! ===")
print("조작법: 방향키로 이동, R키로 재시작, ESC로 종료")

while is_active:
    # 화면 초기화 (어두운 파란색 배경)
    SCREEN.fill((10, 10, 40))
    
    # 이벤트 처리
    is_active = event_process()
    
    # 키보드 입력 처리
    handle_input()
    
    # 게임 로직
    move_player()
    move_star()
    check_collision()
    set_text()
    
    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)  # 60 FPS로 최적화

pygame.quit()
print("게임 종료!")