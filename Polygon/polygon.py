import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader
import math


class App:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_mode((512, 512), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(0, 0, 0, 0)    # set back ground color

        self.shader = self.createShader(
            "Two_Triangle/shaders/vertex.txt", "Two_Triangle/shaders/fragment.txt")
        glUseProgram(self.shader)
        self.pentagon = Pentagon(1, 7)

        self.mainLoop()

    def createShader(self, vertexFilepath, fragmentFilepath):
        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()
        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def mainLoop(self):
        running = True
        while (running):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            glClear(GL_COLOR_BUFFER_BIT)    # color buffer

            glUseProgram(self.shader)
            glBindVertexArray(self.pentagon.vao)
            glDrawArrays(GL_TRIANGLE_FAN, 0, self.pentagon.vertex_count)
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.pentagon.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class Pentagon:
    def __init__(self, radius, numSides) -> None:
        self.vertices = self.verticesPolygon(radius, numSides)

        self.vertices = np.array(self.vertices, dtype=np.float32)
        # There is a vertex at the center and a repeat vertex at the end
        # as head and tail are the same
        self.vertex_count = numSides + 2
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes,
                     self.vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

    def verticesPolygon(self, radius, numSide):
        # a center vertex at (0, 0)
        polyVertices = [0, 0]
        angle = 360/numSide
        # draw 6 time for 5 + 1 outside vertex
        for x in range(0, numSide + 1):
            x_cordinate = radius*math.cos(angle + (2*x*math.pi)/numSide)
            y_cordinate = radius*math.sin(angle + (2*x*math.pi)/numSide)
            polyVertices.append(x_cordinate)
            polyVertices.append(y_cordinate)

        return polyVertices

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


if __name__ == "__main__":
    myApp = App()
