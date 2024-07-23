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
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                "W.............D...............W",
                "W.......O.....................W",
                "W...........WWW...............W",
                "W.............W...............W",
                "W.....O.......................W",
                "W.............................W",
                "W.......D.....................W",
                "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
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
                elif tile == "O":
                    obstaculoL = Obstacle(x*16, y*16)
                    self.obstaculos.add(obstaculoL)
                    self.tiles.append((sprites['obstacle_log'], x * 16, y * 16))
                elif tile == "B":
                    obstaculoB = Obstacle(x*16, y*16)
                    self.obstaculos.add(obstaculoB)
                    self.tiles.append((sprites['obstacle_bush'], x * 16, y * 16))
                    
    def dibujar(self):
        for tile, x, y in self.tiles:
            VENTANA.blit(tile, (x, y))
        self.obstaculos.draw(VENTANA)
