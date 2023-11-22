from qiskit.quantum_info import entropy
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute, BasicAer, transpile, assemble
from numpy import pi
from qiskit.visualization import circuit_drawer
from manim import *
import numpy as np
import tempfile, os


# Function to create a 3D arrow representing a quantum state
def create_arrow(x, y, z):
    origin = (0, -4, -2)
    end = np.array([2 * x, (2 * y) - 4, (2 * z) - 2])

    # Map the phase to a color according to qiskit conventions
    # color = None
    # if 0 <= phase < np.pi / 2:
    #     color = BLUE
    # elif phase < np.pi:
    #     color = PINK
    # elif phase < 3 * np.pi / 2:
    #     color = RED
    # else:
    #     color = ORANGE

    arrow = Arrow3D(
        start=origin,
        end=end,
        resolution=8,
        color=BLUE
    )

    return arrow


# Function to create a 3D sphere representing the Bloch sphere
def create_sphere(radius):
    sphere = Sphere(
        center=(0, -4, -2),  # Posição da esfera
        radius=radius,
        resolution=(12, 10),
    )
    sphere.set_fill(WHITE, 0.01)
    sphere.set_stroke(width=1)
    return sphere


# Function to create 3D axes for visualization
def create_axes(radius):
    # Calculate the lengths of the axes based on the sphere's radius

    axis_lengths = (radius*3)   # Set axis lengths to be twice the radius

    # Position the axes relative to the center of the sphere
    axes = ThreeDAxes(
        x_length=axis_lengths * 0.9,
        y_length=axis_lengths * 1.0,
        z_length=axis_lengths * 0.8,
        tips=False
    )

    axes.move_to((0, -4, -2))  # Move the axes to the desired position
    return axes


# Main scene class to visualize the Bloch sphere and quantum states
class BlochSphere(ThreeDScene):

    def construct(self):
        radius = 2
        # Position the sphere at the center of the space
        sphere = create_sphere(radius)

        axes = create_axes(radius)

        # Labels for quantum states
        ket0 = axes.get_z_axis_label(Tex(r"$| 0 \rangle$")).rotate(0, axis=LEFT).next_to(axes.z_axis, 1.0)
        ket1 = axes.get_z_axis_label(Tex(r"$| 1 \rangle$")).next_to(axes.z_axis, -2.0).rotate(135, Z_AXIS)
        ketX = axes.get_x_axis_label(Tex(r"$| + \rangle$")).next_to(axes.x_axis, 2.5).rotate(-10, axis=RIGHT)
        # ketY = axes.get_y_axis_label(Tex(r"$| - \rangle$")).next_to(axes.y_axis, 5).rotate(70, axis=UP)

        # Add objects (axes, sphere, labels) to the scene
        self.add(axes, sphere, ket0, ket1, ketX)

        # Configuração da câmera
        self.set_camera_orientation(phi=pi / 2.5, theta=pi / 4, zoom=1.1)

        # self.play(FadeIn(sphere))
        # self.wait(5)


def rect2pol(alpha, beta):
    # Calcular coordenadas polares
    r = np.sqrt(abs(alpha) ** 2 + abs(beta) ** 2)
    theta = 2 * np.arccos(alpha.real / r)
    phi = np.angle(beta)

    # Converter ângulo phi de [-π, π] para [0, 2π]
    if phi < 0:
        phi += 2 * np.pi
    return theta, phi


def simulator(circuit):
    backend = Aer.get_backend('statevector_simulator')
    job = execute(circuit, backend)
    result = job.result()
    # Representaçã odo vetor no espaço de hilbert de 2 dimenções
    vector = result.get_statevector(circuit)
    theta, phi = rect2pol(vector[0], vector[1])

    x = 1 * np.sin(theta) * np.cos(phi)
    y = 1 * np.sin(theta) * np.sin(phi)
    z = 1 * np.cos(theta)

    return [x, y, z]


