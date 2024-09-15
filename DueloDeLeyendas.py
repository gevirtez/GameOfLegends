import pygame
import random
import sys
import textwrap

# Inicializar Pygame
pygame.init()

# Definir colores mejorados
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
CREMA = (255, 248, 220)
MARRON_CLARO = (205, 133, 63)
DORADO = (218, 165, 32)
VERDE_OSCURO = (0, 100, 0)
ROJO_OSCURO = (139, 0, 0)
AZUL_CIELO = (135, 206, 235)
GRIS_OSCURO = (64, 64, 64)

# Definir dimensiones de la pantalla
ANCHO = 1280
ALTO = 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Leyendas de Latinoamérica: Duelo de Héroes")

# Definir el reloj para controlar los FPS
reloj = pygame.time.Clock()

# Cargar imágenes de los personajes (asumiendo que existen)
imagenes = {
    "Simón Bolívar": pygame.image.load("images/bolivar.jpg"),
    "Che Guevara": pygame.image.load("images/guevara.jpg"),
    "Evita Perón": pygame.image.load("images/evita.jpeg"),
    "Fidel Castro": pygame.image.load("images/castro.jpeg"),
    "Hermanas Mirabal": pygame.image.load("images/mirabal.jpeg")
}

# Clase para cada personaje histórico
class Personaje:
    def __init__(self, nombre, habilidad, fuerza, estrategia, influencia, imagen, bio, caracteristicas):
        self.nombre = nombre
        self.habilidad = habilidad
        self.fuerza = fuerza
        self.estrategia = estrategia
        self.influencia = influencia
        self.imagen = pygame.transform.scale(imagen, (140, 140))
        self.rect = self.imagen.get_rect()
        self.nivel = 1
        self.experiencia = 0
        self.bio = bio
        self.caracteristicas = caracteristicas
        self.seleccionado = False
        self.victorias = 0
        self.hover = False

    def dibujar(self, x, y):
        self.rect.topleft = (x, y)
        
        # Efecto de hover
        if self.hover:
            pygame.draw.rect(pantalla, DORADO, (x-5, y-5, 180, 280), border_radius=15)
        
        # Dibujar sombra de la carta
        pygame.draw.rect(pantalla, GRIS_OSCURO, (x+5, y+5, 170, 270), border_radius=10)
        
        # Dibujar fondo de la carta
        color_borde = DORADO if self.seleccionado else MARRON_CLARO
        pygame.draw.rect(pantalla, color_borde, (x, y, 170, 270), border_radius=10)
        pygame.draw.rect(pantalla, CREMA, (x+5, y+5, 160, 260), border_radius=8)
        
        # Dibujar imagen con borde
        pygame.draw.rect(pantalla, MARRON_CLARO, (x+15, y+15, 140, 140), border_radius=5)
        pantalla.blit(self.imagen, (x+15, y+15))
        
        fuente_nombre = pygame.font.Font(None, 22)
        fuente_stats = pygame.font.Font(None, 18)
        texto_nombre = fuente_nombre.render(self.nombre, True, NEGRO)
        texto_habilidad = fuente_stats.render(f"Habilidad: {self.habilidad}", True, NEGRO)
        texto_fuerza = fuente_stats.render(f"Fuerza: {self.fuerza}", True, NEGRO)
        texto_estrategia = fuente_stats.render(f"Estrategia: {self.estrategia}", True, NEGRO)
        texto_influencia = fuente_stats.render(f"Influencia: {self.influencia}", True, NEGRO)

        pantalla.blit(texto_nombre, (x + 10, y + 160))
        pantalla.blit(texto_habilidad, (x + 10, y + 185))
        pantalla.blit(texto_fuerza, (x + 10, y + 205))
        pantalla.blit(texto_estrategia, (x + 10, y + 225))
        pantalla.blit(texto_influencia, (x + 10, y + 245))
    
    def dibujar_info_adicional(self, x, y):
        fuente_stats = pygame.font.Font(None, 18)
        texto_nivel = fuente_stats.render(f"Nivel: {self.nivel}", True, NEGRO)
        texto_victorias = fuente_stats.render(f"Victorias: {self.victorias}", True, VERDE_OSCURO)
        
        pantalla.blit(texto_nivel, (x, y))
        pantalla.blit(texto_victorias, (x, y + 20))
        pygame.draw.rect(pantalla, VERDE_OSCURO, (x, y + 40, 100 * (self.experiencia / 100), 5))

    def ganar_experiencia(self, cantidad):
        self.experiencia += cantidad
        if self.experiencia >= 100:
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.experiencia -= 100
        self.fuerza += random.randint(1, 2)
        self.estrategia += random.randint(1, 2)
        self.influencia += random.randint(1, 2)

