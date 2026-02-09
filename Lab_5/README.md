# Lab 5: 3D Transformations and Orthographic Projection (OpenGL)

This lab demonstrates 3D transformations (Translation, Rotation, Shearing, Scaling) applied to standard OpenGL/GLUT 3D shapes, and a toggleable Orthographic Projection.

## Requirements
- Python 3.8+
- PyOpenGL and PyOpenGL_accelerate
- matplotlib, numpy, Pillow (for visual outputs)

Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Visual Demo

To generate all visual outputs for the lab report:

```powershell
python demo.py
```

This will create static visualizations in the `fig/` directory showing all transformation types.

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

- **Common**
	- Shapes: `1` Cube, `2` Sphere, `3` Teapot, `4` Torus
	- Projection: `p` toggles Perspective vs Orthographic
	- Screenshot: `f` takes a screenshot (saves to fig/ directory)
	- Demo: `d` captures transformation demonstration sequences
	- Exit: `Esc`

- **Translation**
	- Axis: `x`, `y`, `z`
	- Adjust: Arrow Up/Down moves along selected axis
	- Mode: `t` switches to translation mode
	- Reset: Space resets translation

- **Rotation**
	- Axis: `x`, `y`, `z`
	- Adjust: Arrow Up/Down rotates about selected axis
	- Mode: `r` switches to rotation mode
	- Reset: Space resets rotation angles

- **Scaling**
	- Axis: `x`, `y`, `z`
	- Adjust: Arrow Up/Down scales along selected axis
	- Mode: `s` switches to scaling mode
	- Reset: Space resets scales to 1,1,1

- **Shearing**
	- Component: `c` cycles `xy, xz, yx, yz, zx, zy`
	- Adjust: Arrow Up/Down changes selected shear component
	- Mode: `h` switches to shearing mode
	- Reset: Space resets all shear components

## Visual Output

The lab provides multiple ways to generate visual outputs:

1. **Static Visualizations**: Run `python demo.py` to generate matplotlib-based comparison images
2. **OpenGL Screenshots**: Use `f` key in any OpenGL program to capture screenshots
3. **Demonstration Sequences**: Use `d` key to automatically capture transformation progressions

All images are saved in the `fig/` directory and can be used in lab reports.

## Files

- `main.py` - Combined interactive demo with all transformations
- `translation.py` - Translation-focused demo
- `rotation.py` - Rotation-focused demo
- `scaling.py` - Scaling-focused demo
- `shearing.py` - Shearing-focused demo
- `ortho_projection.py` - Projection comparison demo
- `visual_demo.py` - Static visualization generator
- `demo.py` - Quick demo runner and help
- `requirements.txt` - Python dependencies
	- Reset: Space resets all shear components

- Orthographic Projection
	- Start in orthographic mode; `p` toggles perspective
	- Arrow Up/Down: change Z offset to visualize depth vs size

## Notes
- Shearing uses a 4x4 matrix multiplied into the model transform.
- Orthographic projection uses `glOrtho`, Perspective uses `gluPerspective`.
- If GLUT fails to open a window on Windows, install FreeGLUT or run in a Python environment where GLUT is available.
