import pygame
import random
import os
import json
import math

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana del juego
ANCHO = 800
ALTO = 600 #640 para cuadrar tamaño sprites tiles mapa
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Journey of the Prairie King")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Reloj para controlar los FPS
reloj = pygame.time.Clock()
FPS = 60

# Fuente para la puntuación
fuente = pygame.font.SysFont('Arial', 25)

# Cargar música de fondo
#pygame.mixer.music.load('background_music.mp3')
#pygame.mixer.music.play(-1)

# Cargar efectos de sonido
sonido_disparo = pygame.mixer.Sound('audio/shoot.wav')
sonido_golpe = pygame.mixer.Sound('audio/hit.wav')
sonido_potenciador = pygame.mixer.Sound('audio/powerup.wav')
sonido_game_over = pygame.mixer.Sound('audio/game_over.wav')

# Función para cargar la spritesheet
def cargar_spritesheet(archivo):
    hoja = pygame.image.load(archivo).convert_alpha()
    return hoja

# Función para recortar sprites individuales de la spritesheet
def obtener_sprite(hoja, x, y, ancho, alto):
    sprite = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    sprite.blit(hoja, (0, 0), (x, y, ancho, alto))
    return sprite

# Cargar spritesheet
spritesheet = cargar_spritesheet('sprites/spritesheet.png')

# Definir sprites individuales basados en las posiciones de la hoja de sprites original
sprites = {
    'player': [obtener_sprite(spritesheet, 367, 112, 16, 16)],#, obtener_sprite(spritesheet, 16, 0, 16, 16)
    'enemy_basic': [obtener_sprite(spritesheet, 224, 64, 16, 16), obtener_sprite(spritesheet, 240, 64, 16, 16)],
    'enemy_fast': [obtener_sprite(spritesheet, 255, 64, 16, 16), obtener_sprite(spritesheet, 272, 64, 16, 16)],
    'enemy_strong': [obtener_sprite(spritesheet, 287, 64, 16, 16), obtener_sprite(spritesheet, 303, 64, 16, 16)],
    'boss': [obtener_sprite(spritesheet, 191, 144, 16, 16),obtener_sprite(spritesheet, 208, 144, 16, 16),obtener_sprite(spritesheet, 223, 144, 16, 16),obtener_sprite(spritesheet, 241, 144, 16, 16)],  # Suponiendo que el boss es un sprite más grande
    'bullet': obtener_sprite(spritesheet, 394, 112, 5, 5),
    'powerup_speed': obtener_sprite(spritesheet, 241, 162, 12, 12),
    'powerup_live': obtener_sprite(spritesheet, 272, 163, 14, 11),
    'powerup_live': obtener_sprite(spritesheet, 272, 163, 14, 11),
    'powerup_multishot': obtener_sprite(spritesheet, 191, 160, 16, 16),
    'powerup_explosive': obtener_sprite(spritesheet, 208, 160, 15, 16),
    'tile_grass': obtener_sprite(spritesheet, 383, 0, 16, 16),
    'tile_dirt': obtener_sprite(spritesheet, 399, 0, 16, 16),
    'tile_water': obtener_sprite(spritesheet, 463, 0, 16, 16),
    'tile_sand': obtener_sprite(spritesheet, 399, 32, 16, 16),
    'tile_sandstone1': obtener_sprite(spritesheet, 335, 32, 16, 16),
    'tile_sandstone2': obtener_sprite(spritesheet, 351, 32, 16, 16),
    'tile_waterD1': obtener_sprite(spritesheet, 463, 32, 16, 16),
    'tile_waterD2': obtener_sprite(spritesheet, 479, 32, 16, 16),
    'obstacle_log': obtener_sprite(spritesheet, 447, 0, 16, 16),
    'obstacle_bush': obtener_sprite(spritesheet, 431, 0, 16, 16)
}

# Función para guardar altas puntuaciones
def guardar_alta_puntuacion(puntuacion):
    archivo_puntuaciones = 'altas_puntuaciones.json'
    if os.path.exists(archivo_puntuaciones):
        with open(archivo_puntuaciones, 'r') as archivo:
            puntuaciones = json.load(archivo)
    else:
        puntuaciones = []

    puntuaciones.append(puntuacion)
    puntuaciones = sorted(puntuaciones, reverse=True)[:5]  # Guardar solo las 5 más altas

    with open(archivo_puntuaciones, 'w') as archivo:
        json.dump(puntuaciones, archivo)

