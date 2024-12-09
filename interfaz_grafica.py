import pygame
from tres_en_raya_supremo import TableroGrande  # Importamos la lógica del juego desde otro archivo
import sys

# Inicializar pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 600, 600  # Tamaño de la ventana
VENTANA = pygame.display.set_mode((ANCHO, ALTO))  # Crear la ventana de pygame
pygame.display.set_caption("Tres en Raya Supremo")  # Título de la ventana

# Colores en formato RGB (rojo, verde, azul)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (200, 200, 200)
VERDE = (0, 255, 0)

# Tamaño de las casillas
TAM_CASILLA = 200  # Tamaño de una celda grande (tablero grande)
TAM_CASILLA_PEQUEÑA = TAM_CASILLA // 3  # Tamaño de una celda pequeña (tablero pequeño)

# Inicializar el tablero
tablero = TableroGrande()  # Creamos una instancia del tablero grande
jugador_actual = "X"  # El primer jugador
tablero_restringido = None  # Restricción del tablero grande donde debe jugarse
juego_terminado = False  # Indica si el juego ha terminado
ganador_final = None  # Guardará el ganador para mostrarlo en pantalla


def obtener_casillas_ganadoras():
    """
    Obtiene las posiciones de las casillas grandes que formaron el 3 en raya.
    Solo se llama cuando hay un ganador en el tablero grande.
    """
    ganadoras = []  # Lista para almacenar las casillas ganadoras
    for i in range(3):
        # Verificar filas
        if all(tablero.tableros[i][j].ganador == ganador_final for j in range(3)):
            ganadoras.extend([(i, j) for j in range(3)])  # Añadir toda la fila
        # Verificar columnas
        if all(tablero.tableros[j][i].ganador == ganador_final for j in range(3)):
            ganadoras.extend([(j, i) for j in range(3)])  # Añadir toda la columna
    # Verificar diagonales
    if all(tablero.tableros[i][i].ganador == ganador_final for i in range(3)):
        ganadoras.extend([(i, i) for i in range(3)])  # Diagonal principal
    if all(tablero.tableros[i][2 - i].ganador == ganador_final for i in range(3)):
        ganadoras.extend([(i, 2 - i) for i in range(3)])  # Diagonal secundaria
    return ganadoras

def texto_centrado(texto, tamaño, color, x, y):
    """
    Dibuja un texto centrado en la pantalla en las coordenadas dadas.
    """
    fuente = pygame.font.Font(None, tamaño)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(x, y))
    VENTANA.blit(superficie, rect)


