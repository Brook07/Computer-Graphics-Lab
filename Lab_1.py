import glfw
from OpenGL.GL import *


class TextRenderer:
    def __init__(self):
        self.th = 15  # stroke thickness

    def rect(self, x1, y1, x2, y2):
        glBegin(GL_QUADS)
        glVertex2f(x1, y1)
        glVertex2f(x2, y1)
        glVertex2f(x2, y2)
        glVertex2f(x1, y2)
        glEnd()

    # -------- LETTERS --------
    def drawU(self, x, y, w, h):
        t = self.th
        self.rect(x, y, x + t, y + h)
        self.rect(x + w - t, y, x + w, y + h)
        self.rect(x + t, y, x + w - t, y + t)

    def drawT(self, x, y, w, h):
        t = self.th
        self.rect(x, y + h - t, x + w, y + h)
        self.rect(x + w / 2 - t / 2, y, x + w / 2 + t / 2, y + h)

    def drawS(self, x, y, w, h):
        t = self.th
        self.rect(x, y + h - t, x + w, y + h)
        self.rect(x, y + h / 2 - t / 2, x + w, y + h / 2 + t / 2)
        self.rect(x, y, x + w, y + t)

        self.rect(x, y + h / 2, x + t, y + h - t)
        self.rect(x + w - t, y + t, x + w, y + h / 2)

    def drawA(self, x, y, w, h):
        t = self.th
        self.rect(x, y, x + t, y + h)
        self.rect(x + w - t, y, x + w, y + h)
        self.rect(x + t, y + h / 2 - t / 2,
                  x + w - t, y + h / 2 + t / 2)
        self.rect(x, y + h - t, x + w, y + h)

    def drawV(self, x, y, w, h):
 
        # Left stroke
        glBegin(GL_POLYGON)
        glVertex2f(x, y + h)
        glVertex2f(x + w * 0.35, y)
        glVertex2f(x + w * 0.50, y)
        glVertex2f(x + w * 0.15, y + h)
        glEnd()

        # Right stroke
        glBegin(GL_POLYGON)
        glVertex2f(x + w * 0.85, y + h)
        glVertex2f(x + w * 0.50, y)
        glVertex2f(x + w * 0.65, y)
        glVertex2f(x + w, y + h)
        glEnd()

    # -------- WORD --------
    def draw_UTSAV(self):
        glColor3f(0.2, 0.8, 1.0)

        x = 200
        y = 250
        w = 90
        h = 220
        gap = 35

        self.drawU(x, y, w, h); x += w + gap
        self.drawT(x, y, w, h); x += w + gap
        self.drawS(x, y, w, h); x += w + gap
        self.drawA(x, y, w, h); x += w + gap
        self.drawV(x, y, w, h)


def main():
    if not glfw.init():
        raise RuntimeError("GLFW initialization failed")

    width, height = 1200, 800
    window = glfw.create_window(width, height, "UTSAV - OpenGL", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Window creation failed")

    glfw.make_context_current(window)

    glClearColor(0.05, 0.05, 0.08, 1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    text = TextRenderer()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        text.draw_UTSAV()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
