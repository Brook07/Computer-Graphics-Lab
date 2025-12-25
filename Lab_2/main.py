import sys
try:
    import pygame
except ImportError:
    import pygame_ce as pygame
from pygame.locals import QUIT, KEYDOWN

from src.draw import dda_line, bresenham_line, midpoint_circle, midpoint_ellipse, draw_axes
from src.charts import line_graph, pie_chart

W, H = 900, 700
BG = (245, 245, 245)
FG = (20, 20, 20)
RED = (220, 60, 60)
GREEN = (60, 180, 75)
BLUE = (60, 60, 220)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 153, 215)

HELP_TEXT = [
    "1: DDA Line",
    "2: Bresenham Line",
    "3: Midpoint Circle",
    "4: Midpoint Ellipse",
    "5: Line Graph (A toggles algo)",
    "6: Pie Chart",
    "H: Toggle Help",
    "Q / ESC: Quit",
]


def draw_text(surface, text, pos, color=FG, size=18):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, True, color)
    surface.blit(img, pos)


def demo_dda(surface):
    draw_text(surface, "DDA Line Drawing", (20, 20), BLUE, 24)
    # examples
    dda_line(surface, 100, 100, 800, 120, RED)
    dda_line(surface, 120, 160, 760, 500, GREEN)
    dda_line(surface, 400, 100, 420, 600, BLUE)


def demo_bresenham(surface):
    draw_text(surface, "Bresenham Line Drawing (both slopes)", (20, 20), BLUE, 24)
    # |m| < 1
    bresenham_line(surface, 100, 120, 800, 200, RED)
    bresenham_line(surface, 150, 300, 850, 330, GREEN)
    # |m| >= 1
    bresenham_line(surface, 120, 160, 200, 650, BLUE)
    bresenham_line(surface, 800, 600, 200, 100, ORANGE)


def demo_circle(surface):
    draw_text(surface, "Midpoint Circle Drawing", (20, 20), BLUE, 24)
    midpoint_circle(surface, W // 2, H // 2, 200, FG)
    midpoint_circle(surface, W // 2, H // 2, 120, CYAN)
    midpoint_circle(surface, W // 2, H // 2, 60, ORANGE)


def demo_ellipse(surface):
    draw_text(surface, "Midpoint Ellipse Drawing", (20, 20), BLUE, 24)
    midpoint_ellipse(surface, W // 2, H // 2, 280, 160, FG)
    midpoint_ellipse(surface, W // 2, H // 2, 200, 120, CYAN)
    midpoint_ellipse(surface, W // 2, H // 2, 120, 60, ORANGE)


def demo_line_graph(surface, algo_state):
    draw_text(surface, f"Line Graph ({algo_state.upper()})", (20, 20), BLUE, 24)
    rect = pygame.Rect(80, 100, W - 160, H - 200)
    pygame.draw.rect(surface, (220, 220, 220), rect, 1)
    draw_axes(surface, rect)
    data = [12, 18, 5, 9, 14, 26, 17, 30, 22, 28, 33, 21]
    line_graph(surface, data, rect, RED, algo=algo_state)


def demo_pie_chart(surface):
    draw_text(surface, "Pie Chart", (20, 20), BLUE, 24)
    rect = pygame.Rect(150, 120, 600, 460)
    pygame.draw.rect(surface, (220, 220, 220), rect, 1)
    values = [40, 25, 15, 10, 10]
    colors = [RED, GREEN, BLUE, ORANGE, PURPLE]
    pie_chart(surface, values, rect, colors)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Computer Graphics Lab 2")
    clock = pygame.time.Clock()

    mode = 1
    show_help = True
    algo_state = "dda"  # for line graph

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                key = event.key
                if key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif key == pygame.K_1:
                    mode = 1
                elif key == pygame.K_2:
                    mode = 2
                elif key == pygame.K_3:
                    mode = 3
                elif key == pygame.K_4:
                    mode = 4
                elif key == pygame.K_5:
                    mode = 5
                elif key == pygame.K_6:
                    mode = 6
                elif key == pygame.K_h:
                    show_help = not show_help
                elif key == pygame.K_a and mode == 5:
                    algo_state = "bresenham" if algo_state == "dda" else "dda"

        screen.fill(BG)
        if mode == 1:
            demo_dda(screen)
        elif mode == 2:
            demo_bresenham(screen)
        elif mode == 3:
            demo_circle(screen)
        elif mode == 4:
            demo_ellipse(screen)
        elif mode == 5:
            demo_line_graph(screen, algo_state)
        elif mode == 6:
            demo_pie_chart(screen)

        if show_help:
            y = 10
            for line in HELP_TEXT:
                draw_text(screen, line, (W - 300, y), (100, 100, 100), 18)
                y += 22

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
