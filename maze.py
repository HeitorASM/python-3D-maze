import random


class Maze:
    def __init__(self, size):
        if size % 2 == 0:
            size += 1
        
        self.size = size
        self. grid = [[1] * size for _ in range(size)]
        self._generate_maze()
        self. start = (1, 1)
        self.end = (size - 2, size - 2)
    
    def _generate_maze(self):
        # Marcar posição inicial como caminho
        self.grid[1][1] = 0
    
        stack = [(1, 1)]
        
        while stack:
            x, y = stack[-1]
            
            neighbors = []
            
            # Acima
            if y > 2 and self.grid[y - 2][x] == 1:
                neighbors.append((x, y - 2, x, y - 1))
            # Abaixo
            if y < self.size - 3 and self.grid[y + 2][x] == 1:
                neighbors.append((x, y + 2, x, y + 1))
            # Esquerda
            if x > 2 and self.grid[y][x - 2] == 1:
                neighbors.append((x - 2, y, x - 1, y))
            # Direita
            if x < self.size - 3 and self.grid[y][x + 2] == 1:
                neighbors.append((x + 2, y, x + 1, y))
            
            if neighbors:
                # Escolher vizinho aleatório
                nx, ny, wx, wy = random.choice(neighbors)
                
                # Marcar como caminho
                self.grid[ny][nx] = 0
                self.grid[wy][wx] = 0
                
                stack.append((nx, ny))
            else:
                stack.pop()
    
    def is_wall(self, x, y):
        """Verificar se uma posição é uma parede"""
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return True
        return self.grid[int(y)][int(x)] == 1
    
    def is_walkable(self, x, y):
        """Verificar se uma posição é transitável"""
        return not self.is_wall(x, y)
    
    def get_size(self):
        """Retornar tamanho do labirinto"""
        return self.size