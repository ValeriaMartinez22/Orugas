# ----------------------------------------------------------
#  Project: Adversarial Caterpillars
#
#  Date: 01-Dic-2022
#  Authors:
#            A01752167 Valeria Martínez Silva
#            A01751272 Aleny Sofía Arévalo Magdaleno
# ----------------------------------------------------------
from dagor import *
from random import choice, randint


class JugadorOrugasEquipo7(JugadorOrugas):

    def __init__(self, nombre):
        super().__init__(nombre)
        self.tiros: int = 0
        self.tipo_opuestos: int = 0

    def find_best_move(self, posicion, max_depth: int = 10) -> float:
        best_eval: float = float("-inf")
        best_move = -1
        for move in self.posiciones_siguientes(posicion):
            result: float = self.alphabeta(move, False, max_depth)
            if result > best_eval:
                best_eval = result
                best_move = move
        self.tiros += 1
        return best_move

    def alphabeta(self, posicion, maximizing: bool, max_depth: int = 10,
                  alpha: float = float("-inf"),
                  beta: float = float("inf")) -> float:
        if self.triunfo(posicion) or max_depth == 0:
            return self.heuristica(posicion)

        if maximizing:
            for move in self.posiciones_siguientes(posicion):
                result = self.alphabeta(move, False,
                                        max_depth - 1,
                                        alpha, beta)
                alpha = max(result, alpha)
                if beta <= alpha:
                    break
            return alpha
        else:  # minimizing
            for move in self.posiciones_siguientes(posicion):
                result = self.alphabeta(move, True, max_depth - 1,
                                        alpha, beta)
                beta = min(result, beta)
                if beta <= alpha:
                    break
            return beta

    def heuristica(self, posicion):

        def pos_actual(sym):
            for r in range(rens):
                for c in range(cols):
                    if tablero[r][c] == sym:
                        return r, c

        # #####################################################################
        # ############## E S T R A T E G I A  O P U E S T O S #################

        def opuestos_iniciales() -> bool:
            r, c = pos_inicial(simbolo)
            if tablero_inicial[rens - 1 - r][cols - 1 - c] == contrario:
                self.tipo_opuestos = 1
                return True
            elif tablero_inicial[rens - 1 - r][c] == contrario:
                self.tipo_opuestos = 2
                return True
            elif tablero_inicial[r][cols - 1 - c] == contrario:
                self.tipo_opuestos = 3
                return True
            return False

        def pos_inicial(sym):
            for r in range(rens):
                for c in range(cols):
                    if tablero_inicial[r][c] == sym:
                        return r, c

        def opuestos_1(r: int, c: int):
            if tablero[rens - 1 - r][cols - 1 - c] == contrario.lower():
                return True
            return False

        def opuestos_2(r: int, c: int):
            if tablero[rens - 1 - r][c] == contrario.lower():
                return True
            return False

        def opuestos_3(r: int, c: int):
            if tablero[r][cols - 1 - c] == contrario.lower():
                return True
            return False

        def camino_opuesto() -> bool:
            for r in range(rens):
                for c in range(cols):
                    if tablero[r][c] == simbolo.lower():
                        if self.tipo_opuestos == 1:
                            if not opuestos_1(r, c):
                                return False
                        elif self.tipo_opuestos == 2:
                            if not opuestos_2(r, c):
                                return False
                        elif self.tipo_opuestos == 3:
                            if not opuestos_3(r, c):
                                return False
            return True

        def cabeza_opuesta() -> bool:
            for r in range(rens):
                for c in range(cols):
                    if tablero[r][c] == simbolo:
                        if self.tipo_opuestos == 1:
                            if tablero[rens - 1 - r][cols - 1 - c] \
                               == contrario:
                                return True
                        elif self.tipo_opuestos == 2:
                            if tablero[rens - 1 - r][c] == contrario:
                                return True
                        elif self.tipo_opuestos == 3:
                            if tablero[r][cols - 1 - c] == contrario:
                                return True
            return False

        # #####################################################################
        # ################ E S T R A T E G I A  L I B R E S ###################

        def vecinos(r, c):
            arriba = (r - 1, c)
            abajo = (r + 1, c)
            der = (r, c + 1)
            izq = (r, c - 1)
            if r == 0:
                arriba = (rens - 1, c)
            if c == 0:
                izq = (r, cols - 1)
            if r == rens - 1:
                abajo = (0, c)
            if c == cols - 1:
                der = (r, 0)
            return (arriba, der, abajo, izq)

        simbolo = self.simbolo
        contrario = self.contrario.simbolo
        if self.triunfo(posicion) == simbolo:
            return 100000
        elif self.triunfo(posicion) == contrario:
            return - 100000

        puntaje = 0
        tablero = posicion[1]
        tablero_inicial = self.juego.posicion_inicial()[1]
        rens = self.juego.renglones
        cols = self.juego.columnas

        # Si eres segundo y aparecen en pos. opuestas, tirar opuestos
        if self.juego._num_tiro % 2 == 0 and opuestos_iniciales():
            if camino_opuesto() and cabeza_opuesta():
                puntaje += 50000

        # Moverse al lugar que te deje con más espacios posibles o
        # al contrario con menos espacios posibles
        else:
            rr, cc = pos_actual(simbolo)
            vecinos_s = vecinos(rr, cc)
            for vecino in vecinos_s:
                r, c = vecino
                if tablero[r][c] == ' ':
                    puntaje += 100

            rr, cc = pos_actual(contrario)
            vecinos_c = vecinos(rr, cc)
            for vecino in vecinos_c:
                r, c = vecino
                if tablero[r][c] == ' ':
                    puntaje -= 100

        return puntaje

    def tira(self, posicion):
        return self.find_best_move(posicion)


if __name__ == '__main__':
    jugador1 = JugadorOrugasEquipo7('Equipo7')
    jugador2 = JugadorOrugasAleatorio('Random')
    juego = JuegoOrugas(
        jugador1,
        jugador2,
        10, 10)
    for _ in range(10):
        juego.inicia(veces=100, delta_max=2)
