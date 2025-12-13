import math
import numpy as np

class Camera:
    def __init__(self, x=1.5, y=1.5, z=1.5):
        self.x = x
        self. y = y
        self.z = z
        
        # Ângulos de rotação
        self. yaw = 0.0  # Rotação horizontal
        self.pitch = 0.0  # Rotação vertical
        
        # Altura do olho
        self.height = 1.7  
        
        self. speed = 0.15
        
        # Colisor em forma de cápsula
        self.capsule_radius = 0.3
        self.capsule_height = 2.0
        self.capsule_half_height = self.capsule_height / 2.0
        
        # Posições anteriores para rollback de colisão
        self.prev_x = x
        self.prev_y = y
        self.prev_z = z
        
        # === FÍSICA E GRAVIDADE ===
        self.velocity_y = 0.0  # Velocidade vertical
        self.gravity = -0.015  # Aceleração para baixo (ajustável)
        self.grounded = False  # Se está no chão
        self.ground_level = 0.0  # Nível do piso
        self.max_height = 15.0  # Altura máxima permitida
        self.jump_strength = 0.3  # Força do pulo (ajustável)
    
    def apply(self):
        """Aplicar transformação da câmera"""
        from OpenGL.GL import glRotatef, glTranslatef
        
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self. yaw, 0, 1, 0)
        glTranslatef(-self.x, -(self.y + self.height), -self.z)
    
    def rotate(self, yaw_delta, pitch_delta):
        """Rotacionar câmera"""
        self.yaw += yaw_delta
        self.pitch += pitch_delta
        
        # Limitar pitch
        if self.pitch > 89:  
            self.pitch = 89
        if self.pitch < -89:
            self.pitch = -89
    
    def move_forward(self, distance, maze):
        """Mover para frente (com detecção de colisão por eixo)"""
        rad_yaw = math.radians(self.yaw)
        dx = math.sin(rad_yaw) * distance
        dz = -math.cos(rad_yaw) * distance
        
        # Guardar posição anterior
        old_x, old_z = self.x, self.z
        
        # Tentar mover em X
        self.x += dx
        if self._check_circle_collision(maze, self.x, self.y, self.z):
            self.x = old_x
        
        # Tentar mover em Z
        self.z += dz
        if self._check_circle_collision(maze, self.x, self. y, self.z):
            self.z = old_z
    
    def move_backward(self, distance, maze):
        """Mover para trás"""
        self.move_forward(-distance, maze)
    
    def move_left(self, distance, maze):
        """Mover para esquerda (com detecção de colisão por eixo)"""
        rad_yaw = math.radians(self.yaw)
        dx = -math.cos(rad_yaw) * distance
        dz = -math. sin(rad_yaw) * distance
        
        old_x, old_z = self.x, self.z
        
        # Tentar mover em X
        self.x += dx
        if self._check_circle_collision(maze, self. x, self.y, self. z):
            self.x = old_x
        
        # Tentar mover em Z
        self.z += dz
        if self._check_circle_collision(maze, self.x, self.y, self.z):
            self.z = old_z
    
    def move_right(self, distance, maze):
        """Mover para direita"""
        self.move_left(-distance, maze)
    
    def jump(self, maze):
        """Pular (só funciona se estiver no chão)"""
        if self.grounded:
            self. velocity_y = self.jump_strength
            self.grounded = False
    
    def update_physics(self, maze):
        """
        Atualizar física:  aplicar gravidade, checar colisões verticais,
        e garantir que o jogador não flutua nem cai infinitamente.
        """
        # Aplicar gravidade
        self.velocity_y += self.gravity
        
        # Calcular próxima posição vertical
        next_y = self. y + self.velocity_y
        
        # Impedir cair abaixo do chão
        if next_y < self.ground_level:
            next_y = self.ground_level
            self.velocity_y = 0
            self.grounded = True
        
        # Impedir subir acima da altura máxima
        elif next_y > self.max_height:
            next_y = self.max_height
            self.velocity_y = 0
        
        # Checar colisão vertical (com vários pontos da cápsula)
        collision_occurred = False
        num_vertical_checks = 3
        
        for i in range(num_vertical_checks):
            vertical_ratio = i / (num_vertical_checks - 1) if num_vertical_checks > 1 else 0.5
            check_y = next_y + (self.capsule_height * vertical_ratio)
            
            if self._check_circle_collision(maze, self.x, check_y, self.z):
                collision_occurred = True
                break
        
        if collision_occurred: 
            # Se está caindo e bate em algo, para
            if self.velocity_y < 0:
                self.grounded = True
            # Se está subindo e bate em teto, para
            self.velocity_y = 0
        else:
            # Sem colisão, atualizar posição
            self. y = next_y
            self. grounded = False
    
    def check_capsule_collision(self, maze):
        """Verificar colisão da cápsula com paredes (mantido para compatibilidade)"""
        base_y = self.y
        
        num_vertical_checks = 3
        collision_occurred = False
        
        for i in range(num_vertical_checks):
            vertical_ratio = i / (num_vertical_checks - 1) if num_vertical_checks > 1 else 0.5
            check_y = base_y + (self.capsule_height * vertical_ratio)
            
            if self._check_circle_collision(maze, self.x, check_y, self.z):
                collision_occurred = True
                break
        
        return collision_occurred
    
    def _check_circle_collision(self, maze, center_x, center_y, center_z):
        """Verificar colisão circular em uma altura específica"""
        num_points = 16
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            dx = math.cos(angle) * self.capsule_radius
            dz = math.sin(angle) * self.capsule_radius
            
            check_x = center_x + dx
            check_z = center_z + dz
            
            if maze. is_wall(check_x, check_z):
                return True
        
        # Verificar também o ponto central
        if maze.is_wall(center_x, center_z):
            return True
        
        return False
    
    def check_collision(self, maze):
        """Interface compatível - agora usando cápsula"""
        return self.check_capsule_collision(maze)
