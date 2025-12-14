import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math
import time

from camera import Camera
from maze import Maze
from render import Renderer


class MazeGame:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.maze_size = 21  # Tamanho do labirinto (deve ser ímpar)
        
        # Inicializar pygame
        pygame.init()
        self.display = (width, height)
        
        # Usar DOUBLEBUF para melhor desempenho
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
        
        # Estado do jogo
        self.game_start_time = time.time()
        self.final_time = 0.0 # Variável para congelar o tempo final
        
        # Configurar OpenGL
        self._setup_opengl()
        
        # Inicializar componentes
        self.maze = Maze(self.maze_size)
        self.camera = Camera()
        self.renderer = Renderer(self.maze)
        
        # Fontes para texto
        pygame.font.init()
        self.win_font_large = pygame.font.Font(None, 74)
        self.win_font_medium = pygame.font.Font(None, 36)
        
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
            self.fov = self.fov_min
        elif self.fov > self.fov_max:
            self.fov = self.fov_max
        self._update_projection()
    
    def _draw_win_message(self):
        """Desenhar mensagem de vitória usando Pygame 2D sobre OpenGL"""
        if not self.camera.has_won:
            return
        
        # Congelar o tempo final assim que a vitória ocorrer
        if self.final_time == 0.0:
            self.final_time = time.time() - self.game_start_time
            
        # 35000ms = 35 segundos para a mensagem. Se já passou, não desenha.
        if self.camera.win_time and pygame.time.get_ticks() - self.camera.win_time > 35000:
            return
            
        # Mudar para modo 2D para desenhar texto
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        # Inverte o eixo Y para que (0,0) seja no canto superior esquerdo (padrão Pygame)
        glOrtho(0, self.width, self.height, 0, -1, 1) 
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Desabilitar recursos 3D que podem interferir
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        
        # Criar uma superfície para o texto
        text_surface = pygame.Surface((600, 250), pygame.SRCALPHA)
        
        # Desenhar fundo semi-transparente
        text_surface.fill((0, 0, 0, 180))  # Preto com transparência
        
        # Desenhar textos
        win_text = self.win_font_large.render("VOCÊ VENCEU!", True, (0, 255, 0))
        
        # Usar o tempo congelado (self.final_time)
        time_text = self.win_font_medium.render(f"Tempo: {self.final_time:.1f} segundos", True, (255, 255, 0))
        
        # Mensagem de tempo restante para o menu
        if pygame.time.get_ticks() - self.camera.win_time < 35000:
             time_left = math.ceil((35000 - (pygame.time.get_ticks() - self.camera.win_time)) / 1000)
             more_text = self.win_font_medium.render(f"Voltando ao menu em {time_left} segundos...", True, (255, 255, 255))
        else:
             more_text = self.win_font_medium.render("Voltando ao menu...", True, (255, 255, 255))
        
        # Centralizar textos
        text_surface.blit(win_text, (300 - win_text.get_width() // 2, 50))
        text_surface.blit(more_text, (300 - more_text.get_width() // 2, 130))
        text_surface.blit(time_text, (300 - time_text.get_width() // 2, 180))
        
        # Converter a superfície para textura OpenGL
        # CORREÇÃO: Mudar o argumento 'flip_vertical' para False para corrigir a inversão
        texture_data = pygame.image.tostring(text_surface, "RGBA", False) 
        
        # Criar e configurar textura
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 600, 250, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        
        # Habilitar blending para transparência
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Desenhar quadrado com a textura
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(self.width//2 - 300, self.height//2 - 125)
        glTexCoord2f(1, 0); glVertex2f(self.width//2 + 300, self.height//2 - 125)
        glTexCoord2f(1, 1); glVertex2f(self.width//2 + 300, self.height//2 + 125)
        glTexCoord2f(0, 1); glVertex2f(self.width//2 - 300, self.height//2 + 125)
        glEnd()
        
        # Limpar
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glDeleteTextures([texture])
        
        # Restaurar estado 3D
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def handle_input(self):
        """Processar entrada do usuário"""
        keys = pygame.key.get_pressed()
        
        # Se o jogador já venceu, limitar controles
        if self.camera.has_won:
            # Ainda permitir ajustar FOV e sair
            if keys[K_PAGEUP] or keys[K_EQUALS]:
                self._adjust_fov(self.fov_step)
            if keys[K_PAGEDOWN] or keys[K_MINUS]: 
                self._adjust_fov(-self.fov_step)
        else:
            # Movimento normal
            move_speed = 0.1
            if keys[K_w]:  
                self.camera.move_forward(move_speed, self.maze)
            if keys[K_s]: 
                self.camera.move_backward(move_speed, self.maze)
            if keys[K_a]:
                self.camera.move_left(move_speed, self.maze)
            if keys[K_d]:
                self.camera.move_right(move_speed, self.maze)
            
            # Pular
            if keys[K_SPACE]:  
                self.camera.jump(self.maze)
        
        # Ajustar FOV (sempre permitido)
        if keys[K_PAGEUP] or keys[K_EQUALS]:
            self._adjust_fov(self.fov_step)
        if keys[K_PAGEDOWN] or keys[K_MINUS]: 
            self._adjust_fov(-self.fov_step)
        
        # Atualizar física (IMPORTANTE!)
        self.camera.update_physics(self.maze)
        
        # Mouse look quando capturado
        if self.mouse_captured:
            mouse_x, mouse_y = pygame.mouse.get_rel()
            self.camera.rotate(mouse_x * 0.5, mouse_y * 0.5)
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    
                    self.running = False
                if event.key == pygame.K_r:
                    # Resetar câmera
                    self.camera = Camera()
                    self.game_start_time = time.time()
                    self.final_time = 0.0 # Resetar o tempo final
                if event.key == pygame.K_BACKSPACE:
                    # Liberar mouse
                    if self.mouse_captured:
                        self._release_mouse()
                if event.key == pygame.K_f:
                    # Alternar FOV entre valores comuns
                    if self.fov == 90:
                        self.fov = 60
                    elif self.fov == 60:
                        self.fov = 120
                    else:
                        self.fov = 90
                    self._update_projection()
            if event.type == pygame.MOUSEBUTTONDOWN:
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
        
        # Desenhar mensagem de vitória se necessário
        if self.camera.has_won:
            self._draw_win_message()
        
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
        print("  R - Resetar câmera (e tempo)")
        print("  ESC - Retornar ao menu")
        print(f"  FOV atual: {self.fov}°")
        print("Obrigado por jogar - HAM")
        
        while self.running:
            self.handle_input()
            self.render()
            self.clock.tick(self.fps)
            
            # === CORREÇÃO: LÓGICA DE RETORNO AO MENU APÓS 35 SEGUNDOS ===
            if self.camera.has_won:
                # self.camera.win_time é em ms, 35000ms = 35 segundos
                if self.camera.win_time and pygame.time.get_ticks() - self.camera.win_time >= 35000:
                    self.running = False  # Sai do loop do jogo e volta para o menu
            
            # Mostrar FPS e FOV
            fps = self.clock.get_fps()
            mouse_status = "CAPTURADO" if self.mouse_captured else "LIVRE"
            grounded_status = "NO CHÃO" if self.camera.grounded else "NO AR"
            
            # Adicionar status de vitória
            win_status = "VENCEU!" if self.camera.has_won else "JOGANDO"
            
            # Calcular tempo decorrido (usar o tempo congelado se tiver vencido)
            elapsed_time = self.final_time if self.camera.has_won and self.final_time > 0.0 else (time.time() - self.game_start_time)

            pygame.display.set_caption(
                f"Labirinto 3D - FPS: {fps:.0f} - FOV: {self.fov}° - "
                f"Mouse: {mouse_status} - {grounded_status} - "
                f"Status: {win_status} - Tempo: {elapsed_time:.1f}s"
            )
        
        self._release_mouse()  # Liberar mouse ao sair
        pygame.quit()


if __name__ == "__main__":
    # Importar e executar o menu
    from menu import Menu
    menu = Menu()
    menu.executar()