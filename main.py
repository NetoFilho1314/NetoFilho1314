import os
import sys
import pygame
import random

def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Inicialize o pygame e o mixer
pygame.init()
pygame.mixer.init()

# Configura a largura e altura da janela
width, height = 1000, 700

# Cria a janela
screen = pygame.display.set_mode((width, height))

# Define o título da janela
pygame.display.set_caption('Stikman World')

# Carrega a imagem do fundo
background_image = pygame.image.load(resource_path('resources/sprites/background0.png'))
background_image = pygame.transform.scale(background_image, (width, height))

# O restante do seu código...

# Define a paleta de blocos com as cores representativas
def load_palette_from_colors(width, height):
    palette = []
    
    # Bloco de grama (verde no topo, marrom embaixo)
    grass_tile = pygame.Surface((width, height))
    grass_tile.fill((0, 255, 0))  # Verde
    pygame.draw.rect(grass_tile, (139, 69, 19), pygame.Rect(0, height // 2, width, height // 2))  # Marrom
    palette.append(grass_tile)
    
    # Bloco de terra (marrom)
    dirt_tile = pygame.Surface((width, height))
    dirt_tile.fill((139, 69, 19))  # Marrom
    palette.append(dirt_tile)
    
    # Bloco de pedra (cinza)
    stone_tile = pygame.Surface((width, height))
    stone_tile.fill((128, 128, 128))  # Cinza
    palette.append(stone_tile)
    
    # Bloco de areia (cor de areia)
    sand_tile = pygame.Surface((width, height))
    sand_tile.fill((255, 255, 178))  # Cor de areia
    palette.append(sand_tile)
    
    # Bloco de diamante (azul brilhante)
    diamond_tile = pygame.Surface((width, height))
    diamond_tile.fill((0, 255, 255))  # Azul brilhante
    palette.append(diamond_tile)
    
    return palette

# Tamanho dos blocos
tile_width = 50
tile_height = 50

# Carregar a paleta a partir das cores definidas
palette = load_palette_from_colors(tile_width, tile_height)

# Lista para armazenar os blocos e seus tiles
blocks = []

# Índice do tile atual
current_tile = 0  # índice do tile atual

# Paleta de blocos (usada para seleção)
palette_rects = []
palette_margin = 10
scroll_offset = 0

# Configura o clock para controlar a taxa de atualização
clock = pygame.time.Clock()

# Configura o jogador
player = pygame.Rect(100, 100, tile_width, tile_height)
player_color = (0, 128, 255)
player_velocity_x = 0
player_velocity_y = 0
player_speed = 5
gravity = 0.5
jump_strength = -10
is_jumping = False

# Variável para controlar a visibilidade do jogador
player_visible = False

# Lista de músicas
music_files = [
    'resources/music/Horizonte Digital01.mp3',
    'resources/music/Horizonte Digital02.mp3',
    'resources/music/Sentido de Viver01.mp3'
]

# Função para tocar uma música aleatória
def play_random_music():
    pygame.mixer.music.stop()  # Para qualquer música que esteja tocando
    music_file = random.choice(music_files)  # Escolhe uma música aleatoriamente
    pygame.mixer.music.load(music_file)  # Carrega a música
    pygame.mixer.music.play()  # Começa a tocar a música

# Função para desenhar o fundo com a imagem
def draw_background():
    screen.blit(background_image, (0, 0))

# Função para desenhar os blocos
def draw_blocks():
    for block in blocks:
        block_surface = palette[block['tile_index']]
        screen.blit(block_surface, block['pos'])

# Função para desenhar a paleta de cores com rolagem vertical
def draw_color_palette():
    x_offset = width - (tile_width + palette_margin)
    y_offset = palette_margin - scroll_offset
    for i, tile_surface in enumerate(palette):
        rect = pygame.Rect(x_offset, y_offset + (i * (tile_height + palette_margin)), tile_width, tile_height)
        palette_rects.append(rect)
        screen.blit(tile_surface, rect.topleft)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Borda preta
    
    # Desenha o contorno da paleta
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x_offset - 5, palette_margin - 5 - scroll_offset, tile_width + 10, len(palette) * (tile_height + palette_margin) + 10), 2)

# Função para detectar a cor selecionada
def get_selected_color(pos):
    for i, rect in enumerate(palette_rects):
        if rect.collidepoint(pos):
            return i
    return None

