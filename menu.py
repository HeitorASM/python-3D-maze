import pygame
import sys
from enum import Enum
import time
import os  # Adicionado para verificar existência de arquivos

PRETO = (0, 0, 0)
CINZA_ESCURO = (40, 40, 40)
CINZA_CLARO = (200, 200, 200)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (100, 150, 255)

class MenuState(Enum):
    PRINCIPAL = 1
    SOBRE = 2
    CONTROLES = 3
    SAIR = 4
    JOGANDO = 5


class Botao:
    def __init__(self, x, y, largura, altura, texto, cor_normal, cor_hover, cor_texto):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
        self.mouse_sobre = False
        
    def desenhar(self, tela, fonte):
        cor = self.cor_hover if self.mouse_sobre else self.cor_normal
        pygame.draw.rect(tela, cor, self.rect)
        pygame.draw.rect(tela, self.cor_texto, self.rect, 3)
        
        # Renderizar texto
        texto_surf = fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)
    
    def atualizar_mouse(self, pos_mouse):
        self.mouse_sobre = self.rect.collidepoint(pos_mouse)
    
    def foi_clicado(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)


class MenuPrincipal:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        
        # Configurar botões
        botao_x = largura // 2 - 150
        self.botao_jogar = Botao(botao_x, 250, 300, 60, "JOGAR", AZUL, VERDE, BRANCO)
        self.botao_sobre = Botao(botao_x, 330, 300, 60, "SOBRE", AZUL, VERDE, BRANCO)
        self.botao_controles = Botao(botao_x, 410, 300, 60, "CONTROLES", AZUL, VERDE, BRANCO)
        self.botao_sair = Botao(botao_x, 490, 300, 60, "SAIR", VERMELHO, (255, 100, 100), BRANCO)
        
        self.botoes = [self.botao_jogar, self.botao_sobre, self.botao_controles, self.botao_sair]
    
    def desenhar(self, tela, fonte_grande, fonte_media):
        tela.fill(CINZA_ESCURO)
        
        # Título
        titulo = fonte_grande.render("GLMaze", True, VERDE)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 100))
        tela.blit(titulo, titulo_rect)
        
        # Subtítulo
        subtitulo = fonte_media.render("Developed by HAM", True, CINZA_CLARO)
        subtitulo_rect = subtitulo.get_rect(center=(self.largura // 2, 180))
        tela.blit(subtitulo, subtitulo_rect)
        
        # Desenhar botões
        for botao in self.botoes:
            botao.desenhar(tela, fonte_media)
    
    def processar_evento(self, evento, click_sound):
        """Processar eventos do menu"""
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_jogar.foi_clicado(evento.pos):
                if click_sound:
                    click_sound.play()
                return MenuState.JOGANDO
            elif self.botao_sobre.foi_clicado(evento.pos):
                if click_sound:
                    click_sound.play()
                return MenuState.SOBRE
            elif self.botao_controles.foi_clicado(evento.pos):
                if click_sound:
                    click_sound.play()
                return MenuState.CONTROLES
            elif self.botao_sair.foi_clicado(evento.pos):
                if click_sound:
                    click_sound.play()
                return MenuState.SAIR
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if click_sound:
                    click_sound.play()
                return MenuState.SAIR
        
        return None
    
    def atualizar(self, pos_mouse):
        """Atualizar estado dos botões"""
        for botao in self.botoes:
            botao.atualizar_mouse(pos_mouse)


class TelaAbout:
    """Tela de informações sobre o projeto"""
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.botao_voltar = Botao(largura // 2 - 150, altura - 100, 300, 60, "VOLTAR", AZUL, VERDE, BRANCO)
        
        self.informacoes = [
            "GLMaze v0.0.2",
            "Um jogo de exploração em 3D onde você",
            "precisa encontrar a saída de um labirinto gerado",
            "proceduralmente usando algoritmo de Depth-First Search.",
            "OBJETIVO:",
            "Encontre a esfera verde para vencer!",
            "DESENVOLVIDO POR:",
            "HAM",
            "DATA DE CRIAÇÃO:",
            "13 de Dezembro de 2025",
            "TECNOLOGIAS UTILIZADAS:",
            "• Python 3",
            "• Pygame",
            "• OpenGL (PyOpenGL)",
            "• NumPy",
        ]
    
    def desenhar(self, tela, fonte_grande, fonte_pequena):
        tela.fill(CINZA_ESCURO)
        
        # Título
        titulo = fonte_grande.render("SOBRE", True, VERDE)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 30))
        tela.blit(titulo, titulo_rect)
        
        # Informações
        y_offset = 100
        for linha in self.informacoes:
            if linha:
                texto = fonte_pequena.render(linha, True, CINZA_CLARO)
            else:
                texto = fonte_pequena.render(" ", True, CINZA_CLARO)
            
            texto_rect = texto.get_rect(center=(self.largura // 2, y_offset))
            tela.blit(texto, texto_rect)
            y_offset += 30
        
        # Botão voltar
        self.botao_voltar.desenhar(tela, fonte_pequena)
    
    def processar_evento(self, evento, click_sound):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_voltar.foi_clicado(evento.pos):
                if click_sound:
                    click_sound.play()
                return MenuState.PRINCIPAL
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if click_sound:
                    click_sound.play()
                return MenuState.PRINCIPAL
        
        return None
    
    def atualizar(self, pos_mouse):
        """Atualizar estado"""
        self.botao_voltar.atualizar_mouse(pos_mouse)


class TelaControles:
    """Tela de informações dos controles"""
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.botao_voltar = Botao(largura // 2 - 150, altura - 100, 300, 60, "VOLTAR", AZUL, VERDE, BRANCO)
        
        self.controles = [
            "CONTROLES DO JOGO",
            "",
            "MOVIMENTO:",
            "W ........................ ....  Mover para frente",
            "S ........................ .... Mover para trás",
            "A ............................  Mover para esquerda",
            "D ............................ Mover para direita",
            "ESPAÇO ....................... Subir",
            "CTRL .........................  Descer",
            "",
            "CAMERA/VISUALIZAÇÃO:",
            "Clique esquerdo do mouse ....  Capturar mouse (Look Around)",
            "BACKSPACE ....................  Liberar mouse",
            "",
            "ZOOM:",
            "+/- ou SCROLL do mouse .. .... Ajustar FOV (Field of View)",
            "F ............................ Alternar FOV (60°/90°/120°)",
            "",
            "GERAL:",
            "R ............................ Resetar posição da câmera",
            "ESC ..........................  Retornar ao menu",
        ]
    
    def desenhar(self, tela, fonte_grande, fonte_pequena):
        tela.fill(CINZA_ESCURO)
        
        titulo = fonte_grande.render("CONTROLES", True, VERDE)
        titulo_rect = titulo.get_rect(center=(self.largura // 2, 20))
        tela.blit(titulo, titulo_rect)
        
        y_offset = 80
        for linha in self.controles:
            if linha:
                texto = fonte_pequena.render(linha, True, CINZA_CLARO)
            else:
                texto = fonte_pequena.render(" ", True, CINZA_CLARO)
            
            texto_rect = texto.get_rect(topleft=(30, y_offset))
            tela.blit(texto, texto_rect)
            y_offset += 25
        
        # Botão voltar
        self.botao_voltar.desenhar(tela, fonte_pequena)
    
    def processar_evento(self, evento, click_sound):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_voltar.foi_clicado(evento.pos):
                if click_sound:
                    click_sound.play()
                return MenuState.PRINCIPAL
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if click_sound:
                    click_sound.play()
                return MenuState.PRINCIPAL
        
        return None
    
    def atualizar(self, pos_mouse):
        self.botao_voltar.atualizar_mouse(pos_mouse)


class Menu:
    def __init__(self, largura=1200, altura=800):
        self.largura = largura
        self.altura = altura
        pygame.init() # Inicializa Pygame aqui
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Labirinto 3D - Menu")
        
        self.relogio = pygame.time.Clock()
        self.executando = True
        self.estado_atual = MenuState.PRINCIPAL
        self.fps = 60

        self.fonte_grande = pygame.font.Font(None, 70)
        self.fonte_media = pygame.font.Font(None, 40)
        self.fonte_pequena = pygame.font.Font(None, 25)
        
        # Inicializar mixer de áudio
        pygame.mixer.init()
        
        # Carregar som de clique
        self.click_sound = None
        sound_path = "Assets/audio/click1.ogg"
        
        if os.path.exists(sound_path):
            try:
                self.click_sound = pygame.mixer.Sound(sound_path)
                self.click_sound.set_volume(0.5)  # Volume ajustável
                print(f"Som de clique carregado: {sound_path}")
            except Exception as e:
                print(f"Erro ao carregar som: {e}")
                self.click_sound = None
        else:
            print(f"Arquivo de som não encontrado: {sound_path}")
            print("Continuando sem som...")
        
        # Telas
        self.menu_principal = MenuPrincipal(largura, altura)
        self.tela_about = TelaAbout(largura, altura)
        self.tela_controles = TelaControles(largura, altura)
    
    def processar_eventos(self):
        """Processar eventos"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.executando = False
                return
            
            novo_estado = None
            
            if self.estado_atual == MenuState.PRINCIPAL:
                novo_estado = self.menu_principal.processar_evento(evento, self.click_sound)
            elif self.estado_atual == MenuState.SOBRE:
                novo_estado = self.tela_about.processar_evento(evento, self.click_sound)
            elif self.estado_atual == MenuState.CONTROLES:
                novo_estado = self.tela_controles.processar_evento(evento, self.click_sound)
            
            if novo_estado:
                self.estado_atual = novo_estado
    
    def atualizar(self):
        """Atualizar estado do menu"""
        pos_mouse = pygame.mouse.get_pos()
        
        if self.estado_atual == MenuState.PRINCIPAL:
            self.menu_principal.atualizar(pos_mouse)
        elif self.estado_atual == MenuState.SOBRE:
            self.tela_about.atualizar(pos_mouse)
        elif self.estado_atual == MenuState.CONTROLES:
            self.tela_controles.atualizar(pos_mouse)
        
        if self.estado_atual == MenuState.SAIR:
            self.executando = False
        elif self.estado_atual == MenuState.JOGANDO:
            self.iniciar_jogo()
    
    def desenhar(self):
        """Desenhar o menu"""
        if self.estado_atual == MenuState.PRINCIPAL:
            self.menu_principal.desenhar(self.tela, self.fonte_grande, self.fonte_media)
        elif self.estado_atual == MenuState.SOBRE:
            self.tela_about.desenhar(self.tela, self.fonte_grande, self.fonte_pequena)
        elif self.estado_atual == MenuState.CONTROLES:
            self.tela_controles.desenhar(self.tela, self.fonte_grande, self.fonte_pequena)
        
        pygame.display.flip()
    
    def iniciar_jogo(self):
        """Iniciar o jogo principal"""
        print("Iniciando o jogo...")
        pygame.quit()
        
        # Importar e executar o jogo
        from main import MazeGame
        game = MazeGame()
        game.run()
        
        # --- CORREÇÃO: Reinicializa o Pygame e o menu para permitir o retorno ---
        
        # Reinicializar Pygame (perdido após pygame.quit() acima)
        pygame.init()
        
        # Reinicializar mixer de áudio
        pygame.mixer.init()
        
        # Recarregar som de clique após reinicialização
        sound_path = "Assets/audio/click1.ogg"
        if os.path.exists(sound_path):
            try:
                self.click_sound = pygame.mixer.Sound(sound_path)
                self.click_sound.set_volume(0.5)
            except Exception as e:
                print(f"Erro ao recarregar som: {e}")
                self.click_sound = None
        
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Labirinto 3D - Menu")
        
        # Redefinir fontes
        pygame.font.init() 
        self.fonte_grande = pygame.font.Font(None, 70)
        self.fonte_media = pygame.font.Font(None, 40)
        self.fonte_pequena = pygame.font.Font(None, 25)
        
        self.estado_atual = MenuState.PRINCIPAL
        self.executando = True 
    
    def executar(self):
        """Loop principal do menu"""
        print("=== Menu do Labirinto 3D ===")
        print("Menu iniciado com sucesso!")
        
        while self.executando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(self.fps)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__": 
    menu = Menu()
    menu.executar()