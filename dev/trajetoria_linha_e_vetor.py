
from manim import *
import numpy as np

class ThreeDVector(ThreeDScene):
    def construct(self):
        r = 3
        initial_theta = 0
        final_theta = np.pi
        initial_phi = 0
        final_phi = np.pi/2

        num_passos = 128
        delta_theta = (final_theta - initial_theta) / num_passos
        delta_phi = (final_phi - initial_phi) / num_passos

        vector_points = []
        for i in range(num_passos):
            theta = initial_theta + i * delta_theta
            phi = initial_phi + i * delta_phi
            x = r * np.sin(theta) * np.cos(phi)
            y = r * np.sin(theta) * np.sin(phi)
            z = r * np.cos(theta)

            if i > 0:
                prev_x, prev_y, prev_z = vector_points[-1]
                line = Line([prev_x, prev_y, prev_z], [x, y, z], color=RED)
                self.add(line)

            vector_points.append((x, y, z))
            self.play(Create(Vector([x, y, z], color=GREEN).shift(ORIGIN)))
            

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
# To test the scene
class Test(Scene):
    def construct(self):
        self.play(Create(ThreeDVector()))
