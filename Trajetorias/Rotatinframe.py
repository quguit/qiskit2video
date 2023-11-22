from manim import *


class gateH(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        # Configuração da esfera de Bloch
        sphere = Sphere(center=ORIGIN,
            radius=2,
            resolution=(15,4)
        )
        sphere.set_fill(BLUE, 0.1)
        sphere.set_stroke(width=1)

        # Adiciona a esfera de Bloch à cena
        self.add(sphere)

        # Vetor inicial no estado |0⟩
        initial_state = np.array([0, 0, 2])

        arrow = Arrow3D(ORIGIN, initial_state, color=RED)

        # Adiciona a seta inicial à cena
        self.add(arrow)



        # Adiciona os eixos sem setas
        axes = ThreeDAxes(tips=False
                          )
        axes.x_axis.remove(axes.x_axis[1])
        axes.y_axis.remove(axes.y_axis[1])
        self.add(axes)

        # Atualiza a seta final
        final_state = np.array([2, 0, 0])
        arrow_target = Arrow3D(ORIGIN, final_state, color=RED)

        # Adiciona rótulos para os quadros
        lab_frame_label = Text("Laboratory Frame", font_size=18).to_edge(UP)

        # Adiciona a seta final à cena e remove a seta inicial
        self.play(ReplacementTransform(arrow, arrow_target))
        # Animação da rotação
        self.play(
            Rotate(arrow, angle=2 * np.pi, axis=OUT, run_time=2),
            Rotate(axes, angle=2 * np.pi, axis=OUT, run_time=2),
            Rotate(sphere, angle=2 * np.pi, axis=OUT, run_time=2),
            Write(lab_frame_label)
        )

        self.wait(1)