# Limpa a lista de retângulos da paleta
def clear_palette_rects():
    global palette_rects
    palette_rects = []

# Função para verificar colisão entre dois retângulos
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Função para aplicar a gravidade
def apply_gravity():
    global player
    global player_velocity_y
    player.y += player_velocity_y
    player_velocity_y += gravity

    # Verifica a colisão com blocos
    block_collision = check_block_collision()
    if block_collision:
        if player_velocity_y > 0:  # Caindo
            player.bottom = block_collision.top
            player_velocity_y = 0
            global is_jumping
            is_jumping = False
        elif player_velocity_y < 0:  # Subindo
            player.top = block_collision.bottom
            player_velocity_y = 0

def check_block_collision():
    for block in blocks:
        block_rect = pygame.Rect(block['pos'][0], block['pos'][1], tile_width, tile_height)
        if check_collision(player, block_rect):
            return block_rect
    return None

# Função para aplicar gravidade a blocos específicos
def apply_block_gravity():
    global blocks
    for block in blocks:
        if block['tile_index'] == 3:  # Índice do bloco de areia
            x, y = block['pos']
            block_rect = pygame.Rect(x, y, tile_width, tile_height)
            if not any(check_collision(block_rect, pygame.Rect(b['pos'][0], b['pos'][1], tile_width, tile_height)) for b in blocks if b['pos'] != block['pos']):
                block['pos'] = (x, y + 1)  # Move o bloco de areia para baixo
        if block['tile_index'] == 4:  # Índice do bloco de agua
            x, y = block['pos']
            block_rect = pygame.Rect(x, y, tile_width, tile_height)
            if not any(check_collision(block_rect, pygame.Rect(b['pos'][0], b['pos'][1], tile_width, tile_height)) for b in blocks if b['pos'] != block['pos']):
                block['pos'] = (x, y + 1)  # Move o bloco de agua para baixo
# Flag para mostrar a paleta de cores
show_palette = False

# Função para desenhar o contador de blocos
def draw_block_counter():
    font = pygame.font.Font('resources/fonts/ComicSansMS.ttf', 30)  # Usando Comic Sans MS
    text = font.render(f'Blocos: {len(blocks)}', True, (0, 0, 0))
    screen.blit(text, (10, height - 40))

