import pygame
import math

pygame.init()

# Paramètres
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 16, 16
CELL_SIZE = WIDTH // COLS
RADIUS = 10

# Couleurs
WHITE = (255, 255, 255)
GRID_COLOR = (30, 30, 30)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

# Setup Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grille Pygame avec Barrières Permanentes")

points = {}
current_player = "red"

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_points():
    for (row, col), color in points.items():
        cx = col * CELL_SIZE
        cy = row * CELL_SIZE
        pygame.draw.circle(screen, RED if color == "red" else BLUE, (cx, cy), 6)

def get_closest_intersection(pos):
    mx, my = pos
    for row in range(ROWS):
        for col in range(COLS):
            cx = col * CELL_SIZE
            cy = row * CELL_SIZE
            distance = math.hypot(mx - cx, my - cy)
            if distance <= RADIUS:
                return (row, col)
    return None

# Boucle principale
running = True
while running:
    screen.fill(WHITE)
    draw_grid()
    draw_points()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            intersection = get_closest_intersection(pos)

            if intersection and intersection not in points:
                points[intersection] = current_player
                current_player = "blue" if current_player == "red" else "red"
            else:
                print("Intersection déjà occupée ou hors limite.")
                
    pygame.display.flip()

pygame.quit()
