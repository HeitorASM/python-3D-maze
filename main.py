import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math

from camera import Camera
from maze import Maze
from render import Renderer


class MazeGame:
    def __init__(self, width=1200, height=800):
        self.width = width
        self. height = height
        self.maze_size = 21  # Tamanho do labirinto (deve ser ímpar)
        
        # Inicializar pygame
        pygame.init()
        self.display = (width, height)
        self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Labirinto 3D")
        
        # Configurações de FOV
        self.fov = 90  # Campo de visão inicial (em graus)
        self.fov_min = 30
        self.fov_max = 120
        self.fov_step = 5
        
        # Controle de mouse
        self.mouse_captured = False
        self.last_mouse_pos = (0, 0)
        
        # Configurar OpenGL
        self._setup_opengl()
        
        # Inicializar componentes
        self.maze = Maze(self.maze_size)
        self.camera = Camera()
        self.renderer = Renderer(self.maze)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
    def _setup_opengl(self):
        """Configurar projeção e iluminação OpenGL"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Configurar luz
        light_pos = (10, 10, 10, 0)
        glLight(GL_LIGHT0, GL_POSITION, light_pos)
        glLight(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
        glLight(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
        glLight(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
        
        # Configurar perspectiva com FOV ajustável
        self._update_projection()
        
    def _update_projection(self):
        """Atualizar projeção com FOV atual"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, (self.width / self.height), 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW)
    
    def _capture_mouse(self):
        """Capturar mouse (esconder cursor e travar na janela)"""
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        pygame.mouse.set_pos(self.width // 2, self.height // 2)
        self.last_mouse_pos = pygame.mouse.get_pos()
        self.mouse_captured = True
    
    def _release_mouse(self):
        """Liberar mouse (mostrar cursor e destravar)"""
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        self.mouse_captured = False
    
    def _adjust_fov(self, delta):
        """Ajustar FOV"""
        self.fov += delta
        if self.fov < self.fov_min:
            self.fov = self. fov_min
        elif self.fov > self.fov_max:
            self. fov = self.fov_max
        self._update_projection()
    
    def handle_input(self):
        """Processar entrada do usuário"""
        keys = pygame.key.get_pressed()
        
        # Movimento
        move_speed = 0.1
        if keys[K_w]:  
            self.camera.move_forward(move_speed, self.maze)
        if keys[K_s]: 
            self.camera.move_backward(move_speed, self. maze)
        if keys[K_a]:
            self.camera.move_left(move_speed, self.maze)
        if keys[K_d]:
            self.camera.move_right(move_speed, self.maze)
        
        # Pular (substitui move_up)
        if keys[K_SPACE]:  
            self.camera.jump(self.maze)
        
        # Remover move_down - agora controlado por gravidade
        
        # Ajustar FOV
        if keys[K_PAGEUP] or keys[K_EQUALS]:
            self._adjust_fov(self.fov_step)
        if keys[K_PAGEDOWN] or keys[K_MINUS]: 
            self._adjust_fov(-self.fov_step)
        
        # Atualizar física (IMPORTANTE!)
        self.camera.update_physics(self.maze)
        
        # Mouse look quando capturado
        if self. mouse_captured:
            mouse_x, mouse_y = pygame.mouse.get_rel()
            self.camera.rotate(mouse_x * 0.5, mouse_y * 0.5)
        
        # Eventos
        for event in pygame.event.get():
            if event. type == pygame.QUIT:
                self. running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    
                    self. running = False
                if event. key == pygame.K_r:
                    # Resetar câmera
                    self.camera = Camera()
                if event.key == pygame.K_BACKSPACE:
                    # Liberar mouse
                    if self.mouse_captured:
                        self._release_mouse()
                if event.key == pygame.K_f:
                    # Alternar FOV entre valores comuns
                    if self.fov == 90:
                        self. fov = 60
                    elif self.fov == 60:
                        self.fov = 120
                    else:
                        self.fov = 90
                    self._update_projection()
            if event.type == pygame. MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    if not self.mouse_captured:
                        self._capture_mouse()
                elif event.button == 4:  # Scroll up
                    self._adjust_fov(self.fov_step)
                elif event.button == 5:  # Scroll down
                    self._adjust_fov(-self.fov_step)
    
    def render(self):
        """Renderizar frame"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        
        glLoadIdentity()
        self.camera.apply()
        
        self.renderer.draw_maze()
        
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        print("=== Labirinto 3D ===")
        print("Controles:")
        print("  W/A/S/D - Movimento")
        print("  ESPAÇO - Pular")
        print("  Clique esquerdo - Capturar mouse")
        print("  BACKSPACE - Liberar mouse")
        print("  +/- ou SCROLL - Ajustar FOV")
        print("  F - Alternar entre FOVs comuns (60/90/120)")
        print("  R - Resetar câmera")
        print("  ESC - Retornar ao menu")
        print(f"  FOV atual: {self.fov}°")
        print("Obrigado por jogar - HAM")
        
        while self.running:
            self.handle_input()
            self.render()
            self.clock.tick(self.fps)
            
            # Mostrar FPS e FOV
            fps = self.clock.get_fps()
            mouse_status = "CAPTURADO" if self.mouse_captured else "LIVRE"
            grounded_status = "NO CHÃO" if self.camera.grounded else "NO AR"
            pygame.display.set_caption(f"Labirinto 3D - FPS: {fps:.0f} - FOV: {self.fov}° - Mouse: {mouse_status} - {grounded_status}")
        
        self._release_mouse()  # Liberar mouse ao sair
        pygame.quit()


if __name__ == "__main__":
    # Importar e executar o menu
    from menu import Menu
    menu = Menu()
    menu.executar()