# Função para desenhar um botão estilizado
def draw_button(text, x, y, width, height, font_size=30):
    font = pygame.font.Font('resources/fonts/ComicSansMS.ttf', font_size)  # Usando Comic Sans MS
    button_color = (100, 150, 255)
    border_color = (0, 0, 0)
    
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_color, button_rect)
    pygame.draw.rect(screen, border_color, button_rect, 2)
    
    text_surface = font.render(text, True, border_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return button_rect

# Função para desenhar o menu inicial
def draw_start_menu():
    draw_background()
    
    # Nome do jogo
    font = pygame.font.Font('resources/fonts/ComicSansMS.ttf', 65)  # Usando Comic Sans MS
    text_surface = font.render('Stikman World', True, (0, 0, 0))
    screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, 50))
    
    # Botão para começar o jogo
    button_rect = draw_button('Começar', width // 2 - 75, height // 2 - 25, 150, 50)
    
    # Botão de ajuda
    help_button_rect = draw_button('Ajuda', width // 2 - 75, height // 2 + 40, 150, 50)
    
    pygame.display.flip()
    return button_rect, help_button_rect

# Função para desenhar a tela de ajuda
def draw_help_screen():
    draw_background()
    
    # Nome da tela de ajuda
    font = pygame.font.Font('resources/fonts/ComicSansMS.ttf', 40)  # Usando Comic Sans MS
    text_surface = font.render('Ajuda', True, (0, 0, 0))
    screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, 50))
    
    # Texto de ajuda
    font = pygame.font.Font('resources/fonts/ComicSansMS.ttf', 24)  # Usando Comic Sans MS
    help_text = [
        'Controles:',
        'W - Pular',
        'A - Mover para a Esquerda',
        'D - Mover para a Direita',
        'B - Adicionar Bloco',
        'R - Remover Bloco',
        'P - Mostrar/Ocultar Paleta',
        'V - Mostrar o Jogador',
        'SETAS up, down - Rolagem da Paleta'
    ]
    
    y_offset = 100
    for line in help_text:
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, y_offset))
        y_offset += 40
    
    # Botão para voltar ao menu inicial
    back_button_rect = draw_button('Voltar', width // 2 - 75, height - 100, 150, 50, font_size=24)
    
    pygame.display.flip()
    return back_button_rect

# Flag para mostrar o menu inicial
show_start_menu = True
show_help_screen = False

# Toca a primeira música
play_random_music()

# Loop principal do jogo
running = True
while running:
    if show_help_screen:
        # Processa os eventos na tela de ajuda
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    show_help_screen = False
                    show_start_menu = True  # Volta ao menu inicial
    
        # Desenha a tela de ajuda
        back_button_rect = draw_help_screen()
    
    elif not show_start_menu:
        # Processa os eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    x, y = pygame.mouse.get_pos()
                    block_x = (x // tile_width) * tile_width
                    block_y = (y // tile_height) * tile_height
                    if not any(block['pos'] == (block_x, block_y) for block in blocks):
                        blocks.append({'pos': (block_x, block_y), 'tile_index': current_tile})
                elif event.key == pygame.K_r:
                    x, y = pygame.mouse.get_pos()
                    block_x = (x // tile_width) * tile_width
                    block_y = (y // tile_height) * tile_height
                    blocks = [block for block in blocks if block['pos'] != (block_x, block_y)]
                elif event.key == pygame.K_p:
                    show_palette = not show_palette
                    if not show_palette:
                        clear_palette_rects()
                elif event.key == pygame.K_v:
                    x, y = pygame.mouse.get_pos()
                    player.x = (x // tile_width) * tile_width
                    player.y = (y // tile_height) * tile_height
                    player_visible = True  # Torna o jogador visível
                elif event.key == pygame.K_w:
                    if not is_jumping:
                        player_velocity_y = jump_strength
                        is_jumping = True
                elif event.key == pygame.K_a:
                    player_velocity_x = -player_speed
                elif event.key == pygame.K_d:
                    player_velocity_x = player_speed
                elif event.key == pygame.K_DOWN:
                    scroll_offset += 10
                elif event.key == pygame.K_UP:
                    scroll_offset -= 10
                elif event.key == pygame.K_h:
                    show_help_screen = True
                    show_start_menu = False  # Fecha o menu inicial

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player_velocity_x = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_palette:
                    selected_color = get_selected_color(event.pos)
                    if selected_color is not None:
                        current_tile = selected_color
                        show_palette = False
                        clear_palette_rects()
                elif button_rect.collidepoint(event.pos) and show_start_menu:
                    show_start_menu = False
                elif help_button_rect.collidepoint(event.pos) and show_start_menu:
                    show_help_screen = True
                    show_start_menu = False

        if player_visible:
            # Atualiza a posição do jogador
            player.x += player_velocity_x

            # Aplica a gravidade
            apply_gravity()

            # Verifica colisões com blocos
            block_collision = check_block_collision()
            if block_collision:
                if player_velocity_x > 0:  # Movendo para a direita
                    player.right = block_collision.left
                elif player_velocity_x < 0:  # Movendo para a esquerda
                    player.left = block_collision.right

        # Aplica gravidade aos blocos de areia
        apply_block_gravity()

        # Limpa a tela
        screen.fill((255, 255, 255))  # Branco

        # Desenha o fundo com a imagem
        draw_background()

        # Desenha todos os blocos
        draw_blocks()

        # Se a paleta de cores deve ser exibida
        if show_palette:
            draw_color_palette()

        # Desenha o jogador se visível
        if player_visible:
            pygame.draw.rect(screen, player_color, player)

        # Desenha o contador de blocos
        draw_block_counter()

        # Atualiza o conteúdo da tela
        pygame.display.flip()

        # Verifica se a música terminou e toca uma nova
        if not pygame.mixer.music.get_busy():
            play_random_music(
)
        # Define a taxa de atualização (fps)
        clock.tick(60)  # 60 fps
    else:
        # Desenha o menu inicial
        button_rect, help_button_rect = draw_start_menu()

        # Aguardar o clique do usuário para começar o jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    show_start_menu = False
                elif help_button_rect.collidepoint(event.pos):
                    show_help_screen = True
                    show_start_menu = False