"""import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana del juego
ANCHO = 800
ALTO = 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Journey of the Prairie King")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Reloj para controlar los FPS
reloj = pygame.time.Clock()
FPS = 60

# Fuente para la puntuación
fuente = pygame.font.SysFont('Arial', 25)

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

# Definir sprites individuales
sprites = {
    'player': obtener_sprite(spritesheet, 0, 0, 32, 32),
    'enemy_basic': obtener_sprite(spritesheet, 32, 0, 32, 32),
    'enemy_fast': obtener_sprite(spritesheet, 64, 0, 32, 32),
    'enemy_strong': obtener_sprite(spritesheet, 96, 0, 32, 32),
    'bullet': obtener_sprite(spritesheet, 128, 0, 16, 16),
    'powerup': obtener_sprite(spritesheet, 144, 0, 32, 32)
}

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = sprites['player']
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.velocidad = 5
        self.puntuacion = 0
        self.vidas = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        if tipo == 'basic':
            self.image = sprites['enemy_basic']
            self.velocidad_y = random.randrange(1, 4)
        elif tipo == 'fast':
            self.image = sprites['enemy_fast']
            self.velocidad_y = random.randrange(4, 7)
        elif tipo == 'strong':
            self.image = sprites['enemy_strong']
            self.velocidad_y = random.randrange(1, 3)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        super().__init__()
        self.image = sprites['bullet']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direccion = direccion
        self.velocidad = 10

    def update(self):
        if self.direccion == 'up':
            self.rect.y -= self.velocidad
        elif self.direccion == 'down':
            self.rect.y += self.velocidad
        elif self.direccion == 'left':
            self.rect.x -= self.velocidad
        elif self.direccion == 'right':
            self.rect.x += self.velocidad

        if self.rect.bottom < 0 or self.rect.top > ALTO or self.rect.right < 0 or self.rect.left > ANCHO:
            self.kill()

class Potenciador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = sprites['powerup']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        pass

# Crear grupos de sprites
todos_los_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()
potenciadores = pygame.sprite.Group()

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

        VENTANA.fill(NEGRO)
        mensaje_inicio = fuente.render("Pulsa ENTER para empezar", True, BLANCO)
        VENTANA.blit(mensaje_inicio, (ANCHO // 2 - mensaje_inicio.get_width() // 2, ALTO // 2 - mensaje_inicio.get_height() // 2))
        pygame.display.flip()
        reloj.tick(FPS)

# Función para mostrar la pantalla de fin
def pantalla_fin():
    fin = True
    while fin:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    fin = False

        VENTANA.fill(NEGRO)
        mensaje_fin = fuente.render("Game Over - Pulsa ENTER para reiniciar", True, BLANCO)
        VENTANA.blit(mensaje_fin, (ANCHO // 2 - mensaje_fin.get_width() // 2, ALTO // 2 - mensaje_fin.get_height() // 2))
        pygame.display.flip()
        reloj.tick(FPS)

# Mostrar la pantalla de inicio
pantalla_inicio()

# Variables del juego
nivel = 1
potenciador_activo = False

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                direcciones = ['up', 'down', 'left', 'right']
                for direccion in direcciones:
                    bala = Bala(jugador.rect.centerx, jugador.rect.centery, direccion)
                    todos_los_sprites.add(bala)
                    balas.add(bala)

    # Actualizar
    todos_los_sprites.update()

    # Comprobar colisiones
    colisiones_enemigos = pygame.sprite.groupcollide(enemigos, balas, True, True)
    for colision in colisiones_enemigos:
        jugador.puntuacion += 10
        if random.random() < 0.1:  # 10% de probabilidad de que aparezca un potenciador
            potenciador = Potenciador(colision.rect.x, colision.rect.y)
            todos_los_sprites.add(potenciador)
            potenciadores.add(potenciador)
        enemigo = Enemigo('basic')
        todos_los_sprites.add(enemigo)
        enemigos.add(enemigo)

    if pygame.sprite.spritecollideany(jugador, enemigos):
        jugador.vidas -= 1
        if jugador.vidas <= 0:
            ejecutando = False
        else:
            for enemigo in enemigos:
                enemigo.kill()
            crear_enemigos(10)

    colisiones_potenciadores = pygame.sprite.spritecollide(jugador, potenciadores, True)
    for colision in colisiones_potenciadores:
        potenciador_activo = True

    # Subir de nivel cada 1000 puntos
    if jugador.puntuacion >= nivel * 1000:
        nivel += 1
        crear_enemigos(5)

    # Dibujar / renderizar
    VENTANA.fill(NEGRO)
    todos_los_sprites.draw(VENTANA)

    # Dibujar la puntuación, nivel y vidas
    texto_puntuacion = fuente.render(f'Puntuación: {jugador.puntuacion}', True, BLANCO)
    VENTANA.blit(texto_puntuacion, (10, 10))
    texto_nivel = fuente.render(f'Nivel: {nivel}', True, BLANCO)
    VENTANA.blit(texto_nivel, (10, 40))
    texto_vidas = fuente.render(f'Vidas: {jugador.vidas}', True, BLANCO)
    VENTANA.blit(texto_vidas, (10, 70))

    # Después de dibujar todo, actualizar la pantalla
    pygame.display.flip()

    # Controlar los FPS
    reloj.tick(FPS)

# Mostrar la pantalla de fin
pantalla_fin()

pygame.quit()
/////////////////////
import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana del juego
ANCHO = 800
ALTO = 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Journey of the Prairie King")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Reloj para controlar los FPS
reloj = pygame.time.Clock()
FPS = 60

# Fuente para la puntuación
fuente = pygame.font.SysFont('Arial', 25)

# Cargar música de fondo
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

# Cargar efectos de sonido
sonido_disparo = pygame.mixer.Sound('shoot.wav')
sonido_golpe = pygame.mixer.Sound('hit.wav')
sonido_potenciador = pygame.mixer.Sound('powerup.wav')
sonido_game_over = pygame.mixer.Sound('game_over.wav')

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

# Definir sprites individuales
sprites = {
    'player': [obtener_sprite(spritesheet, 0, 0, 32, 32), obtener_sprite(spritesheet, 32, 0, 32, 32)],
    'enemy_basic': [obtener_sprite(spritesheet, 0, 32, 32, 32), obtener_sprite(spritesheet, 32, 32, 32, 32)],
    'enemy_fast': [obtener_sprite(spritesheet, 64, 32, 32, 32), obtener_sprite(spritesheet, 96, 32, 32, 32)],
    'enemy_strong': [obtener_sprite(spritesheet, 128, 32, 32, 32), obtener_sprite(spritesheet, 160, 32, 32, 32)],
    'bullet': obtener_sprite(spritesheet, 192, 0, 16, 16),
    'powerup_speed': obtener_sprite(spritesheet, 0, 64, 32, 32),
    'powerup_shield': obtener_sprite(spritesheet, 32, 64, 32, 32),
}

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = sprites['player']
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.velocidad = 5
        self.puntuacion = 0
        self.vidas = 3
        self.animacion = 0
        self.contador_animacion = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

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

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        self.sprites = sprites[f'enemy_{tipo}']
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 4) if tipo != 'fast' else random.randrange(4, 7)
        self.animacion = 0
        self.contador_animacion = 0

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

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
        self.velocidad = 10

    def update(self):
        if self.direccion == 'up':
            self.rect.y -= self.velocidad
        elif self.direccion == 'down':
            self.rect.y += self.velocidad
        elif self.direccion == 'left':
            self.rect.x -= self.velocidad
        elif self.direccion == 'right':
            self.rect.x += self.velocidad

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
        pass

# Crear grupos de sprites
todos_los_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()
potenciadores = pygame.sprite.Group()

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

        VENTANA.fill(NEGRO)
        mensaje_inicio = fuente.render("Pulsa ENTER para empezar", True, BLANCO)
        VENTANA.blit(mensaje_inicio, (ANCHO // 2 - mensaje_inicio.get_width() // 2, ALTO // 2 - mensaje_inicio.get_height() // 2))
        pygame.display.flip()
        reloj.tick(FPS)

# Función para mostrar la pantalla de fin
def pantalla_fin():
    fin = True
    while fin:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    fin = False

        VENTANA.fill(NEGRO)
        mensaje_fin = fuente.render("Game Over - Pulsa ENTER para reiniciar", True, BLANCO)
        VENTANA.blit(mensaje_fin, (ANCHO // 2 - mensaje_fin.get_width() // 2, ALTO // 2 - mensaje_fin.get_height() // 2))
        pygame.display.flip()
        reloj.tick(FPS)

# Mostrar la pantalla de inicio
pantalla_inicio()

# Variables del juego
nivel = 1
potenciador_activo = False
potenciador_tiempo = 0

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                direcciones = ['up', 'down', 'left', 'right']
                for direccion in direcciones:
                    bala = Bala(jugador.rect.centerx, jugador.rect.centery, direccion)
                    todos_los_sprites.add(bala)
                    balas.add(bala)
                sonido_disparo.play()

    # Actualizar
    todos_los_sprites.update()

    # Comprobar colisiones
    colisiones_enemigos = pygame.sprite.groupcollide(enemigos, balas, True, True)
    for colision in colisiones_enemigos:
        jugador.puntuacion += 10
        if random.random() < 0.1:  # 10% de probabilidad de que aparezca un potenciador
            tipo_potenciador = random.choice(['speed', 'shield'])
            potenciador = Potenciador(colision.rect.x, colision.rect.y, tipo_potenciador)
            todos_los_sprites.add(potenciador)
            potenciadores.add(potenciador)
        enemigo = Enemigo('basic')
        todos_los_sprites.add(enemigo)
        enemigos.add(enemigo)
        sonido_golpe.play()

    if pygame.sprite.spritecollideany(jugador, enemigos):
        jugador.vidas -= 1
        if jugador.vidas <= 0:
            sonido_game_over.play()
            ejecutando = False
        else:
            for enemigo in enemigos:
                enemigo.kill()
            crear_enemigos(10)

    colisiones_potenciadores = pygame.sprite.spritecollide(jugador, potenciadores, True)
    for colision in colisiones_potenciadores:
        sonido_potenciador.play()
        if colision.tipo == 'speed':
            jugador.velocidad *= 2
            potenciador_tiempo = pygame.time.get_ticks()
        elif colision.tipo == 'shield':
            jugador.vidas += 1

    # Subir de nivel cada 1000 puntos
    if jugador.puntuacion >= nivel * 1000:
        nivel += 1
        crear_enemigos(5)

    # Verificar tiempo del potenciador
    if potenciador_activo and pygame.time.get_ticks() - potenciador_tiempo > 5000:  # 5 segundos de duración
        jugador.velocidad //= 2
        potenciador_activo = False

    # Dibujar / renderizar
    VENTANA.fill(NEGRO)
    todos_los_sprites.draw(VENTANA)

    # Dibujar la puntuación, nivel y vidas
    texto_puntuacion = fuente.render(f'Puntuación: {jugador.puntuacion}', True, BLANCO)
    VENTANA.blit(texto_puntuacion, (10, 10))
    texto_nivel = fuente.render(f'Nivel: {nivel}', True, BLANCO)
    VENTANA.blit(texto_nivel, (10, 40))
    texto_vidas = fuente.render(f'Vidas: {jugador.vidas}', True, BLANCO)
    VENTANA.blit(texto_vidas, (10, 70))

    # Después de dibujar todo, actualizar la pantalla
    pygame.display.flip()

    # Controlar los FPS
    reloj.tick(FPS)

# Mostrar la pantalla de fin
pantalla_fin()

pygame.quit()

import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana del juego
ANCHO = 800
ALTO = 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Journey of the Prairie King")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Reloj para controlar los FPS
reloj = pygame.time.Clock()
FPS = 60

# Fuente para la puntuación
fuente = pygame.font.SysFont('Arial', 25)

# Cargar música de fondo
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

# Cargar efectos de sonido
sonido_disparo = pygame.mixer.Sound('shoot.wav')
sonido_golpe = pygame.mixer.Sound('hit.wav')
sonido_potenciador = pygame.mixer.Sound('powerup.wav')
sonido_game_over = pygame.mixer.Sound('game_over.wav')

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
spritesheet = cargar_spritesheet('/mnt/data/spritesheet.png')

# Definir sprites individuales basados en las posiciones de la hoja de sprites original
sprites = {
    'player': [obtener_sprite(spritesheet, 0, 0, 16, 16), obtener_sprite(spritesheet, 16, 0, 16, 16)],
    'enemy_basic': [obtener_sprite(spritesheet, 32, 0, 16, 16), obtener_sprite(spritesheet, 48, 0, 16, 16)],
    'enemy_fast': [obtener_sprite(spritesheet, 64, 0, 16, 16), obtener_sprite(spritesheet, 80, 0, 16, 16)],
    'enemy_strong': [obtener_sprite(spritesheet, 96, 0, 16, 16), obtener_sprite(spritesheet, 112, 0, 16, 16)],
    'bullet': obtener_sprite(spritesheet, 128, 0, 8, 8),
    'powerup_speed': obtener_sprite(spritesheet, 144, 0, 16, 16),
    'powerup_shield': obtener_sprite(spritesheet, 160, 0, 16, 16),
}

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = sprites['player']
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.velocidad = 5
        self.puntuacion = 0
        self.vidas = 3
        self.animacion = 0
        self.contador_animacion = 0
        self.potenciador_activo = False
        self.potenciador_tiempo = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

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

        # Verificar tiempo del potenciador
        if self.potenciador_activo and pygame.time.get_ticks() - self.potenciador_tiempo > 5000:  # 5 segundos de duración
            self.velocidad //= 2
            self.potenciador_activo = False

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        self.sprites = sprites[f'enemy_{tipo}']
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 4) if tipo != 'fast' else random.randrange(4, 7)
        self.animacion = 0
        self.contador_animacion = 0

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

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
        self.velocidad = 10

    def update(self):
        if self.direccion == 'up':
            self.rect.y -= self.velocidad
        elif self.direccion == 'down':
            self.rect.y += self.velocidad
        elif self.direccion == 'left':
            self.rect.x -= self.velocidad
        elif self.direccion == 'right':
            self.rect.x += self.velocidad

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
        pass

# Crear grupos de sprites
todos_los_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()
potenciadores = pygame.sprite.Group()

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

        VENTANA.fill(NEGRO)
        mensaje_inicio = fuente.render("Pulsa ENTER para empezar", True, BLANCO)
        VENTANA.blit(mensaje_inicio, (ANCHO // 2 - mensaje_inicio.get_width() // 2, ALTO // 2 - mensaje_inicio.get_height() // 2))
        pygame.display.flip()
        reloj.tick(FPS)

# Función para mostrar la pantalla de fin
def pantalla_fin():
    fin = True
    while fin:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    fin = False

        VENTANA.fill(NEGRO)
        mensaje_fin = fuente.render("Game Over - Pulsa ENTER para reiniciar", True, BLANCO)
        VENTANA.blit(mensaje_fin, (ANCHO // 2 - mensaje_fin.get_width() // 2, ALTO // 2 - mensaje_fin.get_height() // 2))
        pygame.display.flip()
        reloj.tick(FPS)

# Mostrar la pantalla de inicio
pantalla_inicio()

# Variables del juego
nivel = 1

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                direcciones = ['up', 'down', 'left', 'right']
                for direccion in direcciones:
                    bala = Bala(jugador.rect.centerx, jugador.rect.centery, direccion)
                    todos_los_sprites.add(bala)
                    balas.add(bala)
                sonido_disparo.play()

    # Actualizar
    todos_los_sprites.update()

    # Comprobar colisiones
    colisiones_enemigos = pygame.sprite.groupcollide(enemigos, balas, True, True)
    for colision in colisiones_enemigos:
        jugador.puntuacion += 10
        if random.random() < 0.1:  # 10% de probabilidad de que aparezca un potenciador
            tipo_potenciador = random.choice(['speed', 'shield'])
            potenciador = Potenciador(colision.rect.x, colision.rect.y, tipo_potenciador)
            todos_los_sprites.add(potenciador)
            potenciadores.add(potenciador)
        enemigo = Enemigo('basic')
        todos_los_sprites.add(enemigo)
        enemigos.add(enemigo)
        sonido_golpe.play()

    if pygame.sprite.spritecollideany(jugador, enemigos):
        jugador.vidas -= 1
        if jugador.vidas <= 0:
            sonido_game_over.play()
            ejecutando = False
        else:
            for enemigo in enemigos:
                enemigo.kill()
            crear_enemigos(10)

    colisiones_potenciadores = pygame.sprite.spritecollide(jugador, potenciadores, True)
    for colision in colisiones_potenciadores:
        sonido_potenciador.play()
        if colision.tipo == 'speed':
            jugador.velocidad *= 2
            jugador.potenciador_activo = True
            jugador.potenciador_tiempo = pygame.time.get_ticks()
        elif colision.tipo == 'shield':
            jugador.vidas += 1

    # Subir de nivel cada 1000 puntos
    if jugador.puntuacion >= nivel * 1000:
        nivel += 1
        crear_enemigos(5)

    # Dibujar / renderizar
    VENTANA.fill(NEGRO)
    todos_los_sprites.draw(VENTANA)

    # Dibujar la puntuación, nivel y vidas
    texto_puntuacion = fuente.render(f'Puntuación: {jugador.puntuacion}', True, BLANCO)
    VENTANA.blit(texto_puntuacion, (10, 10))
    texto_nivel = fuente.render(f'Nivel: {nivel}', True, BLANCO)
    VENTANA.blit(texto_nivel, (10, 40))
    texto_vidas = fuente.render(f'Vidas: {jugador.vidas}', True, BLANCO)
    VENTANA.blit(texto_vidas, (10, 70))

    # Después de dibujar todo, actualizar la pantalla
    pygame.display.flip()

    # Controlar los FPS
    reloj.tick(FPS)

# Mostrar la pantalla de fin
pantalla_fin()

pygame.quit()"""

