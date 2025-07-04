import pygame
import sys
import random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 640, 720
BOARD_SIZE = 10
CELL_SIZE = 60
TOP_OFFSET = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakes and Ladders")
font = pygame.font.SysFont("dejavusans", 24)

# Snakes and ladders configuration
snakes = {
    16: 6,
    47: 26,
    49: 11,
    56: 53,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    98: 78,
}
ladders = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    80: 100,
}

# Colors for up to four players
PLAYER_COLORS = [
    (255, 0, 0),      # red
    (0, 0, 255),      # blue
    (0, 200, 0),      # green
    (255, 165, 0),    # orange
]

class Player:
    def __init__(self, index):
        self.index = index
        self.pos = 1
        self.color = PLAYER_COLORS[index]

class Game:
    def __init__(self, player_count):
        self.players = [Player(i) for i in range(player_count)]
        self.turn = 0
        self.winner = None

    def roll_dice(self):
        return random.randint(1, 6)

    def move_player(self, player, steps):
        start = player.pos
        end = start + steps
        if end > 100:
            end = 100 - (end - 100)
        if end in snakes:
            end = snakes[end]
        elif end in ladders:
            end = ladders[end]
        player.pos = end
        if end == 100:
            self.winner = player

    def next_turn(self, rolled):
        if rolled != 6:
            self.turn = (self.turn + 1) % len(self.players)

# Board drawing utilities

def index_to_coord(index):
    row = (index - 1) // BOARD_SIZE
    col = (index - 1) % BOARD_SIZE
    if row % 2 == 1:
        col = BOARD_SIZE - 1 - col
    x = col * CELL_SIZE
    y = HEIGHT - CELL_SIZE * (row + 1) - (HEIGHT - BOARD_SIZE * CELL_SIZE - TOP_OFFSET)
    return x + CELL_SIZE // 2, y + CELL_SIZE // 2

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * CELL_SIZE
            y = TOP_OFFSET + (BOARD_SIZE - 1 - row) * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            color = (235, 235, 235) if (row + col) % 2 == 0 else (200, 200, 200)
            pygame.draw.rect(screen, color, rect)
            num = row * BOARD_SIZE + (col if row % 2 == 0 else BOARD_SIZE - 1 - col) + 1
            text = font.render(str(num), True, (0, 0, 0))
            screen.blit(text, (x + 5, y + 5))

def draw_players(players):
    for p in players:
        x, y = index_to_coord(p.pos)
        pygame.draw.circle(screen, p.color, (x, y), 20)

def draw_border(color):
    pygame.draw.rect(screen, color, pygame.Rect(0, 0, WIDTH, HEIGHT), 10)

# Menu helpers

def menu_screen():
    clock = pygame.time.Clock()
    single_rect = pygame.Rect(220, 200, 200, 60)
    multi_rect = pygame.Rect(220, 300, 200, 60)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_rect.collidepoint(event.pos):
                    return 1
                if multi_rect.collidepoint(event.pos):
                    return select_players()
        screen.fill((255, 255, 255))
        title = font.render("Snakes and Ladders", True, (0, 0, 0))
        screen.blit(title, (180, 100))
        pygame.draw.rect(screen, (180, 180, 180), single_rect)
        pygame.draw.rect(screen, (180, 180, 180), multi_rect)
        single_text = font.render("Single Play", True, (0, 0, 0))
        multi_text = font.render("Multiplayer", True, (0, 0, 0))
        screen.blit(single_text, (single_rect.x + 40, single_rect.y + 15))
        screen.blit(multi_text, (multi_rect.x + 40, multi_rect.y + 15))
        pygame.display.flip()
        clock.tick(30)

def select_players():
    clock = pygame.time.Clock()
    buttons = [pygame.Rect(170 + i * 100, 300, 60, 60) for i in range(3)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, b in enumerate(buttons):
                    if b.collidepoint(event.pos):
                        return i + 2
        screen.fill((255, 255, 255))
        prompt = font.render("How many players?", True, (0, 0, 0))
        screen.blit(prompt, (200, 200))
        for i, b in enumerate(buttons):
            pygame.draw.rect(screen, (180, 180, 180), b)
            txt = font.render(str(i + 2), True, (0, 0, 0))
            screen.blit(txt, (b.x + 20, b.y + 15))
        pygame.display.flip()
        clock.tick(30)

# Main game loop
def main():
    player_count = menu_screen()
    game = Game(player_count)
    dice_result = 0
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game.winner:
                dice_result = game.roll_dice()
                player = game.players[game.turn]
                game.move_player(player, dice_result)
                game.next_turn(dice_result)
        screen.fill((255, 255, 255))
        draw_board()
        draw_players(game.players)
        active_player = game.players[game.turn]
        draw_border(active_player.color)
        status = f"Player {game.turn + 1}'s turn"
        if dice_result:
            status += f" - Rolled {dice_result}"
        status_text = font.render(status, True, (0, 0, 0))
        screen.blit(status_text, (20, 20))
        if game.winner:
            win_text = font.render(f"Player {game.winner.index + 1} wins!", True, (0,0,0))
            screen.blit(win_text, (220, 60))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
