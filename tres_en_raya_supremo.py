from colorama import Fore, Style

# Clase que representa un tablero pequeño (3x3)
class TableroPequeño:
    def __init__(self):
        # Inicializamos un tablero vacío y un ganador inicial nulo
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]  # Tablero vacío
        self.ganador = None  # Ganador de este tablero, si existe

    def colocar_ficha(self, jugador, fila, columna):
        """
        Intenta colocar una ficha en el tablero.
        Si la posición está vacía y el tablero no tiene un ganador, realiza el movimiento.
        """
        if self.tablero[fila][columna] == " " and not self.ganador:
            self.tablero[fila][columna] = jugador
            self.verificar_victoria(jugador)  # Comprueba si este movimiento genera una victoria
            return True
        return False

    def verificar_victoria(self, jugador):
        """
        Comprueba si el jugador ha ganado en este tablero.
        Revisa filas, columnas y diagonales.
        """
        for i in range(3):
            # Verificar filas
            if all(self.tablero[i][j] == jugador for j in range(3)):
                self.ganador = jugador
                return
            # Verificar columnas
            if all(self.tablero[j][i] == jugador for j in range(3)):
                self.ganador = jugador
                return
        # Verificar diagonales
        if all(self.tablero[i][i] == jugador for i in range(3)):
            self.ganador = jugador
            return
        if all(self.tablero[i][2 - i] == jugador for i in range(3)):
            self.ganador = jugador
            return

    def esta_lleno(self):
        """
        Devuelve True si el tablero está lleno o si tiene un ganador.
        """
        return self.ganador is not None or all(self.tablero[i][j] != " " for i in range(3) for j in range(3))

    def mostrar(self):
        """Muestra el tablero en consola con colores."""
        for fila in self.tablero:
            print(" | ".join(
                Fore.RED + celda + Style.RESET_ALL if celda == "X" else
                Fore.BLUE + celda + Style.RESET_ALL if celda == "O" else
                " " for celda in fila
            ))
            print("-" * 5)

# Clase que representa el tablero grande (3x3 de tableros pequeños)
class TableroGrande:
    def __init__(self):
        # Crea un tablero de 3x3, donde cada celda es un TableroPequeño
        self.tableros = [[TableroPequeño() for _ in range(3)] for _ in range(3)]
        self.ganador = None  # Ganador del tablero grande

    def colocar_ficha(self, jugador, tablero_fila, tablero_columna, casilla_fila, casilla_columna):
        """
        Coloca una ficha en el tablero grande, dentro del tablero pequeño especificado.
        """
        tablero = self.tableros[tablero_fila][tablero_columna]
        if tablero.colocar_ficha(jugador, casilla_fila, casilla_columna):
            # Si el tablero pequeño resulta en una victoria, se notifica
            if tablero.ganador:
                print(f"¡El jugador {jugador} ha ganado el tablero grande ({tablero_fila + 1}, {tablero_columna + 1})!")
            self.verificar_victoria(jugador)  # Verificar si el tablero grande tiene un ganador
            return True
        return False

    def verificar_victoria(self, jugador):
        """
        Comprueba si el jugador ha ganado en el tablero grande.
        Revisa filas, columnas y diagonales basándose en los ganadores de los tableros pequeños.
        """
        for i in range(3):
            # Verificar filas
            if all(self.tableros[i][j].ganador == jugador for j in range(3)):
                self.ganador = jugador
                return
            # Verificar columnas
            if all(self.tableros[j][i].ganador == jugador for j in range(3)):
                self.ganador = jugador
                return
        # Verificar diagonales
        if all(self.tableros[i][i].ganador == jugador for i in range(3)):
            self.ganador = jugador
            return
        if all(self.tableros[i][2 - i].ganador == jugador for i in range(3)):
            self.ganador = jugador
            return

    def mostrar(self):
        """Muestra el tablero grande y sus tableros pequeños con colores."""
        for fila in self.tableros:
            for i in range(3):  # Filas de los tableros pequeños
                print(" || ".join(
                    " | ".join(
                        Fore.RED + celda + Style.RESET_ALL if celda == "X" else
                        Fore.BLUE + celda + Style.RESET_ALL if celda == "O" else
                        " " for celda in tablero.tablero[i]
                    ) for tablero in fila
                ))
                if i < 2:
                    print("-" * 36)
            print("=" * 36)

    def tablero_disponible(self, fila, columna):
        """
        Devuelve True si el tablero pequeño en (fila, columna) está disponible para jugar.
        """
        return not self.tableros[fila][columna].esta_lleno()


