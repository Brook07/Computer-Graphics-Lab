from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

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


def visualize_line_clipping(lines: List[Line], rect: Rect, algorithm_name: str, clip_func):
    """Visualize line clipping results"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Original lines (left plot)
    ax1.set_xlim(-5, 15)
    ax1.set_ylim(-3, 12)
    ax1.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                  rect.xmax - rect.xmin, 
                                  rect.ymax - rect.ymin, 
                                  fill=False, edgecolor='red', linewidth=2))
    
    colors = ['blue', 'green', 'orange', 'purple']
    for idx, line in enumerate(lines):
        x1, y1, x2, y2 = line
        ax1.plot([x1, x2], [y1, y2], color=colors[idx], linewidth=2, 
                label=f"Line {idx+1}", alpha=0.7)
    
    ax1.set_title(f"{algorithm_name} - Original Lines")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    
    # Clipped lines (right plot)
    ax2.set_xlim(-5, 15)
    ax2.set_ylim(-3, 12)
    ax2.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                  rect.xmax - rect.xmin, 
                                  rect.ymax - rect.ymin, 
                                  fill=False, edgecolor='red', linewidth=2))
    
    for idx, line in enumerate(lines):
        result = clip_func(line, rect)
        if result:
            x1, y1, x2, y2 = result
            ax2.plot([x1, x2], [y1, y2], color=colors[idx], linewidth=3, 
                    label=f"Clipped Line {idx+1}")
        else:
            ax2.text(0.5, 0.95 - idx*0.05, f"Line {idx+1}: Rejected", 
                    transform=ax2.transAxes, color=colors[idx])
    
    ax2.set_title(f"{algorithm_name} - Clipped Lines")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    
    plt.tight_layout()
    plt.savefig(f"output_{algorithm_name.lower().replace('-', '_')}.png", dpi=150, bbox_inches='tight')
    plt.show()


def visualize_polygon_clipping(subject_polygon: List[Point], rect: Rect):
    """Visualize Sutherland-Hodgman polygon clipping"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Original polygon (left plot)
    ax1.set_xlim(-2, 14)
    ax1.set_ylim(-2, 12)
    
    # Draw clipping rectangle
    ax1.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                  rect.xmax - rect.xmin, 
                                  rect.ymax - rect.ymin, 
                                  fill=False, edgecolor='red', linewidth=2, label='Clipping Window'))
    
    # Draw original polygon
    if subject_polygon:
        poly_x = [p[0] for p in subject_polygon] + [subject_polygon[0][0]]
        poly_y = [p[1] for p in subject_polygon] + [subject_polygon[0][1]]
        ax1.plot(poly_x, poly_y, 'b-o', linewidth=2, markersize=6, label='Original Polygon')
        ax1.fill(poly_x, poly_y, color='blue', alpha=0.3)
    
    ax1.set_title('Sutherland-Hodgman - Original Polygon')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    
    # Clipped polygon (right plot)
    ax2.set_xlim(-2, 14)
    ax2.set_ylim(-2, 12)
    
    # Draw clipping rectangle
    ax2.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                  rect.xmax - rect.xmin, 
                                  rect.ymax - rect.ymin, 
                                  fill=False, edgecolor='red', linewidth=2, label='Clipping Window'))
    
    # Draw clipped polygon
    clipped = clip_polygon_with_rect(subject_polygon, rect)
    if clipped:
        clipped_x = [p[0] for p in clipped] + [clipped[0][0]]
        clipped_y = [p[1] for p in clipped] + [clipped[0][1]]
        ax2.plot(clipped_x, clipped_y, 'g-o', linewidth=2, markersize=6, label='Clipped Polygon')
        ax2.fill(clipped_x, clipped_y, color='green', alpha=0.3)
    
    ax2.set_title('Sutherland-Hodgman - Clipped Polygon')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    
    plt.tight_layout()
    plt.savefig("output_sutherland_hodgman.png", dpi=150, bbox_inches='tight')
    plt.show()


