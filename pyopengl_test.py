import sys
import math
import numpy as np
import pygame
from pygame.locals import *

import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *

import unittest

def defineTube(sides:int):
    """ Defines a cylinder without caps and returns it as a three dimensional array (quad, vert, axis). """
    geom = np.zeros((sides, 4, 3))
   
    print (geom.ndim)
    print (geom.shape)
    for i in range(sides):               
        geom[i,0,0] = math.sin(math.pi * 2 / sides * i) * 5.0
        geom[i,0,1] = math.cos(math.pi * 2 / sides * i) * 5.0 
        geom[i,0,2] = -5.0

        geom[i,1,0] = math.sin(math.pi * 2 / sides * i) * 5.0
        geom[i,1,1] = math.cos(math.pi * 2 / sides * i) * 5.0
        geom[i,1,2] = 5.0

        geom[i,2,0] = math.sin(math.pi * 2 / sides * (i + 1)) * 5.0
        geom[i,2,1] = math.cos(math.pi * 2 / sides * (i + 1)) * 5.0
        geom[i,2,2] = 5.0

        geom[i,3,0] = math.sin(math.pi * 2 / sides * (i + 1)) * 5.0
        geom[i,3,1] = math.cos(math.pi * 2 / sides * (i + 1)) * 5.0
        geom[i,3,2] = -5.0  
    return geom

class model():
    """ Defines a 3D geometry and its drawing method. """ 
    geom = np.empty(shape = (0,0,0))

    def draw(self):
        """ Draws the model using OpenGL calls. """
        count = 0

        for i in range(np.ma.size(self.geom,axis=0)):            
            # Alternate between 2 colours           
            if (i % 2 == 1):
                glColor3f(0.3, 0.5, 0.9)
            else:
                glColor3f(0.3, 0.6, 0.9)

            # Tell OpenGL to draw the quad
            glBegin(GL_QUADS)
            for vert in range(4):           
                glVertex3fv(self.geom[i,vert])
            glEnd()

    def __init__(self):
        self.geom = defineTube(16)

def init():
    """ Initializes pygame + OpenGL and sets up a display window and viewing frustum. """    
    pygame.init()
    pygame.display.set_caption("PyOpenGL Test")
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST);    
    glTranslatef(0.0, 0.0, -15)    

def main():
    init()   
    model_a = model()

    while True:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        model_a.draw()

        glRotatef(1, 0.5, 1, 1)
        
        pygame.display.flip()
        pygame.time.wait(5)

        # Listen to quit event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

class SimpleTest(unittest.TestCase):
    # Model should have the defined amount of sides
    def test_defineTube1(self):
        self.assertEqual(len(defineTube(16)), 16)
    def test_defineTube2(self):
        self.assertEqual(len(defineTube(32)), 32)  
    # Each side should have 4 vertices      
    def test_defineTube3(self):
        quads = defineTube(16)
        for quad in quads:
            self.assertEqual(len(quad), 4)          

if __name__ == "__main__":
    #unittest.main()
    main()