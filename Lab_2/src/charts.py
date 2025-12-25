import math
try:
    import pygame
except ImportError:
    import pygame_ce as pygame
from typing import List, Tuple

from .draw import dda_line, bresenham_line, midpoint_circle

Color = Tuple[int, int, int]


def line_graph(surface: pygame.Surface, data: List[float], rect: pygame.Rect, color: Color, algo: str = "dda"):
    if not data:
        return
    n = len(data)
    min_val = min(data)
    max_val = max(data)
    span = max(max_val - min_val, 1e-6)

    def to_point(i: int, v: float) -> Tuple[int, int]:
        x = rect.left + int(i * (rect.width - 1) / (n - 1))
        # invert y for screen
        y = rect.top + rect.height - 1 - int((v - min_val) / span * (rect.height - 1))
        return x, y

    points = [to_point(i, v) for i, v in enumerate(data)]
    for i in range(n - 1):
        (x0, y0), (x1, y1) = points[i], points[i + 1]
        if algo.lower().startswith("bres"):
            bresenham_line(surface, x0, y0, x1, y1, color)
        else:
            dda_line(surface, x0, y0, x1, y1, color)


def pie_chart(surface: pygame.Surface, values: List[float], rect: pygame.Rect, colors: List[Color]):
    total = sum(values) if values else 0.0
    if total <= 0:
        return

    cx = rect.centerx
    cy = rect.centery
    radius = min(rect.width, rect.height) // 2 - 4

    # outline circle
    midpoint_circle(surface, cx, cy, radius, (150, 150, 150))

    start_angle = 0.0
    two_pi = 2.0 * math.pi

    for idx, val in enumerate(values):
        frac = val / total
        sweep = frac * two_pi
        end_angle = start_angle + sweep
        color = colors[idx % len(colors)]

        # Build polygon points approximating the sector
        points = [(cx, cy)]
        steps = max(12, int(sweep * radius / 6))  # dynamic tessellation
        for k in range(steps + 1):
            theta = start_angle + k * sweep / steps
            x = cx + int(radius * math.cos(theta))
            y = cy + int(radius * math.sin(theta))
            points.append((x, y))

        pygame.draw.polygon(surface, color, points)

        # draw boundary lines using our line algorithms
        x_s = cx + int(radius * math.cos(start_angle))
        y_s = cy + int(radius * math.sin(start_angle))
        x_e = cx + int(radius * math.cos(end_angle))
        y_e = cy + int(radius * math.sin(end_angle))
        bresenham_line(surface, cx, cy, x_s, y_s, (30, 30, 30))
        bresenham_line(surface, cx, cy, x_e, y_e, (30, 30, 30))

        start_angle = end_angle
