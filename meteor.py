import pygame
from pygame.rect import *

def eventProcess():
    for event in pygame.event.get():
        if event.type ==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                pygame.quit()

            if event.key==pygame.K_LEFT:
                move.x=-1
            if event.key==pygame.K_RIGHT:
                move.x=1
            if event.key==pygame.K_UP:
                move.y=-1
            if event.key==pygame.K_DOWN:
                move.y=1

def movePlayer():
    SCREEN.blit(player, recPlayer)

    recPlayer.x+=move.x
    recPlayer.y+=move.y

    # 로켓이 창을 넘어가지 않도록 설정
    if recPlayer.x<0:
        recPlayer.x=0
    if recPlayer.x>SCREEN_WIDHT-recPlayer.width:
        recPlayer.x=SCREEN_WIDHT-recPlayer.width

    if recPlayer.y<0:
        recPlayer.y=0
    if recPlayer.y>SCREEN_HEIGHT-recPlayer.height:
        recPlayer.y=SCREEN_HEIGHT-recPlayer.height

    SCREEN.blit(player,recPlayer)



def moveStar():
    SCREEN.blit(star, recStar)


# 1. 변수 초기화
isActive = True
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
move=Rect(0,0,0,0)

# 2. 스크린 설정
pygame.init()  # gygame 라이브러리를 제일 처음 사용하기 위한 동작
SCREEN = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption("CodingNow!")

# 3. player 생성
player = pygame.image.load('player.png')
player = pygame.transform.scale(player, (20, 30))  # 로켓 크기 설정
recPlayer = player.get_rect()
recPlayer.centerx = (SCREEN_WIDHT / 2)
recPlayer.centery = (SCREEN_HEIGHT / 2)

# 4. 유성 생성
star = pygame.image.load('star.png')
star = pygame.transform.scale(star, (20, 20))  # 유성 크기 설정
recStar = player.get_rect()
# 5. 기타
clock=pygame.time.Clock()  # 객체에 시간을 줌


#### 반복 ####
while isActive:
    # 1. 화면 지움
    SCREEN.fill((0,0,0))  # 로켓 잔상 제거 (스크린을 검정색으로 칠함)
    # 2. 이벤트 처리
    eventProcess()
    # 3. 플레이어 이동
    movePlayer()
    # 4. 유성 생성 및 이동
    moveStar()
    # 5. 충돌 확인
    # 6. text 업데이트
    # 7. 화면 경신
    pygame.display.flip()
    clock.tick(100)  # 로켓 동작 시간 느리게
#### 반복 ####

