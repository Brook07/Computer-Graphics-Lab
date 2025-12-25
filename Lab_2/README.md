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
