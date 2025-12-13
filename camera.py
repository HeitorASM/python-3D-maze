import math
import numpy as np
# por emqunto a camera serve como controler do jogador porem vou consertar para ter um arquivo para controlar o movimento 
# devido a essa falta de controles finos de movimento a camera se comporta commo uma camera ela vai para cima para baixo mais não e afetada pela gravidde
# vou adicionar tambem uma em breve um modelo que presta para a camera e tambem um hud/mapa mais por enquanto ta bom 
# -HAM 12/12/25

class Camera:
    def __init__(self, x=1.5, y=1.5, z=1.5):
        self.x = x
        self.y = y
        self.z = z
        
        # Ângulos de rotação e etc
        self.yaw = 0.0  # Rotação horizontal
        self.pitch = 0.0  # Rotação vertical
        
        # Altura do olho
        self.height = 1.7  
        
        self.speed = 0.15
        
        self.capsule_radius = 0.3
        self.capsule_height = 2.0  # Altura total da cápsula
        self.capsule_half_height = self.capsule_height / 2.0
        
        self.prev_x = x
        self.prev_z = z
    
    def apply(self):
        """Aplicar transformação da câmera"""
        from OpenGL.GL import glRotatef, glTranslatef
        
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.yaw, 0, 1, 0)
        glTranslatef(-self.x, -(self.y + self.height), -self.z)
    
    def rotate(self, yaw_delta, pitch_delta):
        """Rotacionar câmera"""
        self.yaw += yaw_delta
        self.pitch += pitch_delta
        
        # Limitar pitch para não virar de cabeça para baixo/cima demais
        if self.pitch > 89:
            self.pitch = 89
        if self.pitch < -89:
            self.pitch = -89
    
    def move_forward(self, distance):
        """Mover para frente"""
        self.prev_x = self.x
        self.prev_z = self.z
        
        rad_yaw = math.radians(self.yaw)
        self.x += math.sin(rad_yaw) * distance
        self.z -= math.cos(rad_yaw) * distance
    
    def move_backward(self, distance):
        """Mover para trás"""
        self.move_forward(-distance)
    
    def move_left(self, distance):
        """Mover para esquerda"""
        self.prev_x = self.x
        self.prev_z = self.z
        
        rad_yaw = math.radians(self.yaw)
        self.x -= math.cos(rad_yaw) * distance
        self.z -= math.sin(rad_yaw) * distance
    
    def move_right(self, distance):
        """Mover para direita"""
        self.move_left(-distance)
    
    def move_up(self, distance):
        """Mover para cima"""
        self.prev_x = self.x
        self.prev_z = self.z
        self.y += distance
    
    def move_down(self, distance):
        """Mover para baixo"""
        self.prev_x = self.x
        self.prev_z = self.z
        self.y -= distance
    
    def check_capsule_collision(self, maze):
        base_y = self.y
        
        # Verificar colisão em múltiplos pontos verticais da cápsula
        num_vertical_checks = 3
        collision_occurred = False
        
        for i in range(num_vertical_checks):
            # Calcular altura do ponto de verificação
            vertical_ratio = i / (num_vertical_checks - 1) if num_vertical_checks > 1 else 0.5
            check_y = base_y + (self.capsule_height * vertical_ratio)
            
            if self._check_circle_collision(maze, self.x, check_y, self.z):
                collision_occurred = True
                break
        #isso reverte a posição se houver colisão (remover isso porque ta calsando bugs muito pesados e tão forte que quase da epilepisia )
        if collision_occurred:
            self.x = self.prev_x
            self.z = self.prev_z
            return True
        
        self.prev_x = self.x
        self.prev_z = self.z
        return False
    
    def _check_circle_collision(self, maze, center_x, center_y, center_z):
        """Verificar colisão circular em uma altura específica"""
        num_points = 16
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            dx = math.cos(angle) * self.capsule_radius
            dz = math.sin(angle) * self.capsule_radius
            
            # Verificar colisão em vários pontos ao redor do círculo
            check_x = center_x + dx
            check_z = center_z + dz
            
            if maze.is_wall(check_x, check_z):
                return True
        
        # Verificar também o ponto central
        if maze.is_wall(center_x, center_z):
            return True
        
        return False
    
    def check_collision(self, maze):
        """Interface compatível - agora usando cápsula"""
        return self.check_capsule_collision(maze)