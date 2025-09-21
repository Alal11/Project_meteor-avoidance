import pygame
from pygame.rect import *
import random

def event_process():
    """이벤트 처리"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                return False
    return True

def handle_input():
    """키보드 입력 처리"""
    # 매 프레임마다 이동값 초기화
    move.x = 0
    move.y = 0
    
    # 현재 눌린 키 상태 확인
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        move.x = -3
    if keys[pygame.K_RIGHT]:
        move.x = 3
    if keys[pygame.K_UP]:
        move.y = -3
    if keys[pygame.K_DOWN]:
        move.y = 3

def move_player():
    """플레이어 이동 및 경계 처리"""
    if not is_game_over:
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
    if time_delay_counter > 7:
        time_delay_counter = 0
        return True
    time_delay_counter += 1
    return False

def make_star():
    """유성 랜덤 생성"""
    if is_game_over:
        return
    if time_delay():
        index = random.randint(0, len(star) - 1)
        if rec_star[index].y == -1:
            rec_star[index].x = random.randint(0, SCREEN_WIDTH - 20)  # 유성 크기 고려
            rec_star[index].y = 0

def move_star():
    """유성 이동 및 렌더링"""
    make_star()
    for i in range(len(star)):
        if rec_star[i].y == -1:
            continue
        if not is_game_over:
            rec_star[i].y += 1
        if rec_star[i].y > SCREEN_HEIGHT:
            rec_star[i].y = -1
        else:
            SCREEN.blit(star[i], rec_star[i])

def check_collision():
    """충돌 확인 및 점수 관리"""
    global score, is_game_over
    if is_game_over:
        return
    
    # 충돌 검사
    for rec in rec_star:
        if rec.y == -1:
            continue
        if (rec.top < rec_player.bottom and rec_player.top < rec.bottom and 
            rec.left < rec_player.right and rec_player.left < rec.right):
            print('충돌 발생!')
            is_game_over = True
            break
    
    # 게임 진행 중에만 점수 증가
    if not is_game_over:
        score += 1

def set_text():
    """점수 출력"""
    font = pygame.font.SysFont("arial", 20, True, False)
    score_surface = font.render(f'Score: {score}', True, 'green')
    SCREEN.blit(score_surface, (10, 10))
    
    # 게임오버 메시지 추가
    if is_game_over:
        game_over_font = pygame.font.SysFont("arial", 30, True, False)
        game_over_surface = game_over_font.render('GAME OVER', True, 'red')
        text_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        SCREEN.blit(game_over_surface, text_rect)

# === 변수 초기화 ===
is_active = True
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
move = Rect(0, 0, 0, 0)
time_delay_counter = 0
score = 0
is_game_over = False

# === 화면 설정 ===
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Meteor Avoidance Game")

# === 플레이어 생성 ===
player = pygame.image.load('player.png')
player = pygame.transform.scale(player, (20, 30))
rec_player = player.get_rect()
rec_player.centerx = SCREEN_WIDTH // 2
rec_player.centery = SCREEN_HEIGHT // 2

# === 유성 생성 ===
star = [pygame.image.load('star.png') for i in range(40)]
rec_star = [None for i in range(len(star))]
for i in range(len(star)):
    star[i] = pygame.transform.scale(star[i], (20, 20))
    rec_star[i] = star[i].get_rect()
    rec_star[i].y = -1

# === 게임 루프 ===
clock = pygame.time.Clock()

while is_active:
    # 화면 초기화
    SCREEN.fill((0, 0, 0))
    
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
    clock.tick(100)

pygame.quit()