# Función para mostrar altas puntuaciones
def mostrar_altas_puntuaciones():
    archivo_puntuaciones = 'altas_puntuaciones.json'
    if os.path.exists(archivo_puntuaciones):
        with open(archivo_puntuaciones, 'r') as archivo:
            puntuaciones = json.load(archivo)
    else:
        puntuaciones = []

    VENTANA.fill(BLANCO)
    titulo = fuente.render("Registro Puntuaciones", True, NEGRO)
    VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))
    for i, puntuacion in enumerate(puntuaciones):
        texto = fuente.render(f"{i + 1}. {puntuacion}", True, NEGRO)
        VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 100 + i * 30))
    pygame.display.update()
    pygame.time.wait(3000)

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = sprites['player']
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.velocidad = 3
        self.puntuacion = 0
        self.vidas = 3
        self.animacion = 0
        self.contador_animacion = 0
        self.speed_potenciador_activo = False
        self.speed_potenciador_tiempo = 0
        self.multishot_activo = False
        self.multishot_potenciador_tiempo = 0
        self.tiempo_disparo = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_d]:
            self.rect.x += self.velocidad
        if keys[pygame.K_w]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_s]:
            self.rect.y += self.velocidad

        if pygame.sprite.spritecollide(self, mapa.obstaculos, False):
            self.rect.x -= self.velocidad

        if pygame.sprite.spritecollide(self, mapa.obstaculos, False):
            self.rect.y -= self.velocidad
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

        self.contador_animacion += 1
        if self.contador_animacion >= 10:
            self.contador_animacion = 0
            self.animacion = (self.animacion + 1) % len(self.sprites)
            self.image = self.sprites[self.animacion]

        # Verificar tiempo del potenciador de velocidad
        if self.speed_potenciador_activo and pygame.time.get_ticks() - self.speed_potenciador_tiempo > 5000:  # 5 segundos de duración
            self.velocidad //= 2
            self.speed_potenciador_activo = False
        
        # Verificar tiempo del potenciador de multishot
        if self.multishot_activo and pygame.time.get_ticks() - self.multishot_potenciador_tiempo > 5000:  # 5 segundos de duración
            self.multishot_activo = False
            
            
        if self.multishot_activo:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_disparo > 150:  # Controlar la cadencia de disparo
                self.tiempo_disparo = tiempo_actual
                self.disparar_multiple()

    def disparar(self):
        if not self.multishot_activo:
            bala = Bala(self.rect.centerx, self.rect.top)
            todos_los_sprites.add(bala)
            balas.add(bala)
            sonido_disparo.play()
        else:
            self.disparar_multiple()

    def disparar_multiple(self):
        for direccion in ['up', 'left', 'right', 'down']:
            bala = Bala(self.rect.centerx, self.rect.top, direccion)
            todos_los_sprites.add(bala)
            balas.add(bala)
        sonido_disparo.play()
    """def disparar_multiple(self):
        for angulo in [-15, 0, 15]:
            rad = math.radians(angulo)
            bala = Bala(self.rect.centerx + int(10 * math.cos(rad)), self.rect.top + int(10 * math.sin(rad)))
            todos_los_sprites.add(bala)
            balas.add(bala)
            sonido_disparo.play()"""

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        self.sprites = sprites[f'enemy_{tipo}']
        self.image = self.sprites[0]
        if tipo == 'basic':
            self.velocidad = 2
        elif tipo == 'fast':
            self.velocidad = 4
        elif tipo == 'strong':
            self.velocidad = 1
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        #self.velocidad_y = random.randrange(1, 4) if tipo != 'fast' else random.randrange(4, 7)
        #self.velocidad_x = random.choice([-2, 2]) if tipo == 'strong' else 0
        self.animacion = 0
        self.contador_animacion = 0
            
    def update(self):
        # Calcular la dirección hacia el jugador
        dx = jugador.rect.x - self.rect.x
        dy = jugador.rect.y - self.rect.y
        dist = math.hypot(dx, dy)

        # Normalizar el vector de dirección
        if dist != 0:
            dx /= dist
            dy /= dist

        # Mover el enemigo hacia el jugador
        self.rect.x += dx * self.velocidad
        self.rect.y += dy * self.velocidad

        # Verificar colisiones con obstáculos y ajustar la dirección si es necesario
        if pygame.sprite.spritecollide(self, mapa.obstaculos, False):
            self.rect.x -= dx * self.velocidad
            self.rect.y -= dy * self.velocidad
            # Ajuste de dirección para evitar el obstáculo
            self.rect.x += dy * self.velocidad
            self.rect.y -= dx * self.velocidad

        # Verificar si el enemigo salió de la pantalla y reubicarlo
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(-100, -40)

        # Animación
        self.contador_animacion += 1
        if self.contador_animacion >= 10:
            self.contador_animacion = 0
            self.animacion = (self.animacion + 1) % len(self.sprites)
            self.image = self.sprites[self.animacion]