# Crear personajes históricos
personajes = [
    Personaje("Simón Bolívar", "Independencia", 8, 9, 10, imagenes["Simón Bolívar"], 
              "Libertador de América del Sur, luchó por la independencia de varios países.",
              ["Lideró la independencia de seis países.", "Cruzó los Andes con su ejército.", "Propuso la unión de las naciones latinoamericanas."]),
    Personaje("Che Guevara", "Revolución", 7, 8, 9, imagenes["Che Guevara"], 
              "Revolucionario argentino, figura clave en la Revolución Cubana.",
              ["Fue médico de profesión.", "Participó en revoluciones en varios países.", "Es Símbolo de la contracultura."]),
    Personaje("Evita Perón", "Activismo", 6, 9, 8, imagenes["Evita Perón"], 
              "Primera Dama de Argentina, luchó por los derechos de los trabajadores y las mujeres.",
              ["Impulsó el voto femenino en Argentina.", "Creó la Fundación Eva Perón.", "Fue defensora de los 'descamisados.'"]),
    Personaje("Fidel Castro", "Revolución", 7, 8, 9, imagenes["Fidel Castro"], 
              "Líder revolucionario y ex-presidente de Cuba.",
              ["Lideró la Revolución Cubana.", "Gobernó Cuba por casi 50 años.", "Sobrevivió a numerosos intentos de asesinato."]),
    Personaje("Hermanas Mirabal", "Activismo", 5, 8, 9, imagenes["Hermanas Mirabal"], 
              "Hermanas dominicanas que se opusieron a la dictadura de Trujillo.",
              ["Son conocidas como 'Las Mariposas'.", "Son símbolos de la resistencia feminista.", "Su asesinato provocó la caída de Trujillo."])
]

# Desafíos históricos
desafios = [
    {"nombre": "Liberación de un país", "fuerza": 7, "estrategia": 7, "influencia": 8},
    {"nombre": "Revolución Social", "fuerza": 6, "estrategia": 8, "influencia": 9},
    {"nombre": "Movimiento Feminista", "fuerza": 5, "estrategia": 8, "influencia": 8},
    {"nombre": "Reforma Educativa", "fuerza": 5, "estrategia": 9, "influencia": 7},
    {"nombre": "Resistencia Pacífica", "fuerza": 4, "estrategia": 9, "influencia": 8},
    {"nombre": "Unificación Continental", "fuerza": 8, "estrategia": 9, "influencia": 9},
    {"nombre": "Reforma Agraria", "fuerza": 6, "estrategia": 7, "influencia": 8},
    {"nombre": "Lucha contra la Corrupción", "fuerza": 6, "estrategia": 8, "influencia": 8},
    {"nombre": "Negociación de Tratados", "fuerza": 5, "estrategia": 9, "influencia": 9},
    {"nombre": "Campaña de Alfabetización", "fuerza": 4, "estrategia": 7, "influencia": 8},
    {"nombre": "Protección de Derechos Indígenas", "fuerza": 6, "estrategia": 7, "influencia": 9},
    {"nombre": "Defensa de Recursos Naturales", "fuerza": 7, "estrategia": 8, "influencia": 7},
    {"nombre": "Reforma del Sistema de Salud", "fuerza": 5, "estrategia": 8, "influencia": 8},
    {"nombre": "Movimiento de Trabajadores", "fuerza": 7, "estrategia": 7, "influencia": 8},
    {"nombre": "Campaña Anti-imperialista", "fuerza": 8, "estrategia": 8, "influencia": 9},
    {"nombre": "Preservación Cultural", "fuerza": 5, "estrategia": 7, "influencia": 9},
    {"nombre": "Reforma Constitucional", "fuerza": 6, "estrategia": 9, "influencia": 8},
    {"nombre": "Movimiento Estudiantil", "fuerza": 7, "estrategia": 7, "influencia": 8},
    {"nombre": "Reconciliación Nacional", "fuerza": 5, "estrategia": 8, "influencia": 9}
]