def dibujar_tablero(animar=False, casillas_ganadoras=None):
    """
    Dibuja el tablero grande y los tableros pequeños, incluyendo las fichas.
    Si 'animar' es True, aplica efectos visuales en las casillas ganadoras.
    """
    VENTANA.fill(BLANCO)  # Limpia la ventana con el color blanco

    # Mostrar texto indicando el turno actual
    texto_turno = f"Turno del jugador: {'X' if jugador_actual == 'X' else 'O'}"
    texto_centrado(texto_turno, 40, ROJO if jugador_actual == 'X' else AZUL, ANCHO // 2, 30)

    # Dibujar líneas divisorias del tablero grande
    for x in range(TAM_CASILLA, ANCHO, TAM_CASILLA):
        pygame.draw.line(VENTANA, NEGRO, (x, 50), (x, ALTO), 13)  # Líneas verticales
    for y in range(TAM_CASILLA + 50, ALTO, TAM_CASILLA):
        pygame.draw.line(VENTANA, NEGRO, (0, y), (ANCHO, y), 13)  # Líneas horizontales

    # Dibujar las casillas del tablero pequeño
    for fila in range(3):
        for columna in range(3):
            tablero_pequeno = tablero.tableros[fila][columna]
            # Dibujar casillas del tablero pequeño si no hay ganador
            if not tablero_pequeno.ganador:
                for i in range(3):
                    for j in range(3):
                        x = columna * TAM_CASILLA + j * TAM_CASILLA_PEQUEÑA
                        y = fila * TAM_CASILLA + i * TAM_CASILLA_PEQUEÑA + 50  # Desplazamos 50px por el texto
                        texto = tablero_pequeno.tablero[i][j]  # Ficha en la celda

                        # Determinar color según el estado
                        if animar and (fila, columna) in casillas_ganadoras:  # Animar casillas ganadoras
                            color = VERDE
                        elif texto == "X":  # Ficha X
                            color = ROJO
                        elif texto == "O":  # Ficha O
                            color = AZUL
                        else:  # Casilla vacía
                            color = NEGRO

                        # Dibujar rectángulos para las casillas
                        pygame.draw.rect(VENTANA, GRIS if tablero_restringido and tablero_restringido != (fila, columna) else BLANCO,
                                         (x, y, TAM_CASILLA_PEQUEÑA - 5, TAM_CASILLA_PEQUEÑA - 5))
                        # Dibujar las fichas
                        if texto != " ":
                            font = pygame.font.Font(None, 50)  # Fuente para las fichas
                            text_surface = font.render(texto, True, color)  # Renderizar el texto
                            text_rect = text_surface.get_rect(center=(x + TAM_CASILLA_PEQUEÑA // 2, y + TAM_CASILLA_PEQUEÑA // 2))
                            VENTANA.blit(text_surface, text_rect)

            # Dibujar fondo y la X o el O grande si el tablero pequeño tiene un ganador
            else:
                # Calcular las coordenadas del rectángulo de fondo
                x_inicio = columna * TAM_CASILLA
                y_inicio = fila * TAM_CASILLA + 48  # Desplazamos 50px por el texto
                # Dibujar el rectángulo de fondo
                pygame.draw.rect(VENTANA, BLANCO, (x_inicio, y_inicio, TAM_CASILLA, TAM_CASILLA))
                # Dibujar la X o el O grande
                centro_x = x_inicio + TAM_CASILLA // 2
                centro_y = y_inicio + TAM_CASILLA // 2
                if tablero_pequeno.ganador == "X":
                    pygame.draw.line(VENTANA, ROJO, (centro_x - 50, centro_y - 50), (centro_x + 50, centro_y + 50), 10)
                    pygame.draw.line(VENTANA, ROJO, (centro_x - 50, centro_y + 50), (centro_x + 50, centro_y - 50), 10)
                elif tablero_pequeno.ganador == "O":
                    pygame.draw.circle(VENTANA, AZUL, (centro_x, centro_y), 60, 10)
   
    if tablero.ganador:
        casillas_ganadoras = obtener_casillas_ganadoras()
        animar_casillas_grandes_ganadoras(casillas_ganadoras)




def animar_casillas_grandes_ganadoras(casillas_ganadoras):
    """
    Anima las casillas grandes ganadoras en el tablero grande.
    """
    for _ in range(1):  # Parpadeo 3 veces
        # Cambiar el fondo de las casillas ganadoras a un color brillante
        for fila, columna in casillas_ganadoras:
            x = columna * TAM_CASILLA
            y = fila * TAM_CASILLA + 50
            pygame.draw.rect(VENTANA, VERDE, (x, y, TAM_CASILLA, TAM_CASILLA))
        pygame.display.flip()
        pygame.time.delay(100)

        # Restaurar el fondo original
        for fila, columna in casillas_ganadoras:
            x = columna * TAM_CASILLA
            y = fila * TAM_CASILLA + 50
            pygame.draw.rect(VENTANA, BLANCO, (x, y, TAM_CASILLA, TAM_CASILLA))
        pygame.display.flip()
        pygame.time.delay(100)


def mostrar_ganador(mensaje):
    """
    Muestra un mensaje en la pantalla al centro.
    """
    VENTANA.fill(BLANCO)  # Limpia la pantalla
    font = pygame.font.Font(None, 80)  # Fuente grande para el mensaje
    text_surface = font.render(mensaje, True, NEGRO)  # Renderizar el texto
    text_rect = text_surface.get_rect(center=(ANCHO // 2, ALTO // 2))  # Centrar el texto
    VENTANA.blit(text_surface, text_rect)  # Colocar el texto en la pantalla
    pygame.display.flip()  # Actualizar la pantalla
    pygame.time.delay(3000)  # Pausar 3 segundos



def manejar_clic(pos):
    """
    Maneja el clic del jugador en el tablero, respetando las restricciones del juego.
    """
    global jugador_actual, tablero_restringido, juego_terminado, ganador_final

    if juego_terminado:  # Ignorar clics si el juego terminó
        return

    # Ajustar la posición del clic debido al texto superior (desplazamiento de 50px)
    x, y = pos
    y -= 50  # Restar el desplazamiento

    # Si el clic está fuera del área del tablero, ignorarlo
    if y < 0:
        return

    # Convertir el clic en coordenadas del tablero grande y pequeño
    fila_grande = y // TAM_CASILLA
    columna_grande = x // TAM_CASILLA
    fila_pequeña = (y % TAM_CASILLA) // TAM_CASILLA_PEQUEÑA
    columna_pequeña = (x % TAM_CASILLA) // TAM_CASILLA_PEQUEÑA

    # Restringir movimientos al tablero permitido
    if tablero_restringido and tablero_restringido != (fila_grande, columna_grande):
        print("Debes jugar en el tablero grande restringido.")
        return

    # Intentar colocar la ficha
    if tablero.colocar_ficha(jugador_actual, fila_grande, columna_grande, fila_pequeña, columna_pequeña):
        tablero_restringido = (fila_pequeña, columna_pequeña)  # Actualizar restricción

        # Permitir elección libre si el tablero está lleno o ganado
        if not tablero.tablero_disponible(fila_pequeña, columna_pequeña):
            tablero_restringido = None

        # Cambiar de jugador
        jugador_actual = "O" if jugador_actual == "X" else "X"

        # Verificar si el juego terminó
        if tablero.ganador:
            ganador_final = tablero.ganador
            casillas_ganadoras = obtener_casillas_ganadoras()
            for _ in range(3):  # Animar casillas ganadoras
                dibujar_tablero(animar=True, casillas_ganadoras=casillas_ganadoras)
                pygame.display.flip()
                pygame.time.delay(500)
                dibujar_tablero(animar=False)
                pygame.display.flip()
                pygame.time.delay(500)
            mostrar_ganador(f"¡{ganador_final} gana el juego!")
            juego_terminado = True
        elif all(t.esta_lleno() for fila in tablero.tableros for t in fila):
            mostrar_ganador("¡Empate! Tableros llenos.")
            juego_terminado = True
    else:
        print("Movimiento inválido. Intenta de nuevo.")

def menu_post_partida(ganador=None):
    """
    Muestra el menú después de terminar una partida.
    Permite al jugador reiniciar el juego o volver al menú principal.
    """
    corriendo = True

    # Crear botones
    botones = {
        "reiniciar": pygame.Rect(ANCHO // 2 - 100, 250, 200, 50),
        "menu": pygame.Rect(ANCHO // 2 - 100, 350, 200, 50)
    }

    while corriendo:
        VENTANA.fill(BLANCO)

        # Mensaje de victoria o empate
        if ganador:
            texto_centrado(f"¡{ganador} gana!", 60, ROJO if ganador == "X" else AZUL, ANCHO // 2, 150)
        else:
            texto_centrado("¡Empate!", 60, NEGRO, ANCHO // 2, 150)

        # Dibujar botones
        for nombre, rect in botones.items():
            color = GRIS if rect.collidepoint(pygame.mouse.get_pos()) else NEGRO
            pygame.draw.rect(VENTANA, color, rect)
            texto_centrado(
                "Jugar de Nuevo" if nombre == "reiniciar" else "Volver al Menú",
                30, BLANCO, rect.centerx, rect.centery
            )

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Clic izquierdo
                pos = pygame.mouse.get_pos()
                if botones["reiniciar"].collidepoint(pos):
                    return "reiniciar"
                elif botones["menu"].collidepoint(pos):
                    return "menu"

        pygame.display.flip()


def main(configuracion):
    """
    Bucle principal del juego con pygame.
    Acepta configuraciones de colores desde el menú.
    """
    global tablero, jugador_actual, tablero_restringido, juego_terminado, ganador_final

    # Inicializar configuración de colores
    global ROJO, AZUL, BLANCO
    ROJO = configuracion["color_x"]
    AZUL = configuracion["color_o"]
    BLANCO = configuracion["color_tablero"]

    corriendo = True
    while corriendo:
        # Inicializar estado del juego
        tablero = TableroGrande()
        jugador_actual = "X"
        tablero_restringido = None
        juego_terminado = False
        ganador_final = None

        while not juego_terminado:
            for evento in pygame.event.get():  # Capturar eventos
                if evento.type == pygame.QUIT:  # Cerrar la ventana
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:  # Clic del mouse
                    manejar_clic(evento.pos)

            dibujar_tablero()  # Actualizar el tablero en cada iteración
            pygame.display.flip()  # Actualizar la pantalla

        # Menú post-partida
        accion = menu_post_partida(ganador=ganador_final)
        if accion == "menu":
            corriendo = False  # Salir del bucle principal para volver al menú
        elif accion == "reiniciar":
            continue  # Reiniciar la partida

    pygame.quit()  # Salir de pygame



if __name__ == "__main__":
    main()
