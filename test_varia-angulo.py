# import numpy as np
#
# # Definindo as coordenadas esféricas iniciais e finais
# r = 5
# initial_theta = 0  # Ângulo polar inicial em radianos
# final_theta = np.pi   # Ângulo polar final em radianos
# initial_phi = 0  # Ângulo azimutal inicial em radianos
# final_phi = np.pi/2  # Ângulo azimutal final em radianos
#
# # Definindo numero de passos
# num_passos = 128
#
# # Calculando o passo de variação para theta e phi
# delta_theta = (final_theta - initial_theta) / num_passos
# delta_phi = (final_phi - initial_phi) / num_passos
#
# # Iterando sobre os passos e realizando cálculos
# for i in range(num_passos):
#     theta = initial_theta + i * delta_theta
#     phi = initial_phi + i * delta_phi
#     x = r * np.sin(theta) * np.cos(phi)
#     y = r * np.sin(theta) * np.sin(phi)
#     z = r * np.cos(theta)
#     print(f'Para o passo {i}:')
#     print(f'Coordenadas esféricas: r = {r}, theta = {theta}, phi = {phi}')
#     print(f'Coordenadas cartesianas: x = {x}, y = {y}, z = {z}')
#     print('-------------------------------------------')
# from manim import *
# import numpy as np
#
# class ThreeDVector(ThreeDScene):
#     def construct(self):
#         r = 3
#         initial_theta = 0
#         final_theta = np.pi
#         initial_phi = 0
#         final_phi = np.pi/2
#
#         num_passos = 10
#         delta_theta = (final_theta - initial_theta) / num_passos
#         delta_phi = (final_phi - initial_phi) / num_passos
#
#         for i in range(num_passos):
#             theta = initial_theta + i * delta_theta
#             phi = initial_phi + i * delta_phi
#             x = r * np.sin(theta) * np.cos(phi)
#             y = r * np.sin(theta) * np.sin(phi)
#             z = r * np.cos(theta)
#
#             self.add(Vector([x, y, z], color=GREEN).shift(ORIGIN))
#
#         self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
#         axes = ThreeDAxes()
#         # self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
#         self.add(axes)
#
# # To test the scene
# class Test(Scene):
#     def construct(self):
#         self.play(Create(ThreeDVector()))

# from manim import *
# import numpy as np
#
# class ThreeDVector(ThreeDScene):
#     def construct(self):
#         r = 3
#         initial_theta = 0
#         final_theta = np.pi
#         initial_phi = 0
#         final_phi = np.pi/2
#
#         num_passos = 128
#         delta_theta = (final_theta - initial_theta) / num_passos
#         delta_phi = (final_phi - initial_phi) / num_passos
#
#         vector_points = []
#         for i in range(num_passos):
#             theta = initial_theta + i * delta_theta
#             phi = initial_phi + i * delta_phi
#             x = r * np.sin(theta) * np.cos(phi)
#             y = r * np.sin(theta) * np.sin(phi)
#             z = r * np.cos(theta)
#
#             if i > 0:
#                 prev_x, prev_y, prev_z = vector_points[-1]
#                 line = Line([prev_x, prev_y, prev_z], [x, y, z], color=RED)
#                 self.add(line)
#
#             vector_points.append((x, y, z))
#             self.add(Vector([x, y, z], color=GREEN).shift(ORIGIN))
#
#         self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
#
# # To test the scene
# class Test(Scene):
#     def construct(self):
#         self.play(Create(ThreeDVector()))

# from manim import *
# import numpy as np
#
# class ThreeDVector(ThreeDScene):
#     def construct(self):
#         r = 3
#         initial_theta = 0
#         final_theta = np.pi
#         initial_phi = 0
#         final_phi = np.pi/2
#
#         num_passos = 128
#         delta_theta = (final_theta - initial_theta) / num_passos
#         delta_phi = (final_phi - initial_phi) / num_passos
#
#         vector_points = []
#         lines = VGroup()
#         vectors = VGroup()
#
#         for i in range(num_passos):
#             theta = initial_theta + i * delta_theta
#             phi = initial_phi + i * delta_phi
#             x = r * np.sin(theta) * np.cos(phi)
#             y = r * np.sin(theta) * np.sin(phi)
#             z = r * np.cos(theta)
#
#             if i > 0:
#                 prev_x, prev_y, prev_z = vector_points[-1]
#                 line = Line([prev_x, prev_y, prev_z], [x, y, z], color=RED)
#                 lines.add(line)
#
#             vector_points.append((x, y, z))
#             vector = Vector([x, y, z], color=GREEN).shift(ORIGIN)
#             vectors.add(vector)
#
#         self.add(vectors)
#         self.play(Create(lines))
#         self.wait(1)
#
#         self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
#
# # To test the scene
# class Test(Scene):
#     def construct(self):
#         self.play(ThreeDVector())
#

from manim import *
import numpy as np

class RotatingVector(ThreeDScene):
    def construct(self):
        r = 3
        initial_theta = 0
        final_theta = np.pi
        initial_phi = 0
        final_phi = np.pi/2

        num_passos = 10
        delta_theta = (final_theta - initial_theta) / num_passos
        delta_phi = (final_phi - initial_phi) / num_passos

        vector_points = []
        lines = VGroup()
        vectors = VGroup()

        rotating_vectors = VGroup()
        rotating_lines = VGroup()

        for i in range(num_passos):
            theta = initial_theta + i * delta_theta
            phi = initial_phi + i * delta_phi
            x = r * np.sin(theta) * np.cos(phi)
            y = r * np.sin(theta) * np.sin(phi)
            z = r * np.cos(theta)

            if i > 0:
                prev_x, prev_y, prev_z = vector_points[-1]
                line = Line([prev_x, prev_y, prev_z], [x, y, z], color=RED)
                lines.add(line)

            vector_points.append((x, y, z))
            vector = Vector([x, y, z], color=GREEN).shift(ORIGIN)
            vectors.add(vector)

            rotating_vector = Vector([x, y, z], color=BLUE).shift(ORIGIN)
            rotating_vectors.add(rotating_vector)

            rotating_vector.rotate(angle=0.1, axis=OUT)
            prev_x, prev_y, prev_z = vector_points[-1]
            rotating_line = Line([prev_x, prev_y, prev_z], [rotating_vector.get_end()[0], rotating_vector.get_end()[1], rotating_vector.get_end()[2]], color=ORANGE)
            rotating_lines.add(rotating_line)

        self.add(vectors)
        self.play(Create(lines))
        self.wait(1)
        self.add(rotating_vectors)
        self.play(Create(rotating_lines))
        self.wait(1)

        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

# To test the scene
class Test(Scene):
    def construct(self):
        self.play(RotatingVector())