# Mostrar desafío
def mostrar_desafio(desafio, x, y):
    pygame.draw.rect(pantalla, MARRON_CLARO, (x-5, y-5, 610, 130), border_radius=10)
    pygame.draw.rect(pantalla, CREMA, (x, y, 600, 120), border_radius=10)
    fuente = pygame.font.Font(None, 36)
    texto_desafio = fuente.render(f"Desafío: {desafio['nombre']}", True, NEGRO)
    texto_fuerza = fuente.render(f"Fuerza: {desafio['fuerza']}", True, NEGRO)
    texto_estrategia = fuente.render(f"Estrategia: {desafio['estrategia']}", True, NEGRO)
    texto_influencia = fuente.render(f"Influencia: {desafio['influencia']}", True, NEGRO)

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
    color = VERDE_OSCURO if all(resultado) else ROJO_OSCURO
    texto = "¡Victoria!" if all(resultado) else "Derrota"
    fuente = pygame.font.Font(None, 48)
    texto_resultado = fuente.render(texto, True, color)
    pantalla.blit(texto_resultado, (x, y))

# Botón interactivo
def dibujar_boton(texto, x, y, ancho, alto, color, color_texto=BLANCO, hover=False):
    if hover:
        pygame.draw.rect(pantalla, DORADO, (x-2, y-2, ancho+4, alto+4), border_radius=10)
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto), border_radius=10)
    fuente = pygame.font.Font(None, 28)
    texto_render = fuente.render(texto, True, color_texto)
    texto_rect = texto_render.get_rect(center=(x + ancho // 2, y + alto // 2))
    pantalla.blit(texto_render, texto_rect)
    return pygame.Rect(x, y, ancho, alto)

# Mostrar introducción del personaje
def mostrar_introduccion(personaje, caracteristica):
    pantalla.fill(CREMA)
    pygame.draw.rect(pantalla, MARRON_CLARO, (ANCHO//4-5, ALTO//4-5, ANCHO//2+10, ALTO//2+10), border_radius=10)
    pygame.draw.rect(pantalla, AZUL_CIELO, (ANCHO//4, ALTO//4, ANCHO//2, ALTO//2), border_radius=10)
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_texto = pygame.font.Font(None, 24)
    
    titulo = fuente_titulo.render(personaje.nombre, True, NEGRO)
    pantalla.blit(titulo, (ANCHO//4 + 10, ALTO//4 + 10))
    
    lineas_bio = textwrap.wrap(personaje.bio, width=50)
    for i, linea in enumerate(lineas_bio):
        texto_bio = fuente_texto.render(linea, True, NEGRO)
        pantalla.blit(texto_bio, (ANCHO//4 + 10, ALTO//4 + 60 + i*30))
    
    texto_caracteristica = f"¿Sabías que...? {caracteristica}"
    texto_envuelto = textwrap.wrap(texto_caracteristica, width=50)
    for i, linea in enumerate(texto_envuelto):
        texto_linea = fuente_texto.render(linea, True, NEGRO)
        pantalla.blit(texto_linea, (ANCHO//4 + 10, ALTO//4 + 150 + i*30))
    
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

# Mostrar pantalla de fin de juego
def mostrar_fin_juego(puntuacion, ronda):
    pantalla.fill(AZUL_CIELO)
    fuente_titulo = pygame.font.Font(None, 64)
    fuente_texto = pygame.font.Font(None, 36)
    
    titulo = fuente_titulo.render("¡Fin del Juego!", True, NEGRO)
    texto_puntuacion = fuente_texto.render(f"Puntuación final: {puntuacion}", True, NEGRO)
    texto_ronda = fuente_texto.render(f"Rondas jugadas: {ronda}", True, NEGRO)
    
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//4))
    pantalla.blit(texto_puntuacion, (ANCHO//2 - texto_puntuacion.get_width()//2, ALTO//2))
    pantalla.blit(texto_ronda, (ANCHO//2 - texto_ronda.get_width()//2, ALTO//2 + 50))
    
    boton_salir = dibujar_boton("Salir", ANCHO//2 - 50, ALTO - 100, 100, 50, MARRON_CLARO)
    
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_salir.collidepoint(evento.pos):
                    esperando = False

# Mostrar introducción del juego
def mostrar_introduccion_juego():
    pantalla.fill(AZUL_CIELO)
    fuente_titulo = pygame.font.Font(None, 64)
    fuente_texto = pygame.font.Font(None, 28)
    
    titulo = fuente_titulo.render("Leyendas de Latinoamérica: Duelo de Héroes", True, NEGRO)
    texto_intro = [
        "¡Bienvenido a un viaje por la historia latinoamericana!",
        "En este juego, asumirás el papel de figuras legendarias",
        "que dieron forma al destino del continente.",
        "",
        "En cada ronda, enfrentarás un desafío histórico.",
        "Elige sabiamente a tu héroe, considerando sus habilidades únicas",
        "y las exigencias de cada situación.",
        "",
        "Aprende sobre estos personajes extraordinarios mientras juegas,",
        "¡y guíalos a la victoria en la lucha por un futuro mejor!",
        "",
        "¿Estás listo para hacer historia?"
    ]
    
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, ALTO//6))
    
    for i, linea in enumerate(texto_intro):
        texto = fuente_texto.render(linea, True, NEGRO)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//3 + i*30))
    
    boton_inicio = dibujar_boton("Comenzar Juego", ANCHO//2 - 75, ALTO - 100, 165, 50, MARRON_CLARO)
    
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_inicio.collidepoint(evento.pos):
                    esperando = False



# Lógica principal del juego
def juego():
    mostrar_introduccion_juego()
    
    fin = False
    seleccion = None
    desafios_restantes = desafios.copy()  # Copiamos la lista original de desafíos
    desafio_actual = random.choice(desafios_restantes)
    desafios_restantes.remove(desafio_actual)  # Eliminamos el desafío seleccionado de la lista
    resultado = None
    puntuacion = 0
    ronda = 1
    max_rondas = 10  # Número máximo de rondas
    seleccion_hecha = False
    boton_siguiente_desafio = pygame.Rect(ANCHO - 180, ALTO - 60, 180, 50)
    boton_hover = False

    while not fin and ronda <= max_rondas:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fin = True
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si se seleccionó una carta
                if not seleccion_hecha:
                    for personaje in personajes:
                        if personaje.rect.collidepoint(evento.pos) and not personaje.seleccionado:
                            seleccion = personaje
                            personaje.seleccionado = True
                            caracteristica = random.choice(personaje.caracteristicas)
                            mostrar_introduccion(seleccion, caracteristica)
                            resultado = comparar_estadisticas(seleccion, desafio_actual)
                            if all(resultado):
                                puntuacion += 1
                                seleccion.victorias += 1
                                seleccion.ganar_experiencia(20)
                            seleccion_hecha = True
                            break

                # Verificar si se presionó el botón de siguiente desafío
                if boton_siguiente_desafio.collidepoint(evento.pos) and seleccion_hecha:
                    desafio_actual = random.choice(desafios_restantes)
                    desafios_restantes.remove(desafio_actual)  # Eliminamos el desafío seleccionado
                    seleccion = None
                    resultado = None
                    ronda += 1
                    seleccion_hecha = False
                    for personaje in personajes:
                        personaje.seleccionado = False
            
            elif evento.type == pygame.MOUSEMOTION:
                # Actualizar estado de hover para personajes y botón
                for personaje in personajes:
                    personaje.hover = personaje.rect.collidepoint(evento.pos)
                boton_hover = boton_siguiente_desafio.collidepoint(evento.pos)

        pantalla.fill(CREMA)

        # Mostrar desafío actual
        mostrar_desafio(desafio_actual, 50, 50)

        # Dibujar personajes en pantalla
        for i, personaje in enumerate(personajes):
            personaje.dibujar(50 + i * 240, 200)

        # Mostrar el resultado
        if resultado is not None:
            mostrar_resultado(resultado, ANCHO // 2 - 100, ALTO - 100)

        # Mostrar puntuación y ronda
        fuente = pygame.font.Font(None, 36)
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, NEGRO)
        texto_ronda = fuente.render(f"Ronda: {ronda}/{max_rondas}", True, NEGRO)
        pantalla.blit(texto_puntuacion, (20, ALTO - 40))
        pantalla.blit(texto_ronda, (20, ALTO - 80))

        # Dibujar botón
        boton_siguiente_desafio = dibujar_boton("Siguiente Desafío", ANCHO - 180, ALTO - 60, 180, 50, MARRON_CLARO, NEGRO, boton_hover)

        pygame.display.flip()
        reloj.tick(60)

    mostrar_fin_juego(puntuacion, ronda - 1)

    pygame.quit()
    sys.exit()

# Iniciar juego
if __name__ == "__main__":
    juego()