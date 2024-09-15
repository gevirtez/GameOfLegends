import pygame
import random
import sys

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AZUL = (100, 100, 255)
ROJO = (255, 100, 100)
VERDE = (100, 255, 100)
AMARILLO = (255, 255, 0)

# Definir dimensiones de la pantalla
ANCHO = 1024
ALTO = 768
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Duelo de Leyendas Interactivo")

# Definir el reloj para controlar los FPS
reloj = pygame.time.Clock()

# Cargar imágenes y sonidos
imagenes = {
    "Simón Bolívar": pygame.image.load("bolivar.png"),
    "Che Guevara": pygame.image.load("guevara.png"),
    "Evita Perón": pygame.image.load("evita.png"),
    "Fidel Castro": pygame.image.load("castro.png"),
    "Mirabal Sisters": pygame.image.load("mirabal.png")
}

sonidos = {
    "victoria": pygame.mixer.Sound("victoria.wav"),
    "derrota": pygame.mixer.Sound("derrota.wav"),
    "seleccion": pygame.mixer.Sound("seleccion.wav"),
    "nuevo_desafio": pygame.mixer.Sound("nuevo_desafio.wav")
}

# Clase para cada personaje histórico
class Personaje:
    def __init__(self, nombre, habilidad, fuerza, estrategia, influencia, imagen):
        self.nombre = nombre
        self.habilidad = habilidad
        self.fuerza = fuerza
        self.estrategia = estrategia
        self.influencia = influencia
        self.imagen = pygame.transform.scale(imagen, (180, 180))
        self.rect = self.imagen.get_rect()
        self.nivel = 1
        self.experiencia = 0

    def dibujar(self, x, y, seleccionada=False):
        self.rect.topleft = (x, y)
        color = VERDE if seleccionada else NEGRO
        pygame.draw.rect(pantalla, color, (x, y, 200, 340))
        pantalla.blit(self.imagen, (x + 10, y + 10))

        fuente = pygame.font.Font(None, 24)
        texto_nombre = fuente.render(self.nombre, True, BLANCO)
        texto_habilidad = fuente.render(f"Habilidad: {self.habilidad}", True, BLANCO)
        texto_fuerza = fuente.render(f"Fuerza: {self.fuerza}", True, BLANCO)
        texto_estrategia = fuente.render(f"Estrategia: {self.estrategia}", True, BLANCO)
        texto_influencia = fuente.render(f"Influencia: {self.influencia}", True, BLANCO)
        texto_nivel = fuente.render(f"Nivel: {self.nivel}", True, AMARILLO)
        texto_exp = fuente.render(f"EXP: {self.experiencia}/100", True, AMARILLO)

        pantalla.blit(texto_nombre, (x + 10, y + 200))
        pantalla.blit(texto_habilidad, (x + 10, y + 225))
        pantalla.blit(texto_fuerza, (x + 10, y + 250))
        pantalla.blit(texto_estrategia, (x + 10, y + 275))
        pantalla.blit(texto_influencia, (x + 10, y + 300))
        pantalla.blit(texto_nivel, (x + 10, y + 325))
        pantalla.blit(texto_exp, (x + 10, y + 350))

    def ganar_experiencia(self, cantidad):
        self.experiencia += cantidad
        if self.experiencia >= 100:
            self.nivel_up()

    def nivel_up(self):
        self.nivel += 1
        self.experiencia -= 100
        self.fuerza += random.randint(1, 2)
        self.estrategia += random.randint(1, 2)
        self.influencia += random.randint(1, 2)

# Crear personajes históricos
personajes = [
    Personaje("Simón Bolívar", "Independencia", 8, 9, 10, imagenes["Simón Bolívar"]),
    Personaje("Che Guevara", "Revolución", 7, 8, 9, imagenes["Che Guevara"]),
    Personaje("Evita Perón", "Activismo", 6, 9, 8, imagenes["Evita Perón"]),
    Personaje("Fidel Castro", "Revolución", 7, 8, 9, imagenes["Fidel Castro"]),
    Personaje("Mirabal Sisters", "Activismo", 5, 7, 9, imagenes["Mirabal Sisters"])
]

# Desafíos históricos
desafios = [
    {"nombre": "Liberación de un país", "fuerza": 8, "estrategia": 7, "influencia": 9},
    {"nombre": "Revolución Social", "fuerza": 7, "estrategia": 8, "influencia": 10},
    {"nombre": "Movimiento Feminista", "fuerza": 5, "estrategia": 9, "influencia": 8},
    {"nombre": "Reforma Educativa", "fuerza": 6, "estrategia": 9, "influencia": 7},
    {"nombre": "Resistencia Pacífica", "fuerza": 4, "estrategia": 10, "influencia": 9},
    {"nombre": "Unificación Continental", "fuerza": 9, "estrategia": 10, "influencia": 10},
    {"nombre": "Reforma Agraria", "fuerza": 7, "estrategia": 8, "influencia": 8},
    {"nombre": "Lucha contra la Corrupción", "fuerza": 6, "estrategia": 9, "influencia": 9}
]