class Jefe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = sprites['boss']
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        #self.rect.center = (ANCHO // 2, -self.rect.height)
        #self.rect.center = (ANCHO // 2, 0)
        self.rect.x = random.randrange(0, ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad = 2
        self.vida = 10
        self.animacion = 0
        self.contador_animacion = 0

    def update(self):
        # Calcular la dirección hacia el jugador
        dx = jugador.rect.x - self.rect.x
        dy = jugador.rect.y - self.rect.y
        dist = math.hypot(dx, dy)

        # Normalizar el vector de dirección
        if dist != 0:
            dx /= dist
            dy /= dist

        # Mover el jefe hacia el jugador
        self.rect.x += dx * self.velocidad
        self.rect.y += dy * self.velocidad

        # Verificar colisiones con obstáculos y ajustar la dirección si es necesario
        if pygame.sprite.spritecollide(self, mapa.obstaculos, False):
            self.rect.x -= dx * self.velocidad
            self.rect.y -= dy * self.velocidad
            # Ajuste de dirección para evitar el obstáculo
            self.rect.x += dy * self.velocidad
            self.rect.y -= dx * self.velocidad
        
        if pygame.sprite.spritecollide(self, mapa.obstaculos, False):
            self.rect.y -= self.velocidad
        
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(-100, -40)

        # Animación si hay más de un sprite
        if len(self.sprites) > 1:
            self.contador_animacion += 1
            if self.contador_animacion >= 10:
                self.contador_animacion = 0
                self.animacion = (self.animacion + 1) % len(self.sprites)
                self.image = self.sprites[self.animacion]

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        super().__init__()
        self.image = sprites['bullet']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direccion = direccion
        self.velocidad = 5

    def update(self):
        if self.direccion == 'up':
            self.rect.y -= self.velocidad
        elif self.direccion == 'down':
            self.rect.y += self.velocidad
        elif self.direccion == 'left':
            self.rect.x -= self.velocidad
        elif self.direccion == 'right':
            self.rect.x += self.velocidad

        if pygame.sprite.spritecollide(self, mapa.obstaculos, False):
            self.kill()

        if self.rect.bottom < 0 or self.rect.top > ALTO or self.rect.right < 0 or self.rect.left > ANCHO:
            self.kill()

class Potenciador(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo
        self.image = sprites[f'powerup_{tipo}']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if pygame.sprite.collide_rect(self, jugador):
            if self.tipo == 'speed':
                if jugador.speed_potenciador_activo == False:
                    jugador.velocidad *= 2
                    jugador.speed_potenciador_activo = True
                jugador.speed_potenciador_tiempo = pygame.time.get_ticks()
                sonido_potenciador.play()
            elif self.tipo == 'live':
                jugador.vidas += 1
                sonido_potenciador.play()
            elif self.tipo == 'multishot':
                jugador.multishot_activo = True
                jugador.multishot_potenciador_tiempo = pygame.time.get_ticks()
                sonido_potenciador.play()
            elif self.tipo == 'explosive':
                jugador.puntuacion += len(enemigos) * 10
                for enemigo in enemigos:
                    enemigo.kill()
                pygame.time.wait(2000)
                crear_enemigos(enemigos_por_oleada)
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.image = sprites[f'obstacle_{tipo}']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Mapa:
    def __init__(self, nivel):
        self.tiles = []
        self.obstaculos = pygame.sprite.Group()
        self.cargar_mapa(nivel)

    def cargar_mapa(self, nivel):
        niveles = {
            1: [
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGDGGGDGGGGGGGGGGGGG",
                "GGGGGGGGOGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDGGDGGGGGGDGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDGGGGGGG",
                "GGGGGGGOGGGGGGGGGGGGGGGGGGGGGGGGGGGGGBGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGDGGGDGGGGGGGGGGGGG",
                "GGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDGGDGGGGGGDGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGOGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGBGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGOGGGDGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGDGGGGGGGGGDGGGGGGGGGGGGGGDGGGGGGGGGG",
                "GGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGDGGGDGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDGGDGGGGGGGDGGGGGGGG",
                "GGGGGGGGGGGGGGBGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGDGGGDGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGOGGGGDGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDGGDGGGGGGDGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGOGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGDGGGGGGGGGDGGGGGGGGDGGGGGGGGGGGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGDGGGGGGGGGGGGGGGGGGDGGGGGG",
                "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
            ],
            2: [
                "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
                "SSSSSSSSSSSSSSTSSSSSSSSSStSSSSSSSSSSSSSSSSSSSSSSSS",
                "SSSSSSSStSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSStSSSSSSSSS",
                "S...........WWW..........................T.......S",
                "S.............W..................................S",
                "S.....O.....................tT...................S",
                "S................................................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S.................................t......S",
                "S..T....S........................................S",
                "S.......S..........T.............................S",
                "S.......S...........t.......................t....S",
                "S.......S....................................t...S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S................T.......................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S.T......................................S",
                "S.......S................................t.......S",
                "S.......S...............................tSt......S",
                "S.......S........................................S",
                "S.......S................tTt.....................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S........................................S",
                "S.......S........TT..............................S",
                "S.......S........tt..............................S",
                "S.......S..................................T.....S",
                "S.......S........................................S",
                "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
            ]
        }
        mapa = niveles[nivel]
        self.tiles = []
        self.obstaculos.empty()
        for y, fila in enumerate(mapa):
            for x, tile in enumerate(fila):
                if tile == "G":
                    self.tiles.append((sprites['tile_grass'], x * 16, y * 16))
                elif tile == "D":
                    self.tiles.append((sprites['tile_dirt'], x * 16, y * 16))
                elif tile == "W":
                    self.tiles.append((sprites['tile_water'], x * 16, y * 16))
                elif tile == "S":
                    self.tiles.append((sprites['tile_sand'], x * 16, y * 16))
                elif tile == "T":
                    self.tiles.append((sprites['tile_sandstone1'], x * 16, y * 16))
                elif tile == "t":
                    self.tiles.append((sprites['tile_sandstone2'], x * 16, y * 16))
                elif tile == "O":
                    obstaculoL = Obstacle(x*16, y*16, 'log')
                    self.obstaculos.add(obstaculoL)
                    self.tiles.append((sprites['obstacle_log'], x * 16, y * 16))
                elif tile == "B":
                    obstaculoB = Obstacle(x*16, y*16, 'bush')
                    self.obstaculos.add(obstaculoB)
                    self.tiles.append((sprites['obstacle_bush'], x * 16, y * 16))
                    
    def dibujar(self):
        for tile, x, y in self.tiles:
            VENTANA.blit(tile, (x, y))
        self.obstaculos.draw(VENTANA)

        
        
# Crear mapas de niveles
nivel_actual = 1
mapa = Mapa(nivel_actual)

# Crear grupos de sprites
todos_los_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()
potenciadores = pygame.sprite.Group()
#obstaculos = pygame.sprite.Group()

# Crear instancia del jugador
jugador = Jugador()
todos_los_sprites.add(jugador)

# Función para crear enemigos
def crear_enemigos(n):
    for _ in range(n):
        tipo = random.choice(['basic', 'fast', 'strong'])
        enemigo = Enemigo(tipo)
        todos_los_sprites.add(enemigo)
        enemigos.add(enemigo)

# Crear los primeros enemigos
crear_enemigos(10)


# Función para mostrar la pantalla de inicio
def pantalla_inicio():
    inicio = True
    while inicio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    inicio = False

        VENTANA.fill(BLANCO)
        mensaje_inicio = fuente.render("Pulsa ENTER para empezar", True, NEGRO)
        VENTANA.blit(mensaje_inicio, (ANCHO // 2 - mensaje_inicio.get_width() // 2, ALTO // 2 - mensaje_inicio.get_height() // 2))
        pygame.display.flip()
        reloj.tick(FPS)

# Función para mostrar la pantalla de fin
def pantalla_fin():
    fin = True
    guardar_alta_puntuacion(jugador.puntuacion)
    while fin:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    fin = False

        VENTANA.fill(BLANCO)
        mensaje_fin = fuente.render("Game Over - Pulsa ENTER para reiniciar", True, NEGRO)
        VENTANA.blit(mensaje_fin, (ANCHO // 2 - mensaje_fin.get_width() // 2, ALTO // 2 - mensaje_fin.get_height() // 2))
        mostrar_altas_puntuaciones()
        #pygame.display.flip()
        pygame.display.update()
        reloj.tick(FPS)

# Mostrar la pantalla de inicio
pantalla_inicio()

# Variables del juego
oleada = 1
enemigos_por_oleada = 10
jefe_activo = False

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                bala = Bala(jugador.rect.centerx, jugador.rect.centery, 'up')
                todos_los_sprites.add(bala)
                balas.add(bala)
                sonido_disparo.play()
            if evento.key == pygame.K_DOWN:
                bala = Bala(jugador.rect.centerx, jugador.rect.centery, 'down')
                todos_los_sprites.add(bala)
                balas.add(bala)
                sonido_disparo.play()
            if evento.key == pygame.K_RIGHT:
                bala = Bala(jugador.rect.centerx, jugador.rect.centery, 'right')
                todos_los_sprites.add(bala)
                balas.add(bala)
                sonido_disparo.play()
            if evento.key == pygame.K_LEFT:
                bala = Bala(jugador.rect.centerx, jugador.rect.centery, 'left')
                todos_los_sprites.add(bala)
                balas.add(bala)
                sonido_disparo.play()
                       
    
    # Actualizar
    todos_los_sprites.update()

    # Colisiones entre balas y enemigos
    colisiones_enemigos = pygame.sprite.groupcollide(enemigos, balas, True, True)
    for colision in colisiones_enemigos:
        jugador.puntuacion += 10
        if random.random() < 0.1:  # 10% de probabilidad de que aparezca un potenciador
            tipo_potenciador = random.choice(['speed', 'live', 'multishot', 'explosive'])
            potenciador = Potenciador(colision.rect.centerx, colision.rect.centery, tipo_potenciador)
            todos_los_sprites.add(potenciador)
            potenciadores.add(potenciador)
        sonido_golpe.play()

    # Colisiones entre balas y jefe
    if jefe_activo:
        colisiones_boss = pygame.sprite.spritecollide(jefe, balas, True, pygame.sprite.collide_mask)
        for colision in colisiones_boss:
            jefe.vida -= 1
            if jefe.vida == 0:
                jefe.kill()
                jefe_activo = False
                nivel_actual += 1
                oleada = 1
                break

    #COLISIÓN DEL JUGADOR CON LOS ENEMIGOS            
    if pygame.sprite.spritecollide(jugador, enemigos, True):
        jugador.vidas -= 1
        if jugador.vidas == 0:
            sonido_game_over.play()
            pantalla_fin()
            jugador.vidas = 3
            jugador.puntuacion = 0
            todos_los_sprites.empty()
            enemigos.empty()
            balas.empty()
            potenciadores.empty()
            #obstaculos.empty()
            jugador = Jugador()
            todos_los_sprites.add(jugador)
            mapa = Mapa(1)
            crear_enemigos(enemigos_por_oleada)
            jefe_activos = False

    # Subir de nivel cada 3 oleadas
    if not enemigos and not jefe_activo:
        if oleada % 3 == 0:
            jefe = Jefe()
            todos_los_sprites.add(jefe)
            jefe_activo = True
        else:
            oleada += 1
            pygame.time.wait(2000)
            crear_enemigos(enemigos_por_oleada)
            enemigos_por_oleada += 2

    # Dibujar / renderizar
    VENTANA.fill(BLANCO)
    mapa.dibujar()
    todos_los_sprites.draw(VENTANA)

    # Dibujar la puntuación, nivel y vidas
    texto_puntuacion = fuente.render(f'Puntuación: {jugador.puntuacion}', True, NEGRO)
    VENTANA.blit(texto_puntuacion, (10, 10))
    texto_nivel = fuente.render(f'Nivel: {nivel_actual}', True, NEGRO)
    VENTANA.blit(texto_nivel, (10, 40))
    texto_vidas = fuente.render(f'Vidas: {jugador.vidas}', True, NEGRO)
    VENTANA.blit(texto_vidas, (10, 70))

    # Después de dibujar todo, actualizar la pantalla
    #pygame.display.flip()
    pygame.display.update()

    # Controlar los FPS
    reloj.tick(FPS)

# Mostrar la pantalla de fin
pantalla_fin()

pygame.quit()