import pygame
import random
import os
import json

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana del juego
ANCHO = 800
ALTO = 600
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
    'obstacle': obtener_sprite(spritesheet, 447, 0, 16, 16)
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
    titulo = fuente.render("Altas Puntuaciones", True, NEGRO)
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
        self.potenciador_activo = False
        self.potenciador_tiempo = 0
        self.multishot_activo = False

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

        # Verificar tiempo del potenciador
        if self.potenciador_activo and pygame.time.get_ticks() - self.potenciador_tiempo > 5000:  # 5 segundos de duración
            self.velocidad //= 2
            self.potenciador_activo = False

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        self.sprites = sprites[f'enemy_{tipo}']
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidad_y = random.randrange(1, 4) if tipo != 'fast' else random.randrange(4, 7)
        self.velocidad_x = random.choice([-2, 2]) if tipo == 'strong' else 0
        self.animacion = 0
        self.contador_animacion = 0

    def update(self):
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        if self.rect.left < 0 or self.rect.right > ANCHO:
            self.velocidad_x *= -1
        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

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
        self.rect.center = (ANCHO // 2, -self.rect.height)
        self.velocidad_y = 1
        self.vida = 10
        self.animacion = 0
        self.contador_animacion = 0

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.y > ALTO // 2 - self.rect.height // 2:
            self.velocidad_y = 0  # El jefe se detiene en el centro de la pantalla

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
        pass

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto):
        super().__init__()
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image.blit(sprites['obstacle'], (0, 0))
class Mapa:
    def __init__(self, nivel):
        self.tiles = []
        self.cargar_mapa(nivel)

    def cargar_mapa(self, nivel):
        niveles = {
            1: [
                "gggggggggggggggggggg",
                "gddddggggddddddggggg",
                "gddddggggddddddggggg",
                "gggggggggggggggggggg",
                "ggggggwwgggggggggggg",
                "ggggggwwgggggggggggg",
                "gggggggggggggggggggg",
                "gggggggggggggggggggg",
                "gggggssswwssssssgggg",
                "gggggssswwssssssgggg"
            ],
            2: [
                "ssssssggggssssswwwww",
                "ssssssggggssssswwwww",
                "ssssssggggssssswwwww",
                "wwwwwwggggwwwwwwwwww",
                "wwwwwwggggwwwwwwwwww",
                "gggggggggggggggggggg",
                "gggggggggggggggggggg",
                "ddddddggggdddddddddd",
                "ddddddggggdddddddddd",
                "ddddddggggdddddddddd"
            ]
        }

        mapa_nivel = niveles[nivel]
        for fila in mapa_nivel:
            fila_tiles = []
            for tile in fila:
                if tile == "g":
                    fila_tiles.append(sprites['tile_grass'])
                elif tile == "d":
                    fila_tiles.append(sprites['tile_dirt'])
                elif tile == "w":
                    fila_tiles.append(sprites['tile_water'])
                elif tile == "s":
                    fila_tiles.append(sprites['tile_sand'])
            self.tiles.append(fila_tiles)

    def dibujar(self):
        for y, fila in enumerate(self.tiles):
            for x, tile in enumerate(fila):
                VENTANA.blit(tile, (x * 32, y * 32))

