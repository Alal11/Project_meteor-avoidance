import pygame
from pygame.rect import *
import random


def eventProcess():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            if event.key == pygame.K_LEFT:
                move.x = -1
            if event.key == pygame.K_RIGHT:
                move.x = 1
            if event.key == pygame.K_UP:
                move.y = -1
            if event.key == pygame.K_DOWN:
                move.y = 1


def movePlayer():
    SCREEN.blit(player, recPlayer)

    recPlayer.x += move.x
    recPlayer.y += move.y

    # 로켓이 창을 넘어가지 않도록 설정
    if recPlayer.x < 0:
        recPlayer.x = 0
    if recPlayer.x > SCREEN_WIDTH - recPlayer.width:
        recPlayer.x = SCREEN_WIDTH - recPlayer.width

    if recPlayer.y < 0:
        recPlayer.y = 0
    if recPlayer.y > SCREEN_HEIGHT - recPlayer.height:
        recPlayer.y = SCREEN_HEIGHT - recPlayer.height

    SCREEN.blit(player, recPlayer)


def timeDelay():  # 유성 속도 조절
    global time_delay
    if time_delay>7:
        time_delay=0
        return True

    time_delay+=1
    return False

def makeStar():  # 유성 랜덤으로 떨어지게 설정
    if timeDelay():
        idex=random.randint(0,len(star)-1)
        if recStar[idex].y==-1:
            recStar[idex].x=random.randint(0, SCREEN_WIDTH)
            recStar[idex].y=0


def moveStar():
    makeStar()
    for i in range(len(star)):
        if recStar[i].y==-1:
            continue

        recStar[i].y += 1
        if recStar[i].y > SCREEN_HEIGHT:
            recStar[i].y = 0

        SCREEN.blit(star[i], recStar[i])


def CheckCollision():  # 충돌 확인 기능
    for rec in recStar:
        if rec.y==-1:
            continue
        if rec.top<recPlayer.bottom and recPlayer.top<rec.bottom and rec.left<recPlayer.right and recPlayer.left<rec.right:
            print('충돌')
            break


# 1. 변수 초기화
isActive = True
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
move = Rect(0, 0, 0, 0)
time_delay=0

# 2. 스크린 설정
pygame.init()  # gygame 라이브러리를 제일 처음 사용하기 위한 동작
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 스크린 크기 설정
pygame.display.set_caption("CodingNow!")

# 3. player 생성
player = pygame.image.load('player.png')
player = pygame.transform.scale(player, (20, 30))  # 로켓 크기 설정
recPlayer = player.get_rect()
recPlayer.centerx = (SCREEN_WIDTH / 2)
recPlayer.centery = (SCREEN_HEIGHT / 2)

# 4. 유성 생성
star = [pygame.image.load('star.png') for i in range(40)]  # 유성 개수 설정
recStar = [None for i in range(len(star))]
for i in range(len(star)):
    star[i] = pygame.transform.scale(star[i], (20, 20))  # 유성 크기 설정
    recStar[i] = player.get_rect()
    recStar[i].y=-1

# 5. 기타
clock = pygame.time.Clock()  # 객체에 시간을 줌

#### 반복 ####
while isActive:
    # 1. 화면 지움
    SCREEN.fill((0, 0, 0))  # 로켓 잔상 제거 (스크린을 검정색으로 칠함)
    # 2. 이벤트 처리
    eventProcess()
    # 3. 플레이어 이동
    movePlayer()
    # 4. 유성 생성 및 이동
    moveStar()
    # 5. 충돌 확인
    CheckCollision()
    # 6. text 업데이트
    # 7. 화면 경신
    pygame.display.flip()
    clock.tick(100)  # 로켓 동작 시간 느리게
#### 반복 ####