# Clase principal que controla el flujo del juego
class Juego:
    def __init__(self):
        # Inicializamos el tablero grande y configuramos el primer jugador
        self.tablero_grande = TableroGrande()
        self.jugador_actual = "X"  # El jugador que comienza
        self.tablero_restringido = None  # Tablero grande restringido donde debe jugar
        self.juego_terminado = False

    def turno(self):
        """
        Gestiona el flujo de un turno: muestra el estado actual, solicita un movimiento
        y actualiza el juego según las reglas.
        """
        print(f"Turno del jugador {self.jugador_actual}")
        self.tablero_grande.mostrar()

        # Si el tablero restringido no está disponible, se permite elegir cualquier tablero
        if self.tablero_restringido and not self.tablero_grande.tablero_disponible(*self.tablero_restringido):
            print("El tablero restringido está lleno o ganado. Puedes elegir cualquier tablero disponible.")
            self.tablero_restringido = None

        # Determinar dónde el jugador puede jugar
        if self.tablero_restringido:
            tablero_fila, tablero_columna = self.tablero_restringido
            print(f"Debes jugar en el tablero grande ({tablero_fila + 1}, {tablero_columna + 1})")
        else:
            print("Puedes elegir cualquier tablero grande.")

        # Solicitar al jugador que seleccione su movimiento
        while True:
            try:
                if not self.tablero_restringido:
                    # Permitir al jugador seleccionar libremente un tablero grande
                    tablero_fila = int(input("Selecciona la fila del tablero grande (1-3): ")) - 1
                    tablero_columna = int(input("Selecciona la columna del tablero grande (1-3): ")) - 1
                    if not self.tablero_grande.tablero_disponible(tablero_fila, tablero_columna):
                        print("Ese tablero no está disponible. Intenta con otro.")
                        continue
                else:
                    tablero_fila, tablero_columna = self.tablero_restringido

                # Seleccionar casilla dentro del tablero pequeño
                casilla_fila = int(input("Selecciona la fila del tablero pequeño (1-3): ")) - 1
                casilla_columna = int(input("Selecciona la columna del tablero pequeño (1-3): ")) - 1

                # Intentar colocar la ficha
                if self.tablero_grande.colocar_ficha(
                    self.jugador_actual, tablero_fila, tablero_columna, casilla_fila, casilla_columna
                ):
                    # Actualizar restricción para el siguiente turno
                    self.tablero_restringido = (casilla_fila, casilla_columna)
                    # Verificar si el juego ha terminado
                    if self.tablero_grande.ganador:
                        print(f"¡El jugador {self.jugador_actual} ha ganado el juego!")
                        self.juego_terminado = True
                    elif all(tablero.esta_lleno() for fila in self.tablero_grande.tableros for tablero in fila):
                        print("¡Empate! Todos los tableros están llenos.")
                        self.juego_terminado = True
                    break
                else:
                    print("Movimiento inválido. Inténtalo de nuevo.")
            except (ValueError, IndexError):
                print("Entrada inválida. Por favor, ingresa valores entre 1 y 3.")

        # Cambiar de jugador si el juego no ha terminado
        if not self.juego_terminado:
            self.jugador_actual = "O" if self.jugador_actual == "X" else "X"

    def jugar(self):
        """
        Inicia el ciclo del juego, alternando turnos hasta que haya un ganador o empate.
        """
        print("¡Bienvenido al Tres en Raya Avanzado!")
        while not self.juego_terminado:
            self.turno()
        print("¡Gracias por jugar!")


# Punto de entrada del juego
if __name__ == "__main__":
    juego = Juego()  # Crear una instancia del juego
    juego.jugar()  # Iniciar el juego
