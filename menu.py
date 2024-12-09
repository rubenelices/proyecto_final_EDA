import pygame
import sys
from interfaz_grafica import main as iniciar_juego  # Importa la función main para iniciar el juego

# Inicialización de pygame
pygame.init()

# Tamaño de la ventana
ANCHO, ALTO = 600, 650
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú Principal - Tres en Raya Supremo")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Configuración predeterminada
configuracion = {
    "color_x": ROJO,
    "color_o": AZUL,
    "color_tablero": BLANCO
}


def texto_centrado(texto, tamaño, color, x, y):
    """
    Dibuja un texto centrado en la pantalla.
    """
    fuente = pygame.font.Font(None, tamaño)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(x, y))
    VENTANA.blit(superficie, rect)


def mostrar_instrucciones():
    """
    Muestra las instrucciones del juego.
    """
    corriendo = True
    while corriendo:
        VENTANA.fill(BLANCO)
        texto_centrado("Instrucciones", 50, NEGRO, ANCHO // 2, 50)
        texto_centrado("1. Haz tres en raya en un tablero pequeño para ganar esa sección.", 25, NEGRO, ANCHO // 2, 150)
        texto_centrado("2. Gana tres tableros pequeños en línea para ganar el juego.", 25, NEGRO, ANCHO // 2, 200)
        texto_centrado("3. El movimiento está restringido al tablero indicado.", 25, NEGRO, ANCHO // 2, 250)
        texto_centrado("Presiona ESC para volver al menú.", 30, NEGRO, ANCHO // 2, 400)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                corriendo = False

        pygame.display.flip()


def personalizar_juego():
    """
    Permite a los jugadores personalizar los colores del juego.
    """
    corriendo = True
    while corriendo:
        VENTANA.fill(BLANCO)
        texto_centrado("Personalización", 50, NEGRO, ANCHO // 2, 50)

        texto_centrado("Presiona 1 para cambiar el color de X.", 30, NEGRO, ANCHO // 2, 150)
        texto_centrado("Presiona 2 para cambiar el color de O.", 30, NEGRO, ANCHO // 2, 200)
        texto_centrado("Presiona 3 para cambiar el color del tablero.", 30, NEGRO, ANCHO // 2, 250)
        texto_centrado("Presiona ESC para volver al menú.", 30, NEGRO, ANCHO // 2, 400)

        texto_centrado(f"Color X: {seleccion_color(configuracion['color_x'])}", 30, configuracion['color_x'], ANCHO // 2, 450)
        texto_centrado(f"Color O: {seleccion_color(configuracion['color_o'])}", 30, configuracion['color_o'], ANCHO // 2, 500)
        texto_centrado(f"Color del tablero: {seleccion_color(configuracion['color_tablero'])}", 30, configuracion['color_tablero'], ANCHO // 2, 550)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

        pygame.display.flip()


def seleccion_color(color):
    """
    Devuelve un texto descriptivo del color.
    """
    if color == ROJO:
        return "Rojo"
    elif color == AZUL:
        return "Azul"
    elif color == VERDE:
        return "Verde"
    elif color == GRIS:
        return "Gris"
    elif color == NEGRO:
        return "Negro"


def menu_principal():
    """
    Muestra el menú principal del juego con botones seleccionables mediante clics.
    """
    corriendo = True

    # Definir las áreas de los botones
    botones = {
        "iniciar": pygame.Rect(ANCHO // 2 - 100, 150, 200, 50),
        "instrucciones": pygame.Rect(ANCHO // 2 - 100, 250, 200, 50),
        "personalizar": pygame.Rect(ANCHO // 2 - 100, 350, 200, 50),
        "salir": pygame.Rect(ANCHO // 2 - 100, 450, 200, 50)
    }

    while corriendo:
        VENTANA.fill(BLANCO)

        # Dibujar título
        texto_centrado("Menú Principal", 60, NEGRO, ANCHO // 2, 50)

        # Dibujar botones y cambiar color si el ratón está sobre ellos
        for nombre, rect in botones.items():
            color = GRIS if rect.collidepoint(pygame.mouse.get_pos()) else NEGRO
            pygame.draw.rect(VENTANA, color, rect)
            texto_centrado(
                "Iniciar Juego" if nombre == "iniciar" else
                "Instrucciones" if nombre == "instrucciones" else
                "Personalizar" if nombre == "personalizar" else
                "Salir", 
                30, BLANCO, rect.centerx, rect.centery
            )

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Clic izquierdo
                pos = pygame.mouse.get_pos()
                if botones["iniciar"].collidepoint(pos):
                    iniciar_juego(configuracion)
                    corriendo = False
                elif botones["instrucciones"].collidepoint(pos):
                    mostrar_instrucciones()
                elif botones["personalizar"].collidepoint(pos):
                    personalizar_juego()
                elif botones["salir"].collidepoint(pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    menu_principal()
