import math
try:
    import pygame
except ImportError:
    import pygame_ce as pygame

Color = tuple


def plot(surface: pygame.Surface, x: int, y: int, color: Color):
    if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
        surface.set_at((x, y), color)


def dda_line(surface: pygame.Surface, x0: int, y0: int, x1: int, y1: int, color: Color):
    dx = x1 - x0
    dy = y1 - y0
    steps = int(max(abs(dx), abs(dy)))
    if steps == 0:
        plot(surface, x0, y0, color)
        return
    x_inc = dx / steps
    y_inc = dy / steps
    x = x0
    y = y0
    for _ in range(steps + 1):
        plot(surface, int(round(x)), int(round(y)), color)
        x += x_inc
        y += y_inc


def bresenham_line_low(surface: pygame.Surface, x0: int, y0: int, x1: int, y1: int, color: Color):
    # Assumes |m| < 1, steps in x
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    d = 2 * abs(dy) - dx
    y_step = 1 if dy >= 0 else -1
    y = y0
    x = x0
    for _ in range(dx + 1):
        plot(surface, x, y, color)
        if d > 0:
            y += y_step
            d -= 2 * dx
        d += 2 * abs(dy)
        x += xi


def bresenham_line_high(surface: pygame.Surface, x0: int, y0: int, x1: int, y1: int, color: Color):
    # Assumes |m| >= 1, steps in y
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    d = 2 * abs(dx) - dy
    x_step = 1 if dx >= 0 else -1
    x = x0
    y = y0
    for _ in range(dy + 1):
        plot(surface, x, y, color)
        if d > 0:
            x += x_step
            d -= 2 * dy
        d += 2 * abs(dx)
        y += yi


def bresenham_line(surface: pygame.Surface, x0: int, y0: int, x1: int, y1: int, color: Color):
    # Route to low/high based on slope magnitude
    if x0 == x1:
        # vertical line
        y_start, y_end = (y0, y1) if y0 <= y1 else (y1, y0)
        for y in range(y_start, y_end + 1):
            plot(surface, x0, y, color)
        return
    m = (y1 - y0) / (x1 - x0)
    if abs(m) < 1:
        bresenham_line_low(surface, x0, y0, x1, y1, color)
    else:
        bresenham_line_high(surface, x0, y0, x1, y1, color)


def _circle_symmetry(surface: pygame.Surface, xc: int, yc: int, x: int, y: int, color: Color):
    plot(surface, xc + x, yc + y, color)
    plot(surface, xc - x, yc + y, color)
    plot(surface, xc + x, yc - y, color)
    plot(surface, xc - x, yc - y, color)
    plot(surface, xc + y, yc + x, color)
    plot(surface, xc - y, yc + x, color)
    plot(surface, xc + y, yc - x, color)
    plot(surface, xc - y, yc - x, color)


def midpoint_circle(surface: pygame.Surface, xc: int, yc: int, r: int, color: Color):
    x = 0
    y = r
    d = 1 - r
    _circle_symmetry(surface, xc, yc, x, y, color)
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        _circle_symmetry(surface, xc, yc, x, y, color)


def _ellipse_symmetry(surface: pygame.Surface, xc: int, yc: int, x: int, y: int, color: Color):
    plot(surface, xc + x, yc + y, color)
    plot(surface, xc - x, yc + y, color)
    plot(surface, xc + x, yc - y, color)
    plot(surface, xc - x, yc - y, color)


def midpoint_ellipse(surface: pygame.Surface, xc: int, yc: int, rx: int, ry: int, color: Color):
    # Region 1
    x = 0
    y = ry
    rx2 = rx * rx
    ry2 = ry * ry
    dx = 2 * ry2 * x
    dy = 2 * rx2 * y
    d1 = ry2 - rx2 * ry + 0.25 * rx2
    _ellipse_symmetry(surface, xc, yc, x, y, color)
    while dx < dy:
        if d1 < 0:
            x += 1
            dx += 2 * ry2
            d1 += dx + ry2
        else:
            x += 1
            y -= 1
            dx += 2 * ry2
            dy -= 2 * rx2
            d1 += dx - dy + ry2
        _ellipse_symmetry(surface, xc, yc, x, y, color)

    # Region 2
    d2 = ry2 * ((x + 0.5) ** 2) + rx2 * ((y - 1) ** 2) - rx2 * ry2
    while y >= 0:
        _ellipse_symmetry(surface, xc, yc, x, y, color)
        if d2 > 0:
            y -= 1
            dy -= 2 * rx2
            d2 += rx2 - dy
        else:
            y -= 1
            x += 1
            dx += 2 * ry2
            dy -= 2 * rx2
            d2 += dx - dy + rx2


def draw_axes(surface: pygame.Surface, rect: pygame.Rect, color: Color = (180, 180, 180)):
    # draw x and y axes through the rect
    # x-axis
    bresenham_line(surface, rect.left, rect.centery, rect.right, rect.centery, color)
    # y-axis
    bresenham_line(surface, rect.centerx, rect.top, rect.centerx, rect.bottom, color)
