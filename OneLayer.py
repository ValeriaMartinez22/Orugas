class JugadorOrugasOneLayer(JugadorOrugas):
    '''Jugador de Orugas que tira de manera aleatoria.'''

    def adyacencias(self, coordenadas):
        r = coordenadas[0]
        c = coordenadas[1]

        arriba = (r+1,c)
        abajo = (r-1,c)
        izquierda = (r,c-1)
        derecha = (r,c+1)
        

        renglones = self.juego.renglones
        columnas = self.juego.columnas

        if r + 1 > renglones - 1:
            arriba = (0, c)
        if r - 1 < 0:
            abajo = (renglones - 1, c)
        if c - 1 < 0:
            izquierda = (r, columnas - 1)
        if c + 1 > columnas - 1:
            derecha = (r, 0)
        
        vecinos = [arriba,abajo,izquierda,derecha]
        return vecinos

    def sumatoriaAdyacenciasVacias(self, coordenadas, tablero):
        sumatoria = 0
        for value in coordenadas:
            r = value[0]
            c = value[1]
            if tablero[r][c] == ' ':
                sumatoria += 10
        return sumatoria

    def heuristica(self, posicion):

        if self.triunfo(posicion) == self.simbolo:
            return 1000

        posibles = self.posiciones_siguientes(posicion)
        contrario = self.contrario.simbolo

        for p in posibles:
            if self.triunfo(p) == contrario:
                return -1000

        puntaje = 0
        tablero = posicion[1]
        miJugador = self.simbolo
        renglones = self.juego.renglones
        columnas = self.juego.columnas

        for r in range(renglones):
            for c in range(columnas):
                if tablero[r][c] == miJugador:
                    misCoor = (r,c)
                elif tablero[r][c] == contrario:
                    contrarioCoor = (r,c)

        misAdyacencias = self.adyacencias(misCoor)
        miSumatoria = self.sumatoriaAdyacenciasVacias(misAdyacencias, tablero)

        contrarioAdyacencias = self.adyacencias(contrarioCoor)
        contrarioSumatoria = self.sumatoriaAdyacenciasVacias(contrarioAdyacencias, tablero)

        puntaje = miSumatoria - contrarioSumatoria

        return puntaje


    def tira(self, posicion):
        posibles = self.posiciones_siguientes(posicion)
        best_move = posibles[0]
        best_evaluation = self.heuristica(best_move)

        for move in posibles[1:]:
            result = self.heuristica(move)
            if result > best_evaluation:
                best_evaluation = result
                best_move = move
        return best_move
