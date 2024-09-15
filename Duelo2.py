import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AZUL = (100, 100, 255)
ROJO = (255, 100, 100)
VERDE = (100, 255, 100)

# Definir dimensiones de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Duelo de Leyendas")

# Definir el reloj para controlar los FPS
reloj = pygame.time.Clock()

# Cargar imágenes de los personajes
imagenes = {
    "Simón Bolívar": pygame.image.load("bolivar.png"),
    "Che Guevara": pygame.image.load("guevara.png"),
    "Evita Perón": pygame.image.load("evita.png"),
    "Fidel Castro": pygame.image.load("castro.png"),
    "Mirabal Sisters": pygame.image.load("mirabal.png")
}

# Clase para cada personaje histórico
class Personaje:
    def __init__(self, nombre, habilidad, fuerza, estrategia, influencia, imagen):
        self.nombre = nombre
        self.habilidad = habilidad
        self.fuerza = fuerza
        self.estrategia = estrategia
        self.influencia = influencia
        self.imagen = imagen

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
]

# Dibujar carta
def dibujar_carta(personaje, x, y, seleccionada=False):
    color = VERDE if seleccionada else NEGRO
    pygame.draw.rect(pantalla, color, (x, y, 200, 300))
    pantalla.blit(pygame.transform.scale(personaje.imagen, (180, 180)), (x + 10, y + 10))

    fuente = pygame.font.Font(None, 30)
    texto_nombre = fuente.render(personaje.nombre, True, BLANCO)
    pantalla.blit(texto_nombre, (x + 10, y + 200))

# Mostrar desafío
def mostrar_desafio(desafio, x, y):
    pygame.draw.rect(pantalla, AZUL, (x, y, 500, 100))
    fuente = pygame.font.Font(None, 36)
    texto_desafio = fuente.render(f"Desafío: {desafio['nombre']}", True, BLANCO)
    texto_fuerza = fuente.render(f"Fuerza: {desafio['fuerza']}", True, BLANCO)
    texto_estrategia = fuente.render(f"Estrategia: {desafio['estrategia']}", True, BLANCO)
    texto_influencia = fuente.render(f"Influencia: {desafio['influencia']}", True, BLANCO)

    pantalla.blit(texto_desafio, (x + 10, y + 10))
    pantalla.blit(texto_fuerza, (x + 10, y + 50))
    pantalla.blit(texto_estrategia, (x + 200, y + 50))
    pantalla.blit(texto_influencia, (x + 400, y + 50))

# Comparar las estadísticas del personaje con el desafío
def comparar_estadisticas(personaje, desafio):
    resultado_fuerza = personaje.fuerza >= desafio['fuerza']
    resultado_estrategia = personaje.estrategia >= desafio['estrategia']
    resultado_influencia = personaje.influencia >= desafio['influencia']

    return resultado_fuerza, resultado_estrategia, resultado_influencia

# Lógica principal del juego
def juego():
    fin = False
    seleccion = None
    desafio_actual = random.choice(desafios)
    resultado = None

    while not fin:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fin = True
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se seleccionó una carta
                for i, personaje in enumerate(personajes):
                    if 100 + i * 250 <= evento.pos[0] <= 300 + i * 250 and 200 <= evento.pos[1] <= 500:
                        seleccion = personaje
                        resultado = comparar_estadisticas(seleccion, desafio_actual)

        pantalla.fill(GRIS)

        # Mostrar desafío actual
        mostrar_desafio(desafio_actual, 150, 50)

        # Dibujar personajes en pantalla
        for i, personaje in enumerate(personajes):
            dibujar_carta(personaje, 100 + i * 250, 200, seleccion == personaje)

        # Mostrar el resultado
        if resultado is not None:
            fuente = pygame.font.Font(None, 36)
            resultado_texto = "Ganaste" if all(resultado) else "Perdiste"
            texto_resultado = fuente.render(resultado_texto, True, ROJO if resultado_texto == "Perdiste" else VERDE)
            pantalla.blit(texto_resultado, (350, 550))

        pygame.display.flip()
        reloj.tick(60)

# Iniciar juego
juego()
pygame.quit()
