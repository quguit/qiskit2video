from manim import *

class ThreeDSpace(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.add(axes)

        # Definindo setas de exemplo
        arrow_start = Arrow3D(start=np.array([0, 0, 0]), end=np.array([0, 0, 3]), color=BLUE)
        arrow_end = Arrow3D(start=np.array([0, 0, 0]), end=np.array([0, 0, -3]), color=RED)

        self.add(arrow_start)

        frames = 30
        speedup_factor = 10  # Fator de aceleração

        for i in range(frames):
            alpha = i / frames

            x_alpha = (1 - alpha) * arrow_start.get_end()[0] + alpha * arrow_end.get_end()[0]
            y_alpha = (1 - alpha) * arrow_start.get_end()[1] + alpha * arrow_end.get_end()[1]
            z_alpha = (1 - alpha) * arrow_start.get_end()[2] + alpha * arrow_end.get_end()[2]

            intermediate_arrow = Arrow3D(start=np.array([0, 0, 0]), end=np.array([x_alpha, y_alpha, z_alpha]), color=GREEN)

            arrow_start.become(intermediate_arrow)

            self.play(Transform(arrow_start, intermediate_arrow), run_time=1 / speedup_factor)

        self.wait(1)