def visualize_all_algorithms():
    """Create comprehensive visualization comparing all algorithms"""
    rect = Rect(0, 0, 10, 8)
    lines = [
        (2, 2, 8, 6),    # Completely inside
        (-3, 1, 12, 7),  # Crosses window
        (5, -2, 5, 10),  # Vertical line crossing
        (12, 10, 15, 14) # Completely outside
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Cohen-Sutherland
    ax = axes[0, 0]
    ax.set_xlim(-5, 17)
    ax.set_ylim(-3, 16)
    ax.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                 rect.xmax - rect.xmin, rect.ymax - rect.ymin, 
                                 fill=False, edgecolor='red', linewidth=2))
    colors = ['blue', 'green', 'orange', 'purple']
    for idx, line in enumerate(lines):
        result = cohen_sutherland_clip(line, rect)
        if result:
            x1, y1, x2, y2 = result
            ax.plot([x1, x2], [y1, y2], color=colors[idx], linewidth=3, label=f"L{idx+1}")
        # Also show original lines in light gray
        x1, y1, x2, y2 = line
        ax.plot([x1, x2], [y1, y2], color='lightgray', linewidth=1, alpha=0.5)
    ax.set_title('Cohen-Sutherland Clipping')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Liang-Barsky
    ax = axes[0, 1]
    ax.set_xlim(-5, 17)
    ax.set_ylim(-3, 16)
    ax.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                 rect.xmax - rect.xmin, rect.ymax - rect.ymin, 
                                 fill=False, edgecolor='red', linewidth=2))
    for idx, line in enumerate(lines):
        result = liang_barsky_clip(line, rect)
        if result:
            x1, y1, x2, y2 = result
            ax.plot([x1, x2], [y1, y2], color=colors[idx], linewidth=3, label=f"L{idx+1}")
        # Also show original lines in light gray
        x1, y1, x2, y2 = line
        ax.plot([x1, x2], [y1, y2], color='lightgray', linewidth=1, alpha=0.5)
    ax.set_title('Liang-Barsky Clipping')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Sutherland-Hodgman
    ax = axes[0, 2]
    subject = [(1, 1), (9, 2), (12, 5), (6, 10), (0, 8)]
    ax.set_xlim(-2, 14)
    ax.set_ylim(-2, 12)
    ax.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                 rect.xmax - rect.xmin, rect.ymax - rect.ymin, 
                                 fill=False, edgecolor='red', linewidth=2))
    
    # Original polygon
    poly_x = [p[0] for p in subject] + [subject[0][0]]
    poly_y = [p[1] for p in subject] + [subject[0][1]]
    ax.plot(poly_x, poly_y, 'b--', linewidth=1, alpha=0.5, label='Original')
    
    # Clipped polygon
    clipped = clip_polygon_with_rect(subject, rect)
    if clipped:
        clipped_x = [p[0] for p in clipped] + [clipped[0][0]]
        clipped_y = [p[1] for p in clipped] + [clipped[0][1]]
        ax.plot(clipped_x, clipped_y, 'g-o', linewidth=2, markersize=4, label='Clipped')
        ax.fill(clipped_x, clipped_y, color='green', alpha=0.3)
    
    ax.set_title('Sutherland-Hodgman Clipping')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Region codes visualization
    ax = axes[1, 0]
    ax.set_xlim(-5, 15)
    ax.set_ylim(-3, 12)
    ax.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                 rect.xmax - rect.xmin, rect.ymax - rect.ymin, 
                                 fill=True, facecolor='lightblue', alpha=0.3, edgecolor='red', linewidth=2))
    
    # Add region code labels
    regions = {
        'TOP-LEFT\n1001': (-2.5, 9.5), 'TOP\n1000': (5, 9.5), 'TOP-RIGHT\n1010': (12.5, 9.5),
        'LEFT\n0001': (-2.5, 4), 'INSIDE\n0000': (5, 4), 'RIGHT\n0010': (12.5, 4),
        'BOTTOM-LEFT\n0101': (-2.5, 1), 'BOTTOM\n0100': (5, 1), 'BOTTOM-RIGHT\n0110': (12.5, 1)
    }
    
    for label, (x, y) in regions.items():
        ax.text(x, y, label, ha='center', va='center', fontsize=8, 
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    ax.set_title('Cohen-Sutherland Region Codes')
    ax.grid(True, alpha=0.3)
    
    # Parametric line visualization for Liang-Barsky
    ax = axes[1, 1]
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-1, 2)
    
    t_values = np.linspace(0, 1, 100)
    for idx, line in enumerate(lines[:2]):  # Show first 2 lines
        x1, y1, x2, y2 = line
        result = liang_barsky_clip(line, rect)
        if result:
            rx1, ry1, rx2, ry2 = result
            # Find parameter values for clipped portion
            dx, dy = x2 - x1, y2 - y1
            if dx != 0:
                t1 = (rx1 - x1) / dx
                t2 = (rx2 - x1) / dx
            else:
                t1 = (ry1 - y1) / dy
                t2 = (ry2 - y1) / dy
            
            ax.axvspan(min(t1, t2), max(t1, t2), alpha=0.3, color=colors[idx], 
                      label=f'Line {idx+1} visible portion')
    
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axhline(y=1, color='black', linewidth=0.5)
    ax.set_xlabel('Parameter t')
    ax.set_ylabel('Visibility')
    ax.set_title('Liang-Barsky Parameter Space')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Clipping steps visualization
    ax = axes[1, 2]
    ax.text(0.5, 0.8, 'Algorithm Comparison', ha='center', fontsize=14, fontweight='bold')
    
    comparison_text = """
Cohen-Sutherland:
✓ Simple region code logic
✓ Good for many rejected lines
✗ Multiple iterations possible

Liang-Barsky:
✓ Parametric approach
✓ Single pass algorithm
✓ More efficient calculations

Sutherland-Hodgman:
✓ Handles convex polygons
✓ Works with any convex window
✗ More complex implementation
    """
    
    ax.text(0.1, 0.7, comparison_text, fontsize=10, verticalalignment='top', 
           fontfamily='monospace')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig("comprehensive_clipping_comparison.png", dpi=150, bbox_inches='tight')
    plt.show()


