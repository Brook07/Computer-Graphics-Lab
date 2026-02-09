# Computer Graphics Lab 2

This project implements classic raster graphics algorithms and simple chart renderers using Python + Pygame.

Implemented:
- DDA Line Drawing
- Bresenham Line Drawing (both slopes: |m|<1 and |m|>=1)
- Midpoint Circle Drawing
- Midpoint Ellipse Drawing
- Line Graph (using DDA or Bresenham)
- Pie Chart

## Setup

1. Ensure Python 3.9+ is installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Controls:
- 1: DDA Line demo
- 2: Bresenham Line demo (both slopes shown)
- 3: Midpoint Circle demo
- 4: Midpoint Ellipse demo
- 5: Line Graph demo (toggle algorithm with `A`)
- 6: Pie Chart demo
- H: Toggle help overlay
- ESC / Q: Quit

## Notes
- Bresenham has two specific implementations (`bresenham_line_low` for |m|<1 and `bresenham_line_high` for |m|>=1). The general `bresenham_line` selects the right one automatically.
- Chart renderers scale input data to the drawing area; adjust sample data in `main.py` as needed.

## Outputs
Below are the generated output images for each demo (files are in this folder).

- **DDA Line Drawing:** [out_1_dda_lines.png](out_1_dda_lines.png) — Example lines drawn with the DDA algorithm.
- **Bresenham Line Drawing:** [out_2_bresenham_lines.png](out_2_bresenham_lines.png) — Lines rendered using Bresenham (handles both slope cases).
- **Midpoint Circle Drawing:** [out_3_circles.png](out_3_circles.png) — Circles rendered with the midpoint circle algorithm.
- **Midpoint Ellipse Drawing:** [out_4_ellipses.png](out_4_ellipses.png) — Ellipses produced by the midpoint ellipse routine.
- **Line Graph (DDA):** [out_5a_line_graph_dda.png](out_5a_line_graph_dda.png) — Sample line graph rendered using DDA for plotting.
- **Line Graph (Bresenham):** [out_5b_line_graph_bresenham.png](out_5b_line_graph_bresenham.png) — Same data plotted using Bresenham-based plotting.
- **Pie Chart:** [out_6_pie_chart.png](out_6_pie_chart.png) — Pie chart output from the simple chart renderer.

If you want these images embedded inline on GitHub, they will display automatically since they are in the same directory.
