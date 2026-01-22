# Lab 5: 3D Transformations and Orthographic Projection (OpenGL)

This lab demonstrates 3D transformations (Translation, Rotation, Shearing, Scaling) applied to standard OpenGL/GLUT 3D shapes, and a toggleable Orthographic Projection.

## Requirements
- Python 3.8+
- PyOpenGL and PyOpenGL_accelerate

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

You can run a focused demo for each transformation or a combined one:

- Translation demo:

```powershell
python translation.py
```

- Rotation demo:

```powershell
python rotation.py
```

- Scaling demo:

```powershell
python scaling.py
```

- Shearing demo:

```powershell
python shearing.py
```

- Orthographic projection demo:

```powershell
python ortho_projection.py
```

- Combined controls (all in one):

```powershell
python main.py
```

## Controls

Controls vary slightly per demo to keep things focused:

- Common
	- Shapes: `1` Cube, `2` Sphere, `3` Teapot, `4` Torus
	- Projection: `p` toggles Perspective vs Orthographic
	- Exit: `Esc`

- Translation
	- Axis: `x`, `y`, `z`
	- Adjust: Arrow Up/Down moves along selected axis
	- Reset: Space resets translation

- Rotation
	- Axis: `x`, `y`, `z`
	- Adjust: Arrow Up/Down rotates about selected axis
	- Reset: Space resets rotation angles

- Scaling
	- Axis: `x`, `y`, `z`
	- Adjust: Arrow Up/Down scales along selected axis
	- Reset: Space resets scales to 1,1,1

- Shearing
	- Component: `c` cycles `xy, xz, yx, yz, zx, zy`
	- Adjust: Arrow Up/Down changes selected shear component
	- Reset: Space resets all shear components

- Orthographic Projection
	- Start in orthographic mode; `p` toggles perspective
	- Arrow Up/Down: change Z offset to visualize depth vs size

## Notes
- Shearing uses a 4x4 matrix multiplied into the model transform.
- Orthographic projection uses `glOrtho`, Perspective uses `gluPerspective`.
- If GLUT fails to open a window on Windows, install FreeGLUT or run in a Python environment where GLUT is available.
