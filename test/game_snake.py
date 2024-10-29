import os
import pygame
import time
import random

# 사용할 오디오 드라이버 설정 ('winmm', 'directsound', 'dummy' 등)
os.environ['SDL_AUDIODRIVER'] = 'winmm'  # 또는 'dummy'로 변경하여 오디오 비활성화

pygame.init()

# 소리 초기화
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"오디오 초기화에 실패했습니다: {e}")
    pygame.mixer = None  # mixer 사용 불가 상태로 설정

# 화면 설정 (확대된 화면 크기)
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("개선된 뱀 게임 with 이미지, 소리 및 점수 표시")

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)          # 음식 색상
green = (0, 255, 0)        # 뱀 머리 색상
dark_green = (0, 200, 0)   # 뱀 몸통 색상
blue = (0, 0, 255)         # 일시정지 메시지 색상

# 뱀 설정
snake_block = 20  # 크기 조정
snake_speed = 12

clock = pygame.time.Clock()

# 한글 폰트 설정 (크기 조정: font_style=25, pause_font=25, score_font=25)
try:
    font_style = pygame.font.SysFont('Malgun Gothic', 25)
    pause_font = pygame.font.SysFont('Malgun Gothic', 25)
    score_font = pygame.font.SysFont('Malgun Gothic', 25)
except:
    font_style = pygame.font.Font(None, 25)
    pause_font = pygame.font.Font(None, 25)
    score_font = pygame.font.Font(None, 25)

def message(msg, color, font, position):
    mesg = font.render(msg, True, color)
    win.blit(mesg, position)

def Your_score(score):
    value = score_font.render("점수: " + str(score), True, white)
    win.blit(value, [10, 10])  # 화면 왼쪽 상단에 점수 표시

def load_image(name, size):
    try:
        image = pygame.image.load(os.path.join("images", name))  # 'images' 폴더 내에서 로드
        image = pygame.transform.scale(image, size)
        return image
    except pygame.error:
        print(f"이미지를 로드할 수 없습니다: {name}")
        return None

# 소리 파일 로드 (sound 폴더 내)
def load_sound(name):
    if pygame.mixer:
        path = os.path.join("sound", name)
        try:
            sound = pygame.mixer.Sound(path)
            return sound
        except pygame.error:
            print(f"소리 파일을 로드할 수 없습니다: {path}")
            return None
    else:
        return None

eat_sound = load_sound('eat.wav')
game_over_sound = load_sound('game_over.wav')
pause_sound = load_sound('pause.wav')
resume_sound = load_sound('resume.wav')

# 배경 음악 로드 및 재생 (선택 사항)
def load_music(name):
    if pygame.mixer:
        path = os.path.join("sound", name)
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(1.0)  # 볼륨 조절 (0.0 ~ 1.0)
            pygame.mixer.music.play(-1)  # 무한 반복 재생
        except pygame.error:
            print(f"배경 음악을 로드할 수 없습니다: {path}")

load_music('background_music.mp3')  # 배경 음악 파일명

# 이미지 로드
heart_image = load_image('heart.png', (30, 30))
star_image = load_image('star.png', (30, 30))
effect_images = [heart_image, star_image]
current_effect_image = None
effect_position = (0, 0)
effect_start_time = 0
effect_duration = 1000  # 밀리초 단위 (1초)

