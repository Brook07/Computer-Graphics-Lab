# 2D Transformations - Computer Graphics Lab Assignment

## Overview
This program implements various 2D transformations using **homogeneous coordinate systems**. All transformations are represented as 3×3 matrices operating on homogeneous coordinates (x, y, 1).

## Features

### Basic Transformations
1. **Translation** - Move shapes along X and Y axes
2. **Rotation** - Rotate shapes about the origin (counter-clockwise)
3. **Scaling** - Enlarge or shrink shapes
4. **Reflection** - Mirror shapes about X-axis, Y-axis, or origin
5. **Shearing** - Slant shapes along X or Y direction

### Composite Transformations
The program demonstrates **4 composite transformations**:
1. **Translation → Rotation → Scaling** (T→R→S)
2. **Scaling → Reflection → Translation** (S→Ref→T)
3. **Rotation → Shearing → Scaling** (R→Sh→S)
4. **Translation → Rotation → Scaling → Shearing → Reflection** (T→R→S→Sh→Ref)

### Supported Shapes
- Line
- Triangle
- Rectangle
- Square

## How It Works

### Homogeneous Coordinates
All 2D points are represented as homogeneous coordinates:
```
(x, y) → (x, y, 1)
```

### Transformation Matrices

#### Translation (tx, ty)
```
[1  0  tx]
[0  1  ty]
[0  0  1 ]
```

#### Rotation (θ degrees)
```
[cos(θ)  -sin(θ)  0]
[sin(θ)   cos(θ)  0]
[0        0       1]
```

#### Scaling (sx, sy)
```
[sx  0   0]
[0   sy  0]
[0   0   1]
```

#### Reflection - Y-axis
```
[-1  0   0]
[0   1   0]
[0   0   1]
```

#### Reflection - X-axis
```
[1   0   0]
[0  -1   0]
[0   0   1]
```

#### Shearing (shx, shy)
```
[1    shx  0]
[shy  1    0]
[0    0    1]
```

### Composite Transformations
Multiple transformations are combined by matrix multiplication:
```
Composite = Tn × Tn-1 × ... × T2 × T1
```
**Important**: The order of matrix multiplication matters!

## Installation Requirements

```bash
pip install numpy matplotlib
```

## How to Run

```bash
python 2D_Transformations.py
```

## Program Output

The program will:
1. Display all original and transformed coordinates in console
2. Show transformation matrices used
3. Display descriptions of each transformation
4. Show visual comparisons (before/after plots) for each transformation

## Key Classes and Methods

### Shape2D Class
- `__init__(points, name)` - Initialize a shape
- `get_homogeneous_points()` - Convert to homogeneous coordinates
- `apply_transformation(matrix)` - Apply transformation
- `reset()` - Reset to original position

### Transformation2D Class (Static Methods)
- `translation_matrix(tx, ty)` - Create translation matrix
- `rotation_matrix(angle_degrees)` - Create rotation matrix
- `scaling_matrix(sx, sy)` - Create scaling matrix
- `reflection_matrix(axis)` - Create reflection matrix
- `shearing_matrix(shx, shy)` - Create shearing matrix
- `composite_transformation(*matrices)` - Combine multiple matrices

### Visualizer2D Class (Static Methods)
- `plot_shape(shape, ax, ...)` - Plot a single shape
- `plot_comparison(original, transformed, title, filename)` - Compare original and transformed

## Example Usage

```python
# Create a triangle
triangle = Shape2D([(0, 0), (4, 0), (2, 3)], name="Triangle")

# Apply translation
trans_matrix = Transformation2D.translation_matrix(tx=5, ty=3)
triangle.apply_transformation(trans_matrix)

# Apply rotation
rot_matrix = Transformation2D.rotation_matrix(angle=45)
triangle.apply_transformation(rot_matrix)

# Composite transformation
composite = Transformation2D.composite_transformation(rot_matrix, trans_matrix)
triangle.apply_transformation(composite)
```

## Important Notes

1. **Homogeneous Coordinates**: All transformations work with homogeneous coordinates where a 2D point (x, y) becomes (x, y, 1).

2. **Matrix Order**: In composite transformations, matrices are applied from right to left mathematically, but the function applies them in the order specified (left to right in the argument list).

3. **Rotation Angle**: Angles are specified in degrees, not radians. Positive angles rotate counter-clockwise.

4. **Reflection Axes**:
   - `'x'` - Reflection about X-axis (vertical mirror)
   - `'y'` - Reflection about Y-axis (horizontal mirror)
   - `'origin'` - Reflection about origin

## Mathematical Foundation

The key concept is that any 2D point can be represented in homogeneous coordinates and transformed using matrix multiplication:

```
P' = T × P

where:
P = [x, y, 1]^T (point in homogeneous coordinates)
T = 3×3 transformation matrix
P' = transformed point
```

## Assignment Requirements Covered

✓ 2D Translation
✓ 2D Rotation
✓ 2D Scaling
✓ 2D Reflection
✓ 2D Shearing
✓ Composite Transformations (4 examples)
✓ Works on multiple 2D shapes (Line, Triangle, Rectangle, Square)
✓ Uses Homogeneous Coordinate Systems
✓ Visual representation of transformations

## Visualization Output

The program generates side-by-side comparisons showing:
- Original shape (blue)
- Transformed shape (red)
- Both plotted on the same coordinate system
- Grid for reference


