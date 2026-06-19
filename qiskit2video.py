"""
qiskit2video — v1.0 (corrigida e atualizada)

Visualiza a evolução de um circuito quântico de 1 qubit na esfera de Bloch
usando Manim, com o statevector obtido via Qiskit Aer.

ESCOPO DESTA VERSÃO: 1 qubit apenas — igual ao escopo original da v1.0.
Suporte a múltiplos qubits (traço parcial para estados reduzidos,
interpolação geométrica genérica) é trabalho planejado para a v2, que será
modularizada em pacotes separados.
"""

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.visualization import circuit_drawer
from qiskit_aer import AerSimulator
from manim import *
import numpy as np
import tempfile
import os
import uuid

# Origem global da esfera de Bloch (válido para o caso de 1 qubit / 1 esfera)
origin = np.array([0, -4, -2])


def create_arrow(x, y, z):
    """Cria a seta 3D que representa o estado do qubit na esfera de Bloch."""
    end = np.array([2 * x, (2 * y) - 4, (2 * z) - 2])
    return Arrow3D(start=origin, end=end, resolution=8, color=BLUE)


def create_sphere(radius, position):
    """Cria a esfera de Bloch."""
    sphere = Sphere(center=position, radius=radius, resolution=(12, 10))
    sphere.set_fill(WHITE, 0.01)
    sphere.set_stroke(WHITE, width=1)
    return sphere


def create_axes(radius, position):
    """Cria os eixos 3D de referência da esfera de Bloch."""
    axis_lengths = radius * 3
    axes = ThreeDAxes(
        x_length=axis_lengths * 0.9,
        y_length=axis_lengths * 1.0,
        z_length=axis_lengths * 0.8,
        tips=False,
    )
    axes.move_to(position)
    return axes


def calculate_sphere_positions(num_qubits):
    """Calcula a posição de cada esfera de Bloch, uma ao lado da outra."""
    return [(i * 3, -4, -2) for i in range(num_qubits)]


def rect2pol(alpha, beta):
    """
    Converte as amplitudes (alpha, beta) para coordenadas polares (theta, phi).

    ATENÇÃO: válido apenas para 1 qubit. `alpha`/`beta` aqui são as duas
    amplitudes inteiras do statevector do sistema — isso só representa
    corretamente o estado de UM qubit. Para múltiplos qubits seria
    necessário extrair o estado reduzido via traço parcial (trabalho da v2).
    """
    r = np.sqrt(abs(alpha) ** 2 + abs(beta) ** 2)
    theta = 2 * np.arccos(alpha.real / r)
    phi = np.angle(beta)
    if phi < 0:
        phi += 2 * np.pi
    return theta, phi


def simulator(circuit):
    """
    Executa o circuito no AerSimulator (modo statevector) e devolve a
    posição cartesiana [x, y, z] do estado na esfera de Bloch.
    """
    backend = AerSimulator(method="statevector")

    circ = circuit.copy()
    circ.save_statevector()

    transpiled = transpile(circ, backend)
    result = backend.run(transpiled).result()
    vector = result.get_statevector(transpiled)

    theta, phi = rect2pol(vector[0], vector[1])

    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return [x, y, z]


def generate_circuit_image(circuit):
    """Gera a imagem do circuito no estado atual como ImageMobject do Manim."""
    temp_dir = tempfile.gettempdir()
    # Nome único por chamada — evita colisão/sobrescrita entre os passos do circuito
    image_path = os.path.join(temp_dir, f"quantum_circuit_{uuid.uuid4().hex}.png")
    circuit_drawer(circuit, output="mpl", filename=image_path)

    circuit_image = ImageMobject(image_path)
    circuit_image.scale(1.2)
    circuit_image.to_corner(UL)
    return circuit_image