def gameLoop():
    global current_effect_image, effect_position, effect_start_time

    game_over = False
    game_close = False
    paused = False  # 일시정지 상태 변수
    game_over_sound_played = False  # 게임 오버 소리 재생 여부

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    score = 0  # 점수 변수 추가

    # 음식 초기 위치 설정
    foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block

    # 효과 이미지 선택을 위한 인덱스
    effect_index = 0

    while not game_over:

        while game_close:
            win.fill(black)
            message("게임 종료! Q-종료 또는 C-재시작", red, font_style, [width / 6, height / 3])
            Your_score(score)  # 점수 표시
            pygame.display.update()

            # 게임 오버 소리 한 번만 재생
            if game_over_sound and not game_over_sound_played:
                game_over_sound.play()
                game_over_sound_played = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        # 게임을 재시작하기 전에 모든 변수 초기화
                        game_over_sound_played = False
                        x1 = width / 2
                        y1 = height / 2
                        x1_change = 0
                        y1_change = 0
                        snake_List = []
                        Length_of_snake = 1
                        score = 0
                        foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
                        foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
                        effect_index = 0
                        current_effect_image = None
                        effect_position = (0, 0)
                        effect_start_time = 0
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:  # P 키로 일시정지 기능 추가
                    paused = not paused
                    if paused:
                        # 일시정지 시 소리 재생
                        if pause_sound:
                            pause_sound.play()
                    else:
                        # 재개 시 소리 재생
                        if resume_sound:
                            resume_sound.play()
                    while paused:
                        win.fill(black)
                        message("일시정지 - P: 재개, R: 재시작, Q: 종료", blue, pause_font, [width / 6, height / 3])
                        Your_score(score)  # 일시정지 중에도 점수 표시
                        pygame.display.update()
                        for pause_event in pygame.event.get():
                            if pause_event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if pause_event.type == pygame.KEYDOWN:
                                if pause_event.key == pygame.K_p:
                                    paused = False
                                    # 재개 시 소리 재생
                                    if resume_sound:
                                        resume_sound.play()
                                elif pause_event.key == pygame.K_r:
                                    # 게임을 재시작하기 전에 모든 변수 초기화
                                    game_over_sound_played = False
                                    x1 = width / 2
                                    y1 = height / 2
                                    x1_change = 0
                                    y1_change = 0
                                    snake_List = []
                                    Length_of_snake = 1
                                    score = 0
                                    foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
                                    foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
                                    effect_index = 0
                                    current_effect_image = None
                                    effect_position = (0, 0)
                                    effect_start_time = 0
                                    paused = False
                                elif pause_event.key == pygame.K_q:
                                    pygame.quit()
                                    quit()

        # 뱀이 화면을 벗어나면 게임 종료
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        win.fill(black)

        # 음식 그리기 (빨간색 원)
        pygame.draw.circle(win, red, (int(foodx) + snake_block // 2, int(foody) + snake_block // 2), snake_block // 2)

        # 뱀 그리기
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 뱀이 자기 자신과 충돌하면 게임 종료
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 뱀의 각 부분을 그리기
        for index, segment in enumerate(snake_List):
            center = (int(segment[0]) + snake_block // 2, int(segment[1]) + snake_block // 2)
            if index == len(snake_List) - 1:
                # 머리는 밝은 초록색
                pygame.draw.circle(win, green, center, snake_block // 2)
                # 간단한 눈 추가
                eye_radius = 3
                eye_x_offset = 5
                eye_y_offset = 5
                pygame.draw.circle(win, black, (center[0] - eye_x_offset, center[1] - eye_y_offset), eye_radius)
                pygame.draw.circle(win, black, (center[0] + eye_x_offset, center[1] - eye_y_offset), eye_radius)
            else:
                # 몸통은 어두운 초록색
                pygame.draw.circle(win, dark_green, center, snake_block // 2)

        # 점수 표시
        Your_score(score)

        # 효과 이미지 표시
        current_time = pygame.time.get_ticks()
        if current_effect_image and current_time - effect_start_time < effect_duration:
            win.blit(current_effect_image, (effect_position[0], effect_position[1]))
        elif current_effect_image and current_time - effect_start_time >= effect_duration:
            # 효과 시간 초과 시 이미지 제거
            current_effect_image = None

        pygame.display.update()

        # 음식 먹었을 때
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            score += 10  # 점수 증가

            # 음식 먹었을 때 소리 재생
            if eat_sound:
                eat_sound.play()

            # 효과 이미지 설정
            if effect_images[effect_index]:
                current_effect_image = effect_images[effect_index]
                effect_position = (foodx, foody)
                effect_start_time = pygame.time.get_ticks()
                # 다음 효과 이미지로 변경
                effect_index = (effect_index + 1) % len(effect_images)
            else:
                current_effect_image = None

        clock.tick(snake_speed)

    # 게임 종료 시 배경 음악 중지
    if pygame.mixer and pygame.mixer.music:
        pygame.mixer.music.stop()
    pygame.quit()
    quit()

gameLoop()
