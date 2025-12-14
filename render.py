from OpenGL.GL import *
from OpenGL.GLU import *

class Renderer:
    def __init__(self, maze):
        self.maze = maze
        self.cell_size = maze.cell_size # Puxa a escala definida no labirinto
        self.wall_height = 2.5 # Altura das paredes ajustável
    
    def draw_maze(self):
        size = self.maze.get_size()
        
        for y in range(size):
            for x in range(size):
                # Acessa a grade lógica para decidir onde desenhar cubos
                if self.maze.grid[y][x] == 1:
                    self.draw_cube(
                        x * self.cell_size,
                        self.wall_height / 2,
                        y * self.cell_size,
                        self.cell_size
                    )
        
        self.draw_floor(size)
        self.draw_end_marker()
    
    def draw_cube(self, x, y, z, size):
        half_size = size / 2.0
        
        glPushMatrix()
        glTranslatef(x + half_size, y, z + half_size)
        
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
    
    def draw_floor(self, size):
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        # O piso cobre toda a área multiplicada pela escala
        full_size = size * self.cell_size
        glVertex3f(0, 0, 0)
        glVertex3f(full_size, 0, 0)
        glVertex3f(full_size, 0, full_size)
        glVertex3f(0, 0, full_size)
        glEnd()
    
    def draw_end_marker(self):
        glColor3f(0.0, 1.0, 0.0)
        glPushMatrix()
        # Posiciona a esfera de saída usando a escala
        end_x = (self.maze.size - 2) * self.cell_size + self.cell_size / 2
        end_z = (self.maze.size - 2) * self.cell_size + self.cell_size / 2
        glTranslatef(end_x, 0.5, end_z)
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.4, 16, 16)
        glPopMatrix()