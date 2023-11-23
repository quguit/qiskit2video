from manim import *
import numpy as np

class RotatingVector(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        radius = 3
        axis_lengths = (radius * 3)  # Set axis lengths to be twice the radius

        # Position the axes relative to the center of the sphere
        axes = ThreeDAxes(
            x_length=axis_lengths * 0.9,
            y_length=axis_lengths * 1.0,
            z_length=axis_lengths * 0.8,
            tips=False
        )
        sphere = Sphere(
            center=(0, 0, 0),  # Posição da esfera
            radius=radius,
            resolution=(12, 10),
        )
        sphere.set_fill(BLUE_D, 0.1)
        sphere.set_stroke(width=1)
        self.add(axes, sphere)

        radius = 3
        initial_theta = 0
        initial_phi = 0

        num_passos = 5
        delta_theta = num_passos * DEGREES
        delta_phi = num_passos * DEGREES

        arrows = VGroup()
        rotating_vector = Arrow3D(start=np.array([0, 0, 0]), end=np.array([0, 0, 0]), color=BLUE)

        for i in range(18):
            # Atualiza o vetor com as novas coordenadas
            x = radius * np.sin(initial_theta) * np.cos(initial_phi)
            y = radius * np.sin(initial_theta) * np.sin(initial_phi)
            z = radius * np.cos(initial_theta)

            # Cria um novo vetor
            new_arrow = Arrow3D(start=np.array([0, 0, 0]), end=np.array([x, y, z]), color=GREEN)

            # Adiciona o novo vetor ao grupo
            arrows.add(new_arrow)

            # Atualiza o vetor existente
            rotating_vector.become(new_arrow)

            # Atualiza os ângulos
            initial_theta += delta_theta
            # Condição para inverter o sentido de theta
            if i < 9:
                initial_theta -= 2 * delta_theta
            initial_phi += delta_phi

            # Adiciona a trajetória à medida que o vetor se move
            if i > 0:
                prev_x, prev_y, prev_z = arrows[-2].get_end()
                line = Line([prev_x, prev_y, prev_z], [x, y, z], color=RED)
                self.add(line)

            # Rotação do vetor
            rotating_vector.rotate(angle=0.1, axis=OUT)
            self.add(rotating_vector)

        # Animação de transição suave
        self.play(
            *[
                Transform(arrows[i], arrows[i + 1])
                for i in range(len(arrows) - 1)
            ],
            run_time=3
        )

        self.wait(1) 


