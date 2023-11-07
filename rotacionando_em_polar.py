from manim import *
import numpy as np

class ThreeDSpace(ThreeDScene):
    def construct(self):
        # Definindo o vetor no espaço 3D
        vetor_cartesiano = np.array([3, 4, 0])

        # Calculando o módulo
        r = np.linalg.norm(vetor_cartesiano)

        # Calculando o ângulo theta em relação ao eixo z
        theta = np.arccos(vetor_cartesiano[2] / r)

        # Calculando o ângulo phi em relação ao plano x-y
        phi = np.arctan2(vetor_cartesiano[1], vetor_cartesiano[0])

        # Criando o array com as coordenadas polares
        coordenadas_polares = np.array([r, (theta * 180 / np.pi) * DEGREES, (phi * 180 / np.pi) * DEGREES])

        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.add(axes)

        # Definindo setas de exemplo
        arrow_start = Arrow3D(start=np.array([0, 0, 0]), end=coordenadas_polares, color=BLUE)

        self.add(arrow_start)
        # Imprimindo as coordenadas polares no formato desejado
        print(coordenadas_polares)

# Executando a animação
ThreeDSpace().render()