class BlochSphereScene(ThreeDScene):
    """
    Cena Manim responsável pela animação inteira. Recebe os dados já
    calculados (statevectors, imagens do circuito, nomes dos gates) e monta
    tudo dentro de `construct()` — como a API do Manim espera. `render()` é
    chamado uma única vez, de fora, depois de instanciar a cena.
    """

    def __init__(self, sv, album, gates, num_qubits, speed, frames, **kwargs):
        self.sv = sv
        self.album = album
        self.gates = gates
        self.num_qubits = num_qubits
        self.speed = speed
        self.frames = frames
        super().__init__(**kwargs)

    def construct(self):
        radius = 2
        sphere_positions = calculate_sphere_positions(self.num_qubits)

        spheres = [create_sphere(radius, p) for p in sphere_positions]
        axes_list = [create_axes(radius, p) for p in sphere_positions]

        ket0 = axes_list[0].get_z_axis_label(Tex(r"$| 0 \rangle$")).rotate(0, axis=LEFT).next_to(axes_list[0].z_axis, 1.0)
        ket1 = axes_list[0].get_z_axis_label(Tex(r"$| 1 \rangle$")).next_to(axes_list[0].z_axis, -2.0).rotate(135, OUT)
        ketX = axes_list[0].get_x_axis_label(Tex(r"$| + \rangle$")).next_to(axes_list[0].x_axis, 2.5).rotate(-10, axis=RIGHT)

        self.add(*axes_list, *spheres, ket0, ket1, ketX)
        self.set_camera_orientation(theta=135 * DEGREES, phi=60 * DEGREES, gamma=0 * DEGREES)

        if self.num_qubits > 1:
            print(
                "AVISO: suporte a múltiplos qubits ainda não é fisicamente "
                "correto nesta versão (sem traço parcial). Use 1 qubit até a v2."
            )

        for q in range(self.num_qubits):
            self._animate_qubit_trajectory(q)

        self.wait(1)

    def _animate_qubit_trajectory(self, q):
        arrows = [create_arrow(*position) for position in self.sv[q]]
        gates_q = self.gates[q]

        current_arrow = arrows[0]
        current_image = self.album[q][0]

        self.add(current_arrow)
        self.add_fixed_in_frame_mobjects(current_image)
        self.add(current_image)
        self.wait(1)

        vector_points = [current_arrow.get_end()]

        for i in range(len(arrows) - 1):
            pos_i = np.array(self.sv[q][i])
            pos_f = np.array(self.sv[q][i + 1])

            r = np.linalg.norm(pos_i) or 1.0

            phi_i = np.rad2deg(np.arctan2(pos_i[1], pos_i[0]))
            theta_i = np.rad2deg(np.arccos(pos_i[2] / np.linalg.norm(pos_i)))
            phi_f = np.rad2deg(np.arctan2(pos_f[1], pos_f[0]))
            theta_f = np.rad2deg(np.arccos(pos_f[2] / np.linalg.norm(pos_f)))

            gate = gates_q[i]

            # Correções específicas por gate, herdadas da v1.0 original.
            # Generalização (SLERP genérico) fica para a v2.
            if gate == "h":
                if theta_i == 0:
                    phi_i = -90
                elif theta_i == 90:
                    if phi_i == 180:
                        phi_i, phi_f = -180, -90
                    else:
                        phi_f = 90
                elif theta_i == 180:
                    phi_i = 90
            elif gate == "z":
                theta_i = theta_f = 90
            elif gate == "x":
                if theta_i == 0:
                    phi_i = phi_f = -90
                elif theta_i == 180:
                    phi_i = phi_f = 90
                    theta_f = 0
            elif gate == "s":
                phi_i = phi_f = 90

            for j in range(self.frames + 1):
                alpha = j / self.frames
                theta = (1 - alpha) * theta_i + alpha * theta_f
                phi = (1 - alpha) * phi_i + alpha * phi_f

                if gate == "y":
                    if theta < 180:
                        phi_f = 0
                    else:
                        phi_f = 180
                        theta_f = 90

                x_alpha = r * np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi))
                y_alpha = r * np.sin(np.deg2rad(theta)) * np.sin(np.deg2rad(phi))
                z_alpha = r * np.cos(np.deg2rad(theta))

                x = x_alpha * 2
                y = (y_alpha * 2) - 4
                z = (z_alpha * 2) - 2

                if j > 0:
                    prev_x, prev_y, prev_z = vector_points[-1]
                    self.add(Line([prev_x, prev_y, prev_z], [x, y, z], color=RED))
                vector_points.append((x, y, z))

                intermediate_arrow = Arrow3D(start=origin, end=np.array([x, y, z]), color=BLUE)
                self.play(Transform(current_arrow, intermediate_arrow), run_time=(1 / self.speed))

            # Atualiza a imagem do circuito para o próximo passo
            self.remove(current_image)
            current_image = self.album[q][i + 1]
            self.add_fixed_in_frame_mobjects(current_image)
            self.add(current_image)