def visualize_line_clipping(lines: List[Line], rect: Rect, algorithm_name: str, clip_func):
    """Visualize line clipping results"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Original lines (left plot)
    ax1.set_xlim(-5, 15)
    ax1.set_ylim(-3, 12)
    ax1.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                  rect.xmax - rect.xmin, 
                                  rect.ymax - rect.ymin, 
                                  fill=False, edgecolor='red', linewidth=2))
    
    colors = ['blue', 'green', 'orange', 'purple']
    for idx, line in enumerate(lines):
        x1, y1, x2, y2 = line
        ax1.plot([x1, x2], [y1, y2], color=colors[idx], linewidth=2, 
                label=f"Line {idx+1}", alpha=0.7)
    
    ax1.set_title(f"{algorithm_name} - Original Lines")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    
    # Clipped lines (right plot)
    ax2.set_xlim(-5, 15)
    ax2.set_ylim(-3, 12)
    ax2.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                  rect.xmax - rect.xmin, 
                                  rect.ymax - rect.ymin, 
                                  fill=False, edgecolor='red', linewidth=2))
    
    for idx, line in enumerate(lines):
        result = clip_func(line, rect)
        if result:
            x1, y1, x2, y2 = result
            ax2.plot([x1, x2], [y1, y2], color=colors[idx], linewidth=3, 
                    label=f"Clipped Line {idx+1}")
        else:
            ax2.text(0.5, 0.95 - idx*0.05, f"Line {idx+1}: Rejected", 
                    transform=ax2.transAxes, color=colors[idx])
    
    ax2.set_title(f"{algorithm_name} - Clipped Lines")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    
    plt.tight_layout()
    plt.savefig(f"output_{algorithm_name.lower().replace('-', '_')}.png", dpi=150, bbox_inches='tight')
    plt.show()


def visualize_polygon_clipping(subject_polygon: List[Point], rect: Rect):
    """Visualize Sutherland-Hodgman polygon clipping"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Original polygon (left plot)
    ax1.set_xlim(-2, 14)
    ax1.set_ylim(-2, 12)
    
    # Draw clipping rectangle
    ax1.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                  rect.xmax - rect.xmin, 
                                  rect.ymax - rect.ymin, 
                                  fill=False, edgecolor='red', linewidth=2, label='Clipping Window'))
    
    # Draw original polygon
    if subject_polygon:
        poly_x = [p[0] for p in subject_polygon] + [subject_polygon[0][0]]
        poly_y = [p[1] for p in subject_polygon] + [subject_polygon[0][1]]
        ax1.plot(poly_x, poly_y, 'b-o', linewidth=2, markersize=6, label='Original Polygon')
        ax1.fill(poly_x, poly_y, color='blue', alpha=0.3)
    
    ax1.set_title('Sutherland-Hodgman - Original Polygon')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    
    # Clipped polygon (right plot)
    ax2.set_xlim(-2, 14)
    ax2.set_ylim(-2, 12)
    
    # Draw clipping rectangle
    ax2.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                  rect.xmax - rect.xmin, 
                                  rect.ymax - rect.ymin, 
                                  fill=False, edgecolor='red', linewidth=2, label='Clipping Window'))
    
    # Draw clipped polygon
    clipped = clip_polygon_with_rect(subject_polygon, rect)
    if clipped:
        clipped_x = [p[0] for p in clipped] + [clipped[0][0]]
        clipped_y = [p[1] for p in clipped] + [clipped[0][1]]
        ax2.plot(clipped_x, clipped_y, 'g-o', linewidth=2, markersize=6, label='Clipped Polygon')
        ax2.fill(clipped_x, clipped_y, color='green', alpha=0.3)
    
    ax2.set_title('Sutherland-Hodgman - Clipped Polygon')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    
    plt.tight_layout()
    plt.savefig("output_sutherland_hodgman.png", dpi=150, bbox_inches='tight')
    plt.show()


