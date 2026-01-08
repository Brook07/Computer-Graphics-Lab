from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

Point = Tuple[float, float]
Line = Tuple[float, float, float, float]


@dataclass(frozen=True)
class Rect:
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    def as_polygon(self) -> List[Point]:
        return [
            (self.xmin, self.ymin),
            (self.xmax, self.ymin),
            (self.xmax, self.ymax),
            (self.xmin, self.ymax),
        ]


INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8


def _compute_out_code(x: float, y: float, rect: Rect) -> int:
    code = INSIDE
    if x < rect.xmin:
        code |= LEFT
    elif x > rect.xmax:
        code |= RIGHT
    if y < rect.ymin:
        code |= BOTTOM
    elif y > rect.ymax:
        code |= TOP
    return code


def cohen_sutherland_clip(line: Line, rect: Rect) -> Optional[Line]:
    x1, y1, x2, y2 = line
    out_code1 = _compute_out_code(x1, y1, rect)
    out_code2 = _compute_out_code(x2, y2, rect)

    while True:
        if out_code1 == 0 and out_code2 == 0:
            return (x1, y1, x2, y2)
        if out_code1 & out_code2:
            return None

        out_code_out = out_code1 or out_code2

        if out_code_out & TOP:
            x = x1 + (x2 - x1) * (rect.ymax - y1) / (y2 - y1)
            y = rect.ymax
        elif out_code_out & BOTTOM:
            x = x1 + (x2 - x1) * (rect.ymin - y1) / (y2 - y1)
            y = rect.ymin
        elif out_code_out & RIGHT:
            y = y1 + (y2 - y1) * (rect.xmax - x1) / (x2 - x1)
            x = rect.xmax
        else:
            y = y1 + (y2 - y1) * (rect.xmin - x1) / (x2 - x1)
            x = rect.xmin

        if out_code_out == out_code1:
            x1, y1 = x, y
            out_code1 = _compute_out_code(x1, y1, rect)
        else:
            x2, y2 = x, y
            out_code2 = _compute_out_code(x2, y2, rect)


def liang_barsky_clip(line: Line, rect: Rect) -> Optional[Line]:
    x1, y1, x2, y2 = line
    dx = x2 - x1
    dy = y2 - y1

    p = [-dx, dx, -dy, dy]
    q = [x1 - rect.xmin, rect.xmax - x1, y1 - rect.ymin, rect.ymax - y1]

    u1, u2 = 0.0, 1.0
    for pk, qk in zip(p, q):
        if pk == 0:
            if qk < 0:
                return None
            continue
        u = -qk / pk
        if pk < 0:
            if u > u2:
                return None
            if u > u1:
                u1 = u
        else:
            if u < u1:
                return None
            if u < u2:
                u2 = u

    clipped_start = (x1 + u1 * dx, y1 + u1 * dy)
    clipped_end = (x1 + u2 * dx, y1 + u2 * dy)
    return (*clipped_start, *clipped_end)


def _is_inside(point: Point, edge_start: Point, edge_end: Point) -> bool:
    x, y = point
    x1, y1 = edge_start
    x2, y2 = edge_end
    return (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) >= 0


def _compute_intersection(
    p1: Point, p2: Point, c1: Point, c2: Point
) -> Point:
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = c1
    x4, y4 = c2

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return p2

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
    return (px, py)


def sutherland_hodgman_clip(
    subject_polygon: Sequence[Point], clip_polygon: Sequence[Point]
) -> List[Point]:
    output_list: List[Point] = list(subject_polygon)
    if not output_list:
        return []

    clip_points = list(clip_polygon)
    for i in range(len(clip_points)):
        input_list = output_list
        output_list = []
        c_start = clip_points[i]
        c_end = clip_points[(i + 1) % len(clip_points)]

        if not input_list:
            break

        s = input_list[-1]
        for e in input_list:
            if _is_inside(e, c_start, c_end):
                if not _is_inside(s, c_start, c_end):
                    output_list.append(_compute_intersection(s, e, c_start, c_end))
                output_list.append(e)
            elif _is_inside(s, c_start, c_end):
                output_list.append(_compute_intersection(s, e, c_start, c_end))
            s = e
    return output_list


def clip_polygon_with_rect(subject_polygon: Sequence[Point], rect: Rect) -> List[Point]:
    return sutherland_hodgman_clip(subject_polygon, rect.as_polygon())


def _format_line(label: str, line: Optional[Line]) -> str:
    if line is None:
        return f"{label}: rejected"
    x1, y1, x2, y2 = line
    return f"{label}: ({x1:.2f}, {y1:.2f}) -> ({x2:.2f}, {y2:.2f})"


def _demo() -> None:
    rect = Rect(0, 0, 10, 8)
    lines: Iterable[Line] = [
        (2, 2, 8, 6),
        (-3, 1, 12, 7),
        (5, -2, 5, 10),
        (12, 10, 15, 14),
    ]

    print("Cohen-Sutherland:")
    for idx, line in enumerate(lines, start=1):
        result = cohen_sutherland_clip(line, rect)
        print(_format_line(f"  L{idx}", result))

    print("\nLiang-Barsky:")
    for idx, line in enumerate(lines, start=1):
        result = liang_barsky_clip(line, rect)
        print(_format_line(f"  L{idx}", result))

    subject = [(1, 1), (9, 2), (12, 5), (6, 10), (0, 8)]
    clipped = clip_polygon_with_rect(subject, rect)

    print("\nSutherland-Hodgman (polygon vs rect):")
    for i, point in enumerate(clipped, start=1):
        x, y = point
        print(f"  P{i}: ({x:.2f}, {y:.2f})")


if __name__ == "__main__":
    _demo()
