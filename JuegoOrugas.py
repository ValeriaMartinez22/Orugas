from dagor import JuegoOrugas, JugadorOrugasAleatorio, JugadorOrugasInteractivo
from equipo7 import JugadorOrugasEquipo7

if __name__ == '__main__':
    juego = JuegoOrugas(
        JugadorOrugasEquipo7('Equipo7'),
        JugadorOrugasAleatorio('RandomBoy'),
        4, 4)

    juego.inicia(veces=100, delta_max=2)
