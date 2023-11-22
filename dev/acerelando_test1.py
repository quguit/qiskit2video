from manim import *

class ThreeDSpace(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.add(axes)

        # Definindo setas de exemplo
        arrow_start = Arrow3D(start=np.array([0, 0, 0]), end=np.array([0, 0, 3]), color=BLUE)
        arrow_end = Arrow3D(start=np.array([0, 0, 0]), end=np.array([np.cos(-90), np.sin(-90), 0]), color=RED)

        self.add(arrow_start)

        frames = 30
        speedup_factor = 10  # Fator de aceleração

        for i in range(frames):
            alpha = i / frames

            start_vec = arrow_start.get_end()
            end_vec = arrow_end.get_end()

            r = np.linalg.norm(start_vec)  # Raio constante

            start_theta = np.arctan2(start_vec[1], start_vec[0])
            start_phi = np.arccos(start_vec[2] / r)

            end_theta = np.arctan2(end_vec[1], end_vec[0])
            end_phi = np.arccos(end_vec[2] / r)

            theta = (1 - alpha) * start_theta + alpha * end_theta
            phi = (1 - alpha) * start_phi + alpha * end_phi

            x_alpha = r * np.sin(phi) * np.cos(theta)
            y_alpha = r * np.sin(phi) * np.sin(theta)
            z_alpha = r * np.cos(phi)

            intermediate_arrow = Arrow3D(start=np.array([0, 0, 0]), end=np.array([x_alpha, y_alpha, z_alpha]), color=GREEN)

            arrow_start.become(intermediate_arrow)

            self.play(Transform(arrow_start, intermediate_arrow), run_time=1 / speedup_factor)

        self.wait(1)