def visualize_all_algorithms():
    """Create comprehensive visualization comparing all algorithms"""
    rect = Rect(0, 0, 10, 8)
    lines = [
        (2, 2, 8, 6),    # Completely inside
        (-3, 1, 12, 7),  # Crosses window
        (5, -2, 5, 10),  # Vertical line crossing
        (12, 10, 15, 14) # Completely outside
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Cohen-Sutherland
    ax = axes[0, 0]
    ax.set_xlim(-5, 17)
    ax.set_ylim(-3, 16)
    ax.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                 rect.xmax - rect.xmin, rect.ymax - rect.ymin, 
                                 fill=False, edgecolor='red', linewidth=2))
    colors = ['blue', 'green', 'orange', 'purple']
    for idx, line in enumerate(lines):
        result = cohen_sutherland_clip(line, rect)
        if result:
            x1, y1, x2, y2 = result
            ax.plot([x1, x2], [y1, y2], color=colors[idx], linewidth=3, label=f"L{idx+1}")
        # Also show original lines in light gray
        x1, y1, x2, y2 = line
        ax.plot([x1, x2], [y1, y2], color='lightgray', linewidth=1, alpha=0.5)
    ax.set_title('Cohen-Sutherland Clipping')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Liang-Barsky
    ax = axes[0, 1]
    ax.set_xlim(-5, 17)
    ax.set_ylim(-3, 16)
    ax.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                 rect.xmax - rect.xmin, rect.ymax - rect.ymin, 
                                 fill=False, edgecolor='red', linewidth=2))
    for idx, line in enumerate(lines):
        result = liang_barsky_clip(line, rect)
        if result:
            x1, y1, x2, y2 = result
            ax.plot([x1, x2], [y1, y2], color=colors[idx], linewidth=3, label=f"L{idx+1}")
        # Also show original lines in light gray
        x1, y1, x2, y2 = line
        ax.plot([x1, x2], [y1, y2], color='lightgray', linewidth=1, alpha=0.5)
    ax.set_title('Liang-Barsky Clipping')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Sutherland-Hodgman
    ax = axes[0, 2]
    subject = [(1, 1), (9, 2), (12, 5), (6, 10), (0, 8)]
    ax.set_xlim(-2, 14)
    ax.set_ylim(-2, 12)
    ax.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                 rect.xmax - rect.xmin, rect.ymax - rect.ymin, 
                                 fill=False, edgecolor='red', linewidth=2))
    
    # Original polygon
    poly_x = [p[0] for p in subject] + [subject[0][0]]
    poly_y = [p[1] for p in subject] + [subject[0][1]]
    ax.plot(poly_x, poly_y, 'b--', linewidth=1, alpha=0.5, label='Original')
    
    # Clipped polygon
    clipped = clip_polygon_with_rect(subject, rect)
    if clipped:
        clipped_x = [p[0] for p in clipped] + [clipped[0][0]]
        clipped_y = [p[1] for p in clipped] + [clipped[0][1]]
        ax.plot(clipped_x, clipped_y, 'g-o', linewidth=2, markersize=4, label='Clipped')
        ax.fill(clipped_x, clipped_y, color='green', alpha=0.3)
    
    ax.set_title('Sutherland-Hodgman Clipping')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Region codes visualization
    ax = axes[1, 0]
    ax.set_xlim(-5, 15)
    ax.set_ylim(-3, 12)
    ax.add_patch(patches.Rectangle((rect.xmin, rect.ymin), 
                                 rect.xmax - rect.xmin, rect.ymax - rect.ymin, 
                                 fill=True, facecolor='lightblue', alpha=0.3, edgecolor='red', linewidth=2))
    
    # Add region code labels
    regions = {
        'TOP-LEFT\n1001': (-2.5, 9.5), 'TOP\n1000': (5, 9.5), 'TOP-RIGHT\n1010': (12.5, 9.5),
        'LEFT\n0001': (-2.5, 4), 'INSIDE\n0000': (5, 4), 'RIGHT\n0010': (12.5, 4),
        'BOTTOM-LEFT\n0101': (-2.5, 1), 'BOTTOM\n0100': (5, 1), 'BOTTOM-RIGHT\n0110': (12.5, 1)
    }
    
    for label, (x, y) in regions.items():
        ax.text(x, y, label, ha='center', va='center', fontsize=8, 
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    ax.set_title('Cohen-Sutherland Region Codes')
    ax.grid(True, alpha=0.3)
    
    # Parametric line visualization for Liang-Barsky
    ax = axes[1, 1]
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-1, 2)
    
    t_values = np.linspace(0, 1, 100)
    for idx, line in enumerate(lines[:2]):  # Show first 2 lines
        x1, y1, x2, y2 = line
        result = liang_barsky_clip(line, rect)
        if result:
            rx1, ry1, rx2, ry2 = result
            # Find parameter values for clipped portion
            dx, dy = x2 - x1, y2 - y1
            if dx != 0:
                t1 = (rx1 - x1) / dx
                t2 = (rx2 - x1) / dx
            else:
                t1 = (ry1 - y1) / dy
                t2 = (ry2 - y1) / dy
            
            ax.axvspan(min(t1, t2), max(t1, t2), alpha=0.3, color=colors[idx], 
                      label=f'Line {idx+1} visible portion')
    
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axhline(y=1, color='black', linewidth=0.5)
    ax.set_xlabel('Parameter t')
    ax.set_ylabel('Visibility')
    ax.set_title('Liang-Barsky Parameter Space')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Clipping steps visualization
    ax = axes[1, 2]
    ax.text(0.5, 0.8, 'Algorithm Comparison', ha='center', fontsize=14, fontweight='bold')
    
    comparison_text = """
Cohen-Sutherland:
✓ Simple region code logic
✓ Good for many rejected lines
✗ Multiple iterations possible

Liang-Barsky:
✓ Parametric approach
✓ Single pass algorithm
✓ More efficient calculations

Sutherland-Hodgman:
✓ Handles convex polygons
✓ Works with any convex window
✗ More complex implementation
    """
    
    ax.text(0.1, 0.7, comparison_text, fontsize=10, verticalalignment='top', 
           fontfamily='monospace')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig("comprehensive_clipping_comparison.png", dpi=150, bbox_inches='tight')
    plt.show()


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
    
    # Generate visualizations
    print("\n" + "="*50)
    print("Generating Visualizations...")
    print("="*50)
    
    # Individual algorithm visualizations
    visualize_line_clipping(list(lines), rect, "Cohen-Sutherland", cohen_sutherland_clip)
    visualize_line_clipping(list(lines), rect, "Liang-Barsky", liang_barsky_clip)
    visualize_polygon_clipping(subject, rect)
    
    # Comprehensive comparison
    visualize_all_algorithms()
    
    # Generate visualizations
    print("\n" + "="*50)
    print("Generating Visualizations...")
    print("="*50)
    
    # Individual algorithm visualizations
    visualize_line_clipping(list(lines), rect, "Cohen-Sutherland", cohen_sutherland_clip)
    visualize_line_clipping(list(lines), rect, "Liang-Barsky", liang_barsky_clip)
    visualize_polygon_clipping(subject, rect)
    
    # Comprehensive comparison
    visualize_all_algorithms()


if __name__ == "__main__":
    _demo()