# Mostrar desafío
def mostrar_desafio(desafio, x, y):
    pygame.draw.rect(pantalla, AZUL, (x, y, 600, 120))
    fuente = pygame.font.Font(None, 36)
    texto_desafio = fuente.render(f"Desafío: {desafio['nombre']}", True, BLANCO)
    texto_fuerza = fuente.render(f"Fuerza: {desafio['fuerza']}", True, BLANCO)
    texto_estrategia = fuente.render(f"Estrategia: {desafio['estrategia']}", True, BLANCO)
    texto_influencia = fuente.render(f"Influencia: {desafio['influencia']}", True, BLANCO)

    pantalla.blit(texto_desafio, (x + 10, y + 10))
    pantalla.blit(texto_fuerza, (x + 10, y + 50))
    pantalla.blit(texto_estrategia, (x + 210, y + 50))
    pantalla.blit(texto_influencia, (x + 410, y + 50))

# Comparar las estadísticas del personaje con el desafío
def comparar_estadisticas(personaje, desafio):
    resultado_fuerza = personaje.fuerza >= desafio['fuerza']
    resultado_estrategia = personaje.estrategia >= desafio['estrategia']
    resultado_influencia = personaje.influencia >= desafio['influencia']

    return resultado_fuerza, resultado_estrategia, resultado_influencia

# Mostrar resultado
def mostrar_resultado(resultado, x, y):
    color = VERDE if all(resultado) else ROJO
    texto = "¡Victoria!" if all(resultado) else "Derrota"
    fuente = pygame.font.Font(None, 48)
    texto_resultado = fuente.render(texto, True, color)
    pantalla.blit(texto_resultado, (x, y))

# Botón de nuevo desafío
def dibujar_boton(texto, x, y, ancho, alto, color):
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto))
    fuente = pygame.font.Font(None, 36)
    texto_render = fuente.render(texto, True, BLANCO)
    texto_rect = texto_render.get_rect(center=(x + ancho // 2, y + alto // 2))
    pantalla.blit(texto_render, texto_rect)
    return pygame.Rect(x, y, ancho, alto)

# Lógica principal del juego
def juego():
    fin = False
    seleccion = None
    desafio_actual = random.choice(desafios)
    resultado = None
    puntuacion = 0
    ronda = 1
    modo_historia = False
    historia_actual = None

    boton_nuevo_desafio = dibujar_boton("Nuevo Desafío", ANCHO - 200, ALTO - 60, 180, 50, AZUL)
    boton_modo_historia = dibujar_boton("Modo Historia", ANCHO - 200, ALTO - 120, 180, 50, VERDE)

    while not fin:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fin = True
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se seleccionó una carta
                for personaje in personajes:
                    if personaje.rect.collidepoint(evento.pos):
                        seleccion = personaje
                        sonidos["seleccion"].play()
                        resultado = comparar_estadisticas(seleccion, desafio_actual)
                        if all(resultado):
                            puntuacion += 1
                            seleccion.ganar_experiencia(20)
                            sonidos["victoria"].play()
                        else:
                            sonidos["derrota"].play()

                # Verificar si se presionó el botón de nuevo desafío
                if boton_nuevo_desafio.collidepoint(evento.pos):
                    desafio_actual = random.choice(desafios)
                    seleccion = None
                    resultado = None
                    ronda += 1
                    sonidos["nuevo_desafio"].play()
                    modo_historia = False

                # Verificar si se presionó el botón de modo historia
                if boton_modo_historia.collidepoint(evento.pos):
                    modo_historia = True
                    historia_actual = generar_historia()

        pantalla.fill(GRIS)

        # Mostrar desafío actual o historia
        if modo_historia:
            mostrar_historia(historia_actual, 50, 50)
        else:
            mostrar_desafio(desafio_actual, 50, 50)

        # Dibujar personajes en pantalla
        for i, personaje in enumerate(personajes):
            personaje.dibujar(50 + i * 220, 200, seleccion == personaje)

        # Mostrar el resultado
        if resultado is not None:
            mostrar_resultado(resultado, ANCHO // 2 - 100, ALTO - 150)

        # Mostrar puntuación y ronda
        fuente = pygame.font.Font(None, 36)
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, NEGRO)
        texto_ronda = fuente.render(f"Ronda: {ronda}", True, NEGRO)
        pantalla.blit(texto_puntuacion, (20, ALTO - 40))
        pantalla.blit(texto_ronda, (20, ALTO - 80))

        # Dibujar botones
        boton_nuevo_desafio = dibujar_boton("Nuevo Desafío", ANCHO - 200, ALTO - 60, 180, 50, AZUL)
        boton_modo_historia = dibujar_boton("Modo Historia", ANCHO - 200, ALTO - 120, 180, 50, VERDE)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()

def generar_historia():
    personaje = random.choice(personajes)
    evento = random.choice([
        f"{personaje.nombre} lidera una revolución en un país ficticio.",
        f"{personaje.nombre} organiza un movimiento de resistencia pacífica.",
        f"{personaje.nombre} implementa una reforma educativa radical.",
        f"{personaje.nombre} negocia un tratado de paz entre naciones en conflicto.",
        f"{personaje.nombre} funda un nuevo partido político con ideales revolucionarios."
    ])
    return f"{evento}\n\n¿Cómo responderías a esta situación?"

def mostrar_historia(historia, x, y):
    pygame.draw.rect(pantalla, VERDE, (x, y, 600, 150))
    fuente = pygame.font.Font(None, 24)
    lineas = historia.split('\n')
    for i, linea in enumerate(lineas):
        texto = fuente.render(linea, True, BLANCO)
        pantalla.blit(texto, (x + 10, y + 10 + i * 30))

# Iniciar juego
if __name__ == "__main__":
    juego()