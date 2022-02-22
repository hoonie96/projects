#########################
#  Use this template to pactice
#########################
import os
import pygame

###################################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Pang")

# FPS
clock = pygame.time.Clock()
###################################################################################################

# 1. 사죵자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰드 등)
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # join 을 해서 current_path에 images 폴더를 더해서 images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 0 은 width, 1 은 height. 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0] # width 만 필요한 이유는 캐릭터 중앙에서 나오기 때문에 /2 를 해야되서

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10


running = True
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed # 캐릭터를 왼쪽으로
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed # 캐릭터를 오른쪽으로
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                # 무기의 x위치는 캐릭터의 위치에서 캐릭터 사이즈 반(캐릭터 중앙) 에 무기의 반(무기 중앙) 를 뺀 값
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos]) # 무기를 여러번 쏘면 좌표 값들이 list 안에 들어감

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0


    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    # 100, 200 -> 180, 160, 140, ...
    # 500, 200 -> 180, 160, 140, ...
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로
    # weapon 에 있는 list 값 들을 하나씩 불러와서 w 라고 하고 w 에 있는 값 들을 통해서 어떤 처리를 함
    # 그 처리 한것들을 다시 weapons 안에 넣는 작업
    # w 는 (weapon_x_pos, weapon_y_pos) 를 갖는 list
    # [w[0] - weapon_speed, w[1] - weapon_speed 값을  엮어서 또 다른 하나의 list [weapons] 로 감싸는 것

    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
    # y 좌표가 화면 위를 닿지 않은 것에서만 다시 list 만들기
    # y 좌표가 화면 위를 벗어나면 사라지는 것과 같은 결과

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))


    pygame.display.update()


pygame.quit()
