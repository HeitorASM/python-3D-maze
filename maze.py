import random

class Maze:
    def __init__(self, size, cell_size=2.0): # Adicionado parâmetro cell_size
        if size % 2 == 0:
            size += 1
        
        self.size = size
        self.cell_size = cell_size # Define a largura de cada corredor/parede
        self.grid = [[1] * size for _ in range(size)]
        self._generate_maze()
        
        # Posições de início e fim baseadas na escala
        self.start = (1 * cell_size, 1 * cell_size)
        self.end = ((size - 2) * cell_size, (size - 2) * cell_size)
    
    def _generate_maze(self):
        self.grid[1][1] = 0
        stack = [(1, 1)]
        
        while stack:
            x, y = stack[-1]
            neighbors = []
            
            if y > 2 and self.grid[y - 2][x] == 1:
                neighbors.append((x, y - 2, x, y - 1))
            if y < self.size - 3 and self.grid[y + 2][x] == 1:
                neighbors.append((x, y + 2, x, y + 1))
            if x > 2 and self.grid[y][x - 2] == 1:
                neighbors.append((x - 2, y, x - 1, y))
            if x < self.size - 3 and self.grid[y][x + 2] == 1:
                neighbors.append((x + 2, y, x + 1, y))
            
            if neighbors:
                nx, ny, wx, wy = random.choice(neighbors)
                self.grid[ny][nx] = 0
                self.grid[wy][wx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
    
    def is_wall(self, x, z): # Alterado de (x, y) para (x, z) para clareza 3D
        """
        Verificar se uma posição no mundo 3D colide com uma parede na grade.
        Divide a posição real pelo cell_size para encontrar o índice inteiro na matriz.
        """
        grid_x = int(x / self.cell_size)
        grid_z = int(z / self.cell_size)
        
        if grid_x < 0 or grid_x >= self.size or grid_z < 0 or grid_z >= self.size:
            return True
        return self.grid[grid_z][grid_x] == 1
    
    def is_walkable(self, x, z):
        return not self.is_wall(x, z)
    
    def get_size(self):
        return self.size