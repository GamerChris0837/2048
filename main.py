import pygame
import random


pygame.init()

WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 30
font = pygame.font.Font('KoPub Dotum Bold.ttf', 24)
icon = pygame.image.load('icon1.jpg')
pygame.display.set_icon(icon)

colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high

def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('게임 오버!', True, 'white')
    game_over_text2 = font.render('Enter키를 눌러 재시작하세요', True, 'white')
    screen.blit(game_over_text1, (155, 65))
    screen.blit(game_over_text2, (60, 105))

def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                s = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            s += 1
                    if s > 0:
                        board[i - s][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - s - 1][j] == board[i - s][j] and not merged[i - s][j] \
                            and not merged[i - s - 1][j]:
                        board[i - s - 1][j] *= 2
                        score += board[i - s - 1][j]
                        board[i - s][j] = 0
                        merged[i - s - 1][j] = True

    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                s = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        s += 1
                if s > 0:
                    board[2 - i + s][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + s <= 3:
                    if board[2 - i + s][j] == board[3 - i + s][j] and not merged[3 - i + s][j] \
                            and not merged[2 - i + s][j]:
                        board[3 - i + s][j] *= 2
                        score += board[3 - i + s][j]
                        board[2 - i + s][j] = 0
                        merged[3 - i + s][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                s = 0
                for q in range(j):
                    if board[i][q] == 0:
                        s += 1
                if s > 0:
                    board[i][j - s] = board[i][j]
                    board[i][j] = 0
                if board[i][j - s] == board[i][j - s - 1] and not merged[i][j - s - 1] \
                        and not merged[i][j - s]:
                    board[i][j - s - 1] *= 2
                    score += board[i][j - s - 1]
                    board[i][j - s] = 0
                    merged[i][j - s - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                s = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        s += 1
                if s > 0:
                    board[i][3 - j + s] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + s <= 3:
                    if board[i][4 - j + s] == board[i][3 - j + s] and not merged[i][4 - j + s] \
                            and not merged[i][3 - j + s]:
                        board[i][4 - j + s] *= 2
                        score += board[i][4 - j + s]
                        board[i][3 - j + s] = 0
                        merged[i][4 - j + s] = True
    return board

def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'점수: {score}', True, 'black')
    high_score_text = font.render(f'최고 점수: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    pass

def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('KoPub Dotum Bold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    if score >= high_score:
        high_score = score

    pygame.display.flip()
pygame.quit()