import pygame
import sys
import random
from pygame.locals import *

# 초기화
pygame.init()

# 음향 효과 로드
brick_sound = pygame.mixer.Sound('sound/brick_hit.wav')  # 벽돌에 공이 맞을 때 재생될 소리
paddle_sound = pygame.mixer.Sound('sound/paddle_hit.wav')  # 패들에 공이 맞을 때 재생될 소리
win_sound = pygame.mixer.Sound('sound/win_sound.wav')  # 모든 벽돌을 깼을 때 재생될 소리

font = pygame.font.SysFont('malgungothic', 55)  # '맑은 고딕'을 선택하여 한글을 표시합니다.

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE, (255, 255, 0), (255, 165, 0), (128, 0, 128)]  # 벽돌 색상 리스트

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 게임 화면 생성
pygame.display.set_caption("벽돌깨기 게임")  # 창 제목 설정

# 패들 설정
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)  # 패들의 위치와 크기 설정
paddle_speed = 6  # 패들의 이동 속도

# 공 설정
BALL_RADIUS = 10
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)  # 공의 위치와 크기 설정
ball_speed = [4, -4]  # 공의 초기 속도 (x, y)

# 벽돌 설정 함수
def create_bricks():
    bricks = []
    brick_color = random.choice(COLORS)  # 벽돌의 색상을 랜덤으로 선택
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            brick_x = col * (BRICK_WIDTH + BRICK_SPACING) + BRICK_SPACING // 2
            brick_y = row * (BRICK_HEIGHT + BRICK_SPACING) + BRICK_SPACING // 2
            brick = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)  # 벽돌의 위치와 크기 설정
            bricks.append((brick, brick_color))  # 벽돌과 그 색상을 리스트에 추가
    print("Bricks created with color: {}".format(brick_color))  # 벽돌 생성 로그
    return bricks

BRICK_ROWS = 4  # 벽돌의 행 개수
BRICK_COLUMNS = 10  # 벽돌의 열 개수
BRICK_SPACING = 5  # 벽돌 사이의 간격
BRICK_WIDTH = (WIDTH - (BRICK_COLUMNS + 1) * BRICK_SPACING) // BRICK_COLUMNS  # 벽돌의 너비 계산
BRICK_HEIGHT = 30  # 벽돌의 높이
bricks = create_bricks()  # 초기 벽돌 생성

# 게임 루프
clock = pygame.time.Clock()  # 게임 속도 조절을 위한 Clock 객체 생성
paused = False  # 일시 정지 상태 여부

while True:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:  # 종료 이벤트가 발생하면 게임 종료
            print("Game quit event detected.")  # 게임 종료 이벤트 로그
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:  # 방향키 '상' 입력 시 일시 정지
                paused = True
                print("Game paused.")  # 게임 일시 정지 로그
                text = font.render("Paused!!", True, WHITE)  # 일시정지
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))  # 화면 중앙에 메시지 출력
                pygame.display.flip()  # 화면 업데이트
            elif event.key == K_DOWN:  # 방향키 '하' 입력 시 다시 재생
                paused = False
                print("Game resumed.")  # 게임 재개 로그
                text = font.render("Restart", True, WHITE)  # 다시재생
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))  # 화면 중앙에 메시지 출력
                pygame.display.flip()  # 화면 업데이트
                
    if paused:
        continue

    # 패들 움직임
    keys = pygame.key.get_pressed()  # 키 입력 상태를 가져옴
    if keys[K_LEFT] and paddle.left > 0:  # 왼쪽 화살표 키가 눌리고 패들이 화면을 벗어나지 않으면
        paddle.move_ip(-paddle_speed, 0)  # 패들을 왼쪽으로 이동
        print("Paddle moved left to position: {}".format(paddle.left))  # 패들 이동 로그
    if keys[K_RIGHT] and paddle.right < WIDTH:  # 오른쪽 화살표 키가 눌리고 패들이 화면을 벗어나지 않으면
        paddle.move_ip(paddle_speed, 0)  # 패들을 오른쪽으로 이동
        print("Paddle moved right to position: {}".format(paddle.right))  # 패들 이동 로그

    # 공 움직임
    ball.left += ball_speed[0]  # 공의 x축 위치 업데이트
    ball.top += ball_speed[1]  # 공의 y축 위치 업데이트
    print("Ball position updated to: ({}, {})".format(ball.left, ball.top))  # 공 위치 업데이트 로그

    # 공의 벽 충돌
    if ball.left <= 0 or ball.right >= WIDTH:  # 공이 왼쪽 또는 오른쪽 벽에 부딪히면
        ball_speed[0] = -ball_speed[0]  # x축 속도를 반대로 변경
        print("Ball hit side wall. New speed: {}".format(ball_speed))  # 벽 충돌 로그
    if ball.top <= 0 or ball.bottom >= HEIGHT:  # 공이 위쪽 또는 아래쪽 벽에 부딪히면
        ball_speed[1] = -ball_speed[1]  # y축 속도를 반대로 변경
        print("Ball hit top/bottom wall. New speed: {}".format(ball_speed))  # 벽 충돌 로그

    # 공과 패들의 충돌
    if ball.colliderect(paddle):  # 공이 패들과 충돌하면
        ball_speed[1] = -ball_speed[1]  # y축 속도를 반대로 변경
        paddle_sound.play()  # 패들 충돌 소리 재생
        print("Ball hit paddle. New speed: {}".format(ball_speed))  # 패들 충돌 로그

    # 공과 벽돌의 충돌
    for brick, color in bricks[:]:  # 모든 벽돌에 대해 반복
        if ball.colliderect(brick):  # 공이 벽돌과 충돌하면
            bricks.remove((brick, color))  # 해당 벽돌을 리스트에서 제거
            ball_speed[1] = -ball_speed[1]  # y축 속도를 반대로 변경
            brick_sound.play()  # 벽돌 충돌 소리 재생
            print("Ball hit brick at position: ({}, {}). Brick removed.".format(brick.left, brick.top))  # 벽돌 충돌 로그
            break

    # 벽돌이 모두 깨졌을 때
    if not bricks:  # 벽돌 리스트가 비어 있으면 (모든 벽돌이 깨졌을 때)
        win_sound.play()  # 승리 소리 재생
        font = pygame.font.SysFont(None, 55)  # 폰트 설정
        text = font.render("Nice. Finished!", True, WHITE)  # 축하 메시지 렌더링
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))  # 화면 중앙에 메시지 출력
        pygame.display.flip()  # 화면 업데이트
        print("All bricks cleared. Displaying win message.")  # 모든 벽돌 제거 로그
        pygame.time.wait(2000)  # 2초 대기
        bricks = create_bricks()  # 새로운 벽돌 생성
        ball.left, ball.top = WIDTH // 2, HEIGHT // 2  # 공을 초기 위치로 설정
        ball_speed = [4, -4]  # 공의 속도 초기화
        print("New bricks created. Ball reset to initial position.")  # 새로운 게임 시작 로그

    # 화면 그리기
    screen.fill(BLACK)  # 화면을 검정색으로 채움
    pygame.draw.rect(screen, BLUE, paddle)  # 패들을 화면에 그림
    pygame.draw.ellipse(screen, WHITE, ball)  # 공을 화면에 그림
    for brick, color in bricks:  # 모든 벽돌에 대해 반복
        pygame.draw.rect(screen, color, brick)  # 벽돌을 화면에 그림

    pygame.display.flip()  # 화면 업데이트
    clock.tick(60)  # 초당 60프레임으로 설정