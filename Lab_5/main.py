from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

window_width = 1000
window_height = 700

mode = "translate"
axis = "x"
shape_index = 0

tx, ty, tz = 0.0, 0.0, 0.0
rx, ry, rz = 0.0, 0.0, 0.0
sx, sy, sz = 1.0, 1.0, 1.0

shear_components = ["xy", "xz", "yx", "yz", "zx", "zy"]
shear_comp_index = 0
sh_xy = 0.0
sh_xz = 0.0
sh_yx = 0.0
sh_yz = 0.0
sh_zx = 0.0
sh_zy = 0.0

projection = "perspective"

def get_shear_matrix():
    return [
        1.0, sh_yx, sh_zx, 0.0,
        sh_xy, 1.0, sh_zy, 0.0,
        sh_xz, sh_yz, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0,
    ]

def draw_axes():
    glDisable(GL_LIGHTING)
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(2, 0, 0)
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 2, 0)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 2)
    glEnd()
    glEnable(GL_LIGHTING)

def draw_shape():
    glColor3f(0.9, 0.9, 0.9)
    if shape_index == 0:
        glutSolidCube(1.0)
    elif shape_index == 1:
        glutSolidSphere(0.6, 32, 32)
    elif shape_index == 2:
        glutSolidTeapot(0.6)
    else:
        glutSolidTorus(0.2, 0.6, 32, 32)

def render_text(x, y, text):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glColor3f(1, 1, 1)
    glRasterPos2i(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(ch))
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = window_width / float(window_height)
    if projection == "perspective":
        gluPerspective(60.0, aspect, 0.1, 100.0)
    else:
        glOrtho(-2.0 * aspect, 2.0 * aspect, -2.0, 2.0, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    draw_axes()

    glPushMatrix()
    glTranslatef(tx, ty, tz)
    glMultMatrixf(get_shear_matrix())
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)
    glRotatef(rz, 0, 0, 1)
    glScalef(sx, sy, sz)

    draw_shape()

    glPopMatrix()

    render_text(10, window_height - 20, f"Mode: {mode} | Axis: {axis} | Shape: {shape_index+1} | Proj: {projection}")
    render_text(10, window_height - 40, f"T({tx:.2f},{ty:.2f},{tz:.2f}) R({rx:.1f},{ry:.1f},{rz:.1f}) S({sx:.2f},{sy:.2f},{sz:.2f}) H(xy:{sh_xy:.2f} xz:{sh_xz:.2f} yx:{sh_yx:.2f} yz:{sh_yz:.2f} zx:{sh_zx:.2f} zy:{sh_zy:.2f})")

    glutSwapBuffers()

def reshape(w, h):
    global window_width, window_height
    window_width, window_height = max(1, w), max(1, h)
    glViewport(0, 0, window_width, window_height)

def keyboard(key, x, y):
    global mode, axis, shape_index, projection
    global tx, ty, tz, rx, ry, rz, sx, sy, sz
    global shear_comp_index
    k = key.decode("utf-8") if isinstance(key, bytes) else key
    if k == "\x1b":
        glutLeaveMainLoop()
        return
    if k in ("1", "2", "3", "4"):
        shape_index = int(k) - 1
    elif k in ("t", "r", "s", "h"):
        mode = {"t": "translate", "r": "rotate", "s": "scale", "h": "shear"}[k]
    elif k in ("x", "y", "z"):
        axis = k
    elif k == "p":
        projection = "orthographic" if projection == "perspective" else "perspective"
    elif k == "c" and mode == "shear":
        shear_comp_index = (shear_comp_index + 1) % len(shear_components)
    elif k == " ":
        tx, ty, tz = 0.0, 0.0, 0.0
        rx, ry, rz = 0.0, 0.0, 0.0
        sx, sy, sz = 1.0, 1.0, 1.0
        reset_shear()
    glutPostRedisplay()

def reset_shear():
    global sh_xy, sh_xz, sh_yx, sh_yz, sh_zx, sh_zy
    sh_xy = sh_xz = sh_yx = sh_yz = sh_zx = sh_zy = 0.0

def special_keys(key, x, y):
    global tx, ty, tz, rx, ry, rz, sx, sy, sz
    global sh_xy, sh_xz, sh_yx, sh_yz, sh_zx, sh_zy
    delta_t = 0.1
    delta_r = 5.0
    delta_s = 0.1
    delta_h = 0.05

    inc = key == GLUT_KEY_UP
    if mode == "translate":
        if axis == "x":
            tx += (delta_t if inc else -delta_t)
        elif axis == "y":
            ty += (delta_t if inc else -delta_t)
        else:
            tz += (delta_t if inc else -delta_t)
    elif mode == "rotate":
        if axis == "x":
            rx += (delta_r if inc else -delta_r)
        elif axis == "y":
            ry += (delta_r if inc else -delta_r)
        else:
            rz += (delta_r if inc else -delta_r)
    elif mode == "scale":
        if axis == "x":
            sx += (delta_s if inc else -delta_s)
        elif axis == "y":
            sy += (delta_s if inc else -delta_s)
        else:
            sz += (delta_s if inc else -delta_s)
    elif mode == "shear":
        comp = shear_components[shear_comp_index]
        val = (delta_h if inc else -delta_h)
        if comp == "xy":
            sh_xy += val
        elif comp == "xz":
            sh_xz += val
        elif comp == "yx":
            sh_yx += val
        elif comp == "yz":
            sh_yz += val
        elif comp == "zx":
            sh_zx += val
        elif comp == "zy":
            sh_zy += val
    glutPostRedisplay()

def init_gl():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glClearColor(0.08, 0.08, 0.1, 1.0)

def idle():
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Lab 5 - 3D Transformations & Orthographic Projection")
    init_gl()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    import sys
    main()