def generate_circuit_image(circuit):
    # Gere a representação visual do circuito usando 'mpl' do Qiskit
    temp_dir = tempfile.gettempdir()  # Diretório temporário para salvar a imagem
    image_path = os.path.join(temp_dir, "quantum_circuit.png")
    circuit_drawer(circuit, output='mpl', filename=image_path)

    # Carregue a imagem gerada usando Manim
    circuit_image = ImageMobject(image_path)

    # Dimensione a imagem como desejado
    circuit_image.scale(1.2)

    # Posicione a imagem no canto superior esquerdo
    circuit_image.to_corner(UL)

    return circuit_image


# classe personalizada que herda de QuantumCircuit
class QuantumCircuit(QuantumCircuit):
    def __init__(self, qreg_q, *args, **kwargs):
        super().__init__(qreg_q, *args, **kwargs)
        self.sv = []  # lista de posições
        self.arrows = []  # lista de vetores criados Arrow3D
        self.sv.append(simulator(self))
        self.album = []
        self.album.append(generate_circuit_image(self))

    # método personalizado para a operação X
    def x(self, qubit, **kwargs):
        super().x(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))

    # método personalizado para a operação Pauli y
    def y(self, qubit):
        super().y(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))

    # método personalizado para a operação s
    def s(self, qubit):
        super().s(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))
        # self.add_entanglement(qubit)

    # método personalizado para a operação Pauli-z
    def z(self, qubit):
        super().z(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))
        # self.add_entanglement(qubit)

    # método personalizado para a operação t
    def t(self, qubit):
        super().t(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))

    # método personalizado para a operação H
    def h(self, qubit):
        super().h(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))
        # self.add_entanglement(self.calculate_entanglement(qubit))

    # método personalizado para a operação U
    def u(self, theta1, theta2, theta3, qubit):
        super().u(theta1, theta2, theta3, qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))
        # self.add_entanglement(self.calculate_entanglement(qubit))

    def video(self, speed):  # bideo, velocidade, exportação,
        # criando uma cena 3D
        bloch_sphere = BlochSphere()
        # executando o construtor
        bloch_sphere.construct()
        # Função que cria setas com base nas posições especificadas em sv
        arrows = [create_arrow(*position) for position in self.sv]
        #Testando com inicialização fora do laçõ para evitar repetição
        arrow_start = arrows[0]
        bloch_sphere.add(arrow_start)

        for i, arrow in enumerate(arrows):
            # Adiciona a imagem do circuito correspondente a esta etapa
            circuit_image = self.album[i]

            # Adicione a imagem à cena
            bloch_sphere.add(circuit_image)

            # Adicione a imagem à cena como um objeto fixo na moldura
            bloch_sphere.add_fixed_in_frame_mobjects(circuit_image)

            # aguarda o tempo em segundos da variavel speed
            bloch_sphere.wait(speed)

            # adiciona o vetor a cena
            bloch_sphere.play(Create(arrows[i]))

            # Verifique se existe um próximo vetor na lista

            if i < len(arrows) - 1:
                arrow_start = arrows[i]
                arrow_end = arrows[i + 1]

                frames = 30
                speedup_factor = 10  # Fator de aceleração

                for j in range(frames):
                    alpha = j / frames

                    x_alpha = (1 - alpha) * arrow_start.get_end()[0] + alpha * arrow_end.get_end()[0]
                    y_alpha = (1 - alpha) * arrow_start.get_end()[1] + alpha * arrow_end.get_end()[1]
                    z_alpha = (1 - alpha) * arrow_start.get_end()[2] + alpha * arrow_end.get_end()[2]

                    arrow_intermediate = Arrow3D(start=np.array([0, -4, -2]), end=np.array([x_alpha, y_alpha, z_alpha]),
                                                 color=BLUE)

                    arrow_start.become(arrow_intermediate)

                    bloch_sphere.play(Transform(arrow_start, arrow_intermediate), run_time=1 / speedup_factor)

        bloch_sphere.render()
