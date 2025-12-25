from PIL import Image, ImageDraw
import math

W, H = 900, 700
BG = (245, 245, 245)
FG = (20, 20, 20)
RED = (220, 60, 60)
GREEN = (60, 180, 75)
BLUE = (60, 60, 220)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 153, 215)

class Surface:
    def __init__(self, width, height, bg):
        self.img = Image.new('RGB', (width, height), bg)
        self.px = self.img.load()
        self.width = width
        self.height = height

    def set_at(self, pos, color):
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            self.px[x, y] = color

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def save(self, path):
        self.img.save(path)


def plot(surface: Surface, x: int, y: int, color):
    surface.set_at((x, y), color)


def dda_line(surface: Surface, x0, y0, x1, y1, color):
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


def bresenham_line_low(surface: Surface, x0, y0, x1, y1, color):
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


def bresenham_line_high(surface: Surface, x0, y0, x1, y1, color):
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


def bresenham_line(surface: Surface, x0, y0, x1, y1, color):
    if x0 == x1:
        ys, ye = (y0, y1) if y0 <= y1 else (y1, y0)
        for y in range(ys, ye + 1):
            plot(surface, x0, y, color)
        return
    m = (y1 - y0) / (x1 - x0)
    if abs(m) < 1:
        bresenham_line_low(surface, x0, y0, x1, y1, color)
    else:
        bresenham_line_high(surface, x0, y0, x1, y1, color)


def _circle_symmetry(surface: Surface, xc, yc, x, y, color):
    plot(surface, xc + x, yc + y, color)
    plot(surface, xc - x, yc + y, color)
    plot(surface, xc + x, yc - y, color)
    plot(surface, xc - x, yc - y, color)
    plot(surface, xc + y, yc + x, color)
    plot(surface, xc - y, yc + x, color)
    plot(surface, xc + y, yc - x, color)
    plot(surface, xc - y, yc - x, color)


def midpoint_circle(surface: Surface, xc, yc, r, color):
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


def _ellipse_symmetry(surface: Surface, xc, yc, x, y, color):
    plot(surface, xc + x, yc + y, color)
    plot(surface, xc - x, yc + y, color)
    plot(surface, xc + x, yc - y, color)
    plot(surface, xc - x, yc - y, color)


def midpoint_ellipse(surface: Surface, xc, yc, rx, ry, color):
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


def draw_axes(surface: Surface, rect, color=(180, 180, 180)):
    x0, y0, w, h = rect
    # x-axis
    bresenham_line(surface, x0, y0 + h // 2, x0 + w, y0 + h // 2, color)
    # y-axis
    bresenham_line(surface, x0 + w // 2, y0, x0 + w // 2, y0 + h, color)


def line_graph(surface: Surface, data, rect, color, algo='dda'):
    if not data:
        return
    x0, y0, w, h = rect
    n = len(data)
    mn = min(data)
    mx = max(data)
    span = max(mx - mn, 1e-6)

    def to_point(i, v):
        x = x0 + int(i * (w - 1) / (n - 1))
        y = y0 + h - 1 - int((v - mn) / span * (h - 1))
        return x, y

    pts = [to_point(i, v) for i, v in enumerate(data)]
    for i in range(n - 1):
        (x0p, y0p), (x1p, y1p) = pts[i], pts[i + 1]
        if algo.lower().startswith('bres'):
            bresenham_line(surface, x0p, y0p, x1p, y1p, color)
        else:
            dda_line(surface, x0p, y0p, x1p, y1p, color)


def pie_chart(surface: Surface, values, rect, colors):
    total = sum(values) if values else 0.0
    if total <= 0:
        return

    cx = rect[0] + rect[2] // 2
    cy = rect[1] + rect[3] // 2
    r = min(rect[2], rect[3]) // 2 - 4

    midpoint_circle(surface, cx, cy, r, (150, 150, 150))

    start_angle = 0.0
    two_pi = 2.0 * math.pi
    draw = ImageDraw.Draw(surface.img)

    for idx, val in enumerate(values):
        frac = val / total
        sweep = frac * two_pi
        end_angle = start_angle + sweep
        color = colors[idx % len(colors)]

        steps = max(12, int(sweep * r / 6))
        pts = [(cx, cy)]
        for k in range(steps + 1):
            th = start_angle + k * sweep / steps
            x = cx + int(r * math.cos(th))
            y = cy + int(r * math.sin(th))
            pts.append((x, y))
        draw.polygon(pts, fill=color)

        xs = cx + int(r * math.cos(start_angle))
        ys = cy + int(r * math.sin(start_angle))
        xe = cx + int(r * math.cos(end_angle))
        ye = cy + int(r * math.sin(end_angle))
        bresenham_line(surface, cx, cy, xs, ys, (30, 30, 30))
        bresenham_line(surface, cx, cy, xe, ye, (30, 30, 30))

        start_angle = end_angle


def main():
    s = Surface(W, H, BG)

    # 1: DDA
    dda_line(s, 100, 100, 800, 120, RED)
    dda_line(s, 120, 160, 760, 500, GREEN)
    dda_line(s, 400, 100, 420, 600, BLUE)
    s.save('out_1_dda_lines.png')

    # 2: Bresenham both slopes
    s2 = Surface(W, H, BG)
    bresenham_line(s2, 100, 120, 800, 200, RED)
    bresenham_line(s2, 150, 300, 850, 330, GREEN)
    bresenham_line(s2, 120, 160, 200, 650, BLUE)
    bresenham_line(s2, 800, 600, 200, 100, ORANGE)
    s2.save('out_2_bresenham_lines.png')

    # 3: Midpoint Circle
    s3 = Surface(W, H, BG)
    midpoint_circle(s3, W // 2, H // 2, 200, FG)
    midpoint_circle(s3, W // 2, H // 2, 120, CYAN)
    midpoint_circle(s3, W // 2, H // 2, 60, ORANGE)
    s3.save('out_3_circles.png')

    # 4: Midpoint Ellipse
    s4 = Surface(W, H, BG)
    midpoint_ellipse(s4, W // 2, H // 2, 280, 160, FG)
    midpoint_ellipse(s4, W // 2, H // 2, 200, 120, CYAN)
    midpoint_ellipse(s4, W // 2, H // 2, 120, 60, ORANGE)
    s4.save('out_4_ellipses.png')

    # 5: Line Graph (DDA then Bresenham)
    s5a = Surface(W, H, BG)
    rect = (80, 100, W - 160, H - 200)
    draw_axes(s5a, rect)
    data = [12, 18, 5, 9, 14, 26, 17, 30, 22, 28, 33, 21]
    line_graph(s5a, data, rect, RED, algo='dda')
    s5a.save('out_5a_line_graph_dda.png')

    s5b = Surface(W, H, BG)
    draw_axes(s5b, rect)
    line_graph(s5b, data, rect, RED, algo='bresenham')
    s5b.save('out_5b_line_graph_bresenham.png')

    # 6: Pie Chart
    s6 = Surface(W, H, BG)
    pie_rect = (150, 120, 600, 460)
    values = [40, 25, 15, 10, 10]
    colors = [RED, GREEN, BLUE, ORANGE, PURPLE]
    pie_chart(s6, values, pie_rect, colors)
    s6.save('out_6_pie_chart.png')

    print('Generated:')
    print(' out_1_dda_lines.png')
    print(' out_2_bresenham_lines.png')
    print(' out_3_circles.png')
    print(' out_4_ellipses.png')
    print(' out_5a_line_graph_dda.png')
    print(' out_5b_line_graph_bresenham.png')
    print(' out_6_pie_chart.png')

if __name__ == '__main__':
    main()
