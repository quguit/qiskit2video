from manim import *

class BlochSphereRotation(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        # Configuração da esfera de Bloch
        bloch_sphere = Sphere(
            radius=2,
            center=ORIGIN,
            resolution=(10, 5)  # Ajuste a resolução conforme necessário
        )
        bloch_sphere.set_fill(BLUE_E, 0.1)
        bloch_sphere.set_stroke(width=1)

        # Adiciona a esfera de Bloch à cena
        self.add(bloch_sphere)

        # Vetor inicial no estado |0⟩
        initial_state = np.array([0, 0, 2])
        arrow = Arrow3D(ORIGIN, initial_state, color=RED)

        # Adiciona a seta inicial à cena
        self.add(arrow)

        # Adiciona rótulos para os quadros
        lab_frame_label = Text("Laboratory Frame", font_size=18).to_edge(UP)

        # Rotação no "laboratory frame"
        self.play(Rotate(arrow, angle=2 * np.pi, axis=OUT, run_time=2), Write(lab_frame_label))

        self.wait(1)
