from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

window_width = 1000
window_height = 700

axis = "x"
shape_index = 0
projection = "perspective"

rx, ry, rz = 0.0, 0.0, 0.0

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
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)
    glRotatef(rz, 0, 0, 1)
    draw_shape()
    glPopMatrix()

    render_text(10, window_height - 20, f"Rotation | Axis: {axis} | Shape: {shape_index+1} | Proj: {projection}")
    render_text(10, window_height - 40, f"R({rx:.1f},{ry:.1f},{rz:.1f})")

    glutSwapBuffers()

def reshape(w, h):
    global window_width, window_height
    window_width, window_height = max(1, w), max(1, h)
    glViewport(0, 0, window_width, window_height)

def keyboard(key, x, y):
    global axis, shape_index, projection
    global rx, ry, rz
    k = key.decode("utf-8") if isinstance(key, bytes) else key
    if k == "\x1b":
        glutLeaveMainLoop()
        return
    if k in ("1", "2", "3", "4"):
        shape_index = int(k) - 1
    elif k in ("x", "y", "z"):
        axis = k
    elif k == "p":
        projection = "orthographic" if projection == "perspective" else "perspective"
    elif k == " ":
        rx, ry, rz = 0.0, 0.0, 0.0
    glutPostRedisplay()

def special_keys(key, x, y):
    global rx, ry, rz
    delta_r = 5.0
    inc = key == GLUT_KEY_UP
    val = (delta_r if inc else -delta_r)
    if axis == "x":
        rx += val
    elif axis == "y":
        ry += val
    else:
        rz += val
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
    glutCreateWindow(b"Lab 5 - Rotation")
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
