"""
Sistema de renderização do labirinto
"""
from OpenGL.GL import *
from OpenGL.GLU import *


class Renderer:
    def __init__(self, maze):
        self.maze = maze
        self.cell_size = 1.0
        self.wall_height = 2.0
    
    def draw_maze(self):
        """Desenhar o labirinto"""
        size = self.maze.get_size()
        
        # Desenhar cada célula
        for y in range(size):
            for x in range(size):
                if self.maze.is_wall(x, y):
                    self.draw_cube(
                        x * self.cell_size,
                        self.wall_height / 2,
                        y * self.cell_size,
                        self.cell_size
                    )
        
        # Desenhar piso
        self.draw_floor(size)
        
        # Desenhar marcadores de saída
        self.draw_end_marker()
    
    
    # so eu e Deus sabiamos oque como e porque isso funciona hoje apenas Deus sabe
    def draw_cube(self, x, y, z, size):

        half_size = size / 2.0
        
        glPushMatrix()
        glTranslatef(x + half_size, y, z + half_size)
        
        # Cor das paredes (cinza)
        glColor3f(0.5, 0.5, 0.5)
        
        glBegin(GL_QUADS)
        
        # Face frontal
        glColor3f(0.6, 0.6, 0.6)
        glNormal3f(0, 0, 1)
        glVertex3f(-half_size, -y, half_size)
        glVertex3f(half_size, -y, half_size)
        glVertex3f(half_size, y, half_size)
        glVertex3f(-half_size, y, half_size)
        
        # Face traseira
        glColor3f(0.5, 0.5, 0.5)
        glNormal3f(0, 0, -1)
        glVertex3f(-half_size, -y, -half_size)
        glVertex3f(-half_size, y, -half_size)
        glVertex3f(half_size, y, -half_size)
        glVertex3f(half_size, -y, -half_size)
        
        # Face topo
        glColor3f(0.7, 0.7, 0.7)
        glNormal3f(0, 1, 0)
        glVertex3f(-half_size, y, -half_size)
        glVertex3f(-half_size, y, half_size)
        glVertex3f(half_size, y, half_size)
        glVertex3f(half_size, y, -half_size)
        
        # Face base
        glColor3f(0.4, 0.4, 0.4)
        glNormal3f(0, -1, 0)
        glVertex3f(-half_size, -y, -half_size)
        glVertex3f(half_size, -y, -half_size)
        glVertex3f(half_size, -y, half_size)
        glVertex3f(-half_size, -y, half_size)
        
        # Face esquerda
        glColor3f(0.55, 0.55, 0.55)
        glNormal3f(-1, 0, 0)
        glVertex3f(-half_size, -y, -half_size)
        glVertex3f(-half_size, -y, half_size)
        glVertex3f(-half_size, y, half_size)
        glVertex3f(-half_size, y, -half_size)
        
        # Face direita
        glColor3f(0.65, 0.65, 0.65)
        glNormal3f(1, 0, 0)
        glVertex3f(half_size, -y, -half_size)
        glVertex3f(half_size, y, -half_size)
        glVertex3f(half_size, y, half_size)
        glVertex3f(half_size, -y, half_size)
        
        glEnd()
        glPopMatrix()
    
    #o chção da mo labirinto mais não tem colição 
    def draw_floor(self, size):
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        
        glNormal3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(size * self.cell_size, 0, 0)
        glVertex3f(size * self.cell_size, 0, size * self.cell_size)
        glVertex3f(0, 0, size * self.cell_size)
        
        glEnd()
    
    def draw_end_marker(self):

        glColor3f(0.0, 1.0, 0.0)
        glPushMatrix()
        
        end_x = (self.maze.size - 2) * self.cell_size + self.cell_size / 2
        end_z = (self.maze.size - 2) * self.cell_size + self.cell_size / 2
        
        glTranslatef(end_x, 0.1, end_z)
        
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.3, 16, 16)
        
        glPopMatrix()