class TrackedQuantumCircuit(QuantumCircuit):
    """
    Subclasse de QuantumCircuit que rastreia o statevector e a imagem do
    circuito a cada gate aplicado, permitindo gerar a animação depois.

    Renomeada de `QuantumCircuit` (nome usado na v1.0 original) só
    internamente, para não sombrear a classe base do Qiskit dentro do
    próprio módulo. O alias no final do arquivo mantém a API pública
    idêntica à v1.0 (`from qiskit2video import *` continua expondo
    `QuantumCircuit` como a classe rastreada).
    """

    def __init__(self, qreg_q, *args, **kwargs):
        super().__init__(qreg_q, *args, **kwargs)

        self.sv = [[] for _ in range(self.num_qubits)]
        self.album = [[] for _ in range(self.num_qubits)]
        self.gates = [[] for _ in range(self.num_qubits)]

        for i in range(self.num_qubits):
            self.sv[i].append(simulator(self))
            self.album[i].append(generate_circuit_image(self))

    def video(self, speed=15, frames=30):
        """Gera a animação da evolução do(s) qubit(s) na esfera de Bloch."""
        scene = BlochSphereScene(
            sv=self.sv,
            album=self.album,
            gates=self.gates,
            num_qubits=self.num_qubits,
            speed=speed,
            frames=frames,
        )
        scene.render()

    def _track(self, qubit_index):
        self.sv[qubit_index].append(simulator(self))
        self.album[qubit_index].append(generate_circuit_image(self))

    def h(self, qubit):
        super().h(qubit)
        i = qubit.index if hasattr(qubit, "index") else qubit
        self.gates[i].append("h")
        self._track(i)

    def x(self, qubit):
        super().x(qubit)
        i = qubit.index if hasattr(qubit, "index") else qubit
        self.gates[i].append("x")
        self._track(i)

    def y(self, qubit):
        super().y(qubit)
        i = qubit.index if hasattr(qubit, "index") else qubit
        self.gates[i].append("y")
        self._track(i)

    def z(self, qubit):
        super().z(qubit)
        i = qubit.index if hasattr(qubit, "index") else qubit
        self.gates[i].append("z")
        self._track(i)

    def s(self, qubit):
        super().s(qubit)
        i = qubit.index if hasattr(qubit, "index") else qubit
        self.gates[i].append("s")
        self._track(i)

    def t(self, qubit):
        super().t(qubit)
        i = qubit.index if hasattr(qubit, "index") else qubit
        self.gates[i].append("t")
        self._track(i)

    def u(self, theta1, theta2, theta3, qubit):
        super().u(theta1, theta2, theta3, qubit)
        i = qubit.index if hasattr(qubit, "index") else qubit
        self.gates[i].append("u")
        self._track(i)


# Alias mantido por compatibilidade com a API pública da v1.0 original.
QuantumCircuit = TrackedQuantumCircuit