# Crear grupos de sprites
todos_los_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
balas = pygame.sprite.Group()
potenciadores = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()

# Crear instancia del jugador
jugador = Jugador()
todos_los_sprites.add(jugador)

jefe = Jefe()
todos_los_sprites.add(jefe)

# Función para crear enemigos
def crear_enemigos(n):
    for _ in range(n):
        tipo = random.choice(['basic', 'fast', 'strong'])
        enemigo = Enemigo(tipo)
        todos_los_sprites.add(enemigo)
        enemigos.add(enemigo)

# Crear los primeros enemigos
crear_enemigos(10)

# Crear obstáculos
obstaculo1 = Obstaculo(300, 200, 100, 100)
obstaculo2 = Obstaculo(500, 400, 100, 100)
todos_los_sprites.add(obstaculo1)
todos_los_sprites.add(obstaculo2)
obstaculos.add(obstaculo1)
obstaculos.add(obstaculo2)

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
        pygame.display.flip()
        reloj.tick(FPS)

# Mostrar la pantalla de inicio
pantalla_inicio()

# Variables del juego
nivel = 1
mapa = Mapa(nivel)
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
                
            """if evento.key == pygame.K_SPACE:
                direcciones = ['up', 'down', 'left', 'right']
                for direccion in direcciones:
                    bala = Bala(jugador.rect.centerx, jugador.rect.centery, direccion)
                    todos_los_sprites.add(bala)
                    balas.add(bala)
                sonido_disparo.play()"""
    
    #MANTENER PULSADO EL BOTÓN DE DISPARAR
    """keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        bala = Bala(jugador.rect.centerx, jugador.rect.centery, 'down')
        todos_los_sprites.add(bala)
        balas.add(bala)
        sonido_disparo.play()
    if keys[pygame.K_UP]:
        bala = Bala(jugador.rect.centerx, jugador.rect.centery, 'up')
        todos_los_sprites.add(bala)
        balas.add(bala)
        sonido_disparo.play()
    if keys[pygame.K_RIGHT]:
        bala = Bala(jugador.rect.centerx, jugador.rect.centery, 'right')
        todos_los_sprites.add(bala)
        balas.add(bala)
        sonido_disparo.play()
    if keys[pygame.K_LEFT]:
        bala = Bala(jugador.rect.centerx, jugador.rect.centery, 'left')
        todos_los_sprites.add(bala)
        balas.add(bala)
        sonido_disparo.play()"""
        
    
    # Actualizar
    todos_los_sprites.update()

    # Comprobar colisiones
    colisiones_enemigos = pygame.sprite.groupcollide(enemigos, balas, True, True)
    for colision in colisiones_enemigos:
        jugador.puntuacion += 10
        if random.random() < 0.1:  # 10% de probabilidad de que aparezca un potenciador
            tipo_potenciador = random.choice(['speed', 'live', 'multishot', 'explosive'])
            potenciador = Potenciador(colision.rect.x, colision.rect.y, tipo_potenciador)
            todos_los_sprites.add(potenciador)
            potenciadores.add(potenciador)
        sonido_golpe.play()

    colisiones_boss = pygame.sprite.spritecollide(jefe, balas, True, pygame.sprite.collide_mask)
    for colision in colisiones_boss:
        jefe.vida -= 1
        if jefe.vida == 0:
            jefe.kill()
            jefe_activo = False
            nivel += 1
            oleada = 1
            break

    #COLISIÓN DEL JUGADOR CON LOS ENEMIGOS
    if pygame.sprite.spritecollideany(jugador, enemigos):
        jugador.vidas -= 1
        if jugador.vidas <= 0:
            sonido_game_over.play()
            ejecutando = False
        else:
            for enemigo in enemigos:
                enemigo.kill()
            crear_enemigos(enemigos_por_oleada)

    #EFECTOS DISTINTOS POTENCIADORES AL COLISIONAR EL JUGADOR CON ELLOS
    colisiones_potenciadores = pygame.sprite.spritecollide(jugador, potenciadores, True)
    for colision in colisiones_potenciadores:
        sonido_potenciador.play()
        if colision.tipo == 'speed':
            jugador.velocidad *= 2
            jugador.potenciador_activo = True
            jugador.potenciador_tiempo = pygame.time.get_ticks()
        elif colision.tipo == 'live':
            jugador.vidas += 1

    # Subir de nivel cada 3 oleadas
    if not enemigos and not jefe_activo:
        if oleada % 3 == 0:
            jefe = Jefe()
            todos_los_sprites.add(jefe)
            jefe_activo = True
        else:
            oleada += 1
            crear_enemigos(enemigos_por_oleada)
            enemigos_por_oleada += 2

    # Dibujar / renderizar
    VENTANA.fill(BLANCO)
    todos_los_sprites.draw(VENTANA)

    # Dibujar la puntuación, nivel y vidas
    texto_puntuacion = fuente.render(f'Puntuación: {jugador.puntuacion}', True, NEGRO)
    VENTANA.blit(texto_puntuacion, (10, 10))
    texto_nivel = fuente.render(f'Nivel: {nivel}', True, NEGRO)
    VENTANA.blit(texto_nivel, (10, 40))
    texto_vidas = fuente.render(f'Vidas: {jugador.vidas}', True, NEGRO)
    VENTANA.blit(texto_vidas, (10, 70))

    # Dibujar tiempo restante del potenciador si está activo
    if jugador.potenciador_activo:
        tiempo_restante = 5 - (pygame.time.get_ticks() - jugador.potenciador_tiempo) // 1000
        texto_potenciador = fuente.render(f'Tiempo Potenciador: {tiempo_restante}', True, NEGRO)
        VENTANA.blit(texto_potenciador, (10, 100))

    # Después de dibujar todo, actualizar la pantalla
    pygame.display.flip()

    # Controlar los FPS
    reloj.tick(FPS)

# Mostrar la pantalla de fin
pantalla_fin()

pygame.quit()

