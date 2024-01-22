from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute, BasicAer, transpile, assemble
from numpy import pi
from qiskit.visualization import circuit_drawer
from manim import *
import numpy as np
import tempfile, os
    
origin = np.array([0, -4, -2]) # variable global, will be the origin of the bloch sphere


# Function to create a 3D arrow representing a quantum state
def create_arrow(x, y, z):

    #translating the axis to a global variable
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
        center=origin,  # Position of the sphere
        radius=radius,
        resolution=(12, 10),
    )
    sphere.set_fill(WHITE, 0.01) # sets the fill color of this circle to blue (WHITE, set in constants), and the fill transparency to 0.01.
    sphere.set_stroke(WHITE, width=1) # sets the stroke color of this circle to WHITE (defined in constants), and the stroke width to 1.
    return sphere


# Function to create 3D axes for visualization
def create_axes(radius):

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

    def construct(self):    # declaring only what should be started with the constructor

        # setting the radius of the vector for demonstration purposes, in practice the radius is always constant at 1.
        radius = 2

        # create the sphere and axes
        sphere = create_sphere(radius)
        axes = create_axes(radius)

        # Labels for scene
        ket0 = axes.get_z_axis_label(Tex(r"$| 0 \rangle$")).rotate(0, axis=LEFT).next_to(axes.z_axis, 1.0)
        ket1 = axes.get_z_axis_label(Tex(r"$| 1 \rangle$")).next_to(axes.z_axis, -2.0).rotate(135, Z_AXIS)
        ketX = axes.get_x_axis_label(Tex(r"$| + \rangle$")).next_to(axes.x_axis, 2.5).rotate(-10, axis=RIGHT)

        # Add mobjects (axes, sphere, labels) to the scene
        self.add(axes, sphere, ket0, ket1, ketX)

        # Camera setup, i.e. the user's view
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

# Receives alpha and beta from the qubit and transforms it into a polar representation
def rect2pol(alpha, beta):
    # Calculating polar coordinates
    r = np.sqrt(abs(alpha) ** 2 + abs(beta) ** 2)
    theta = 2 * np.arccos(alpha.real / r)
    phi = np.angle(beta)

    # Convert phi angle from [-π, π] to [0, 2π]
    if phi < 0:
        phi += 2 * np.pi
    return theta, phi

#simulates the circuit at that moment, used to obtain the quantum state (alpha and beta), in case of doubt consult the API on qiskit
def simulator(circuit):
    backend = Aer.get_backend('statevector_simulator')
    job = execute(circuit, backend)
    result = job.result()

    # Vector representation in 2-dimensional Hilbert space
    vector = result.get_statevector(circuit)
    # get alpha and beta to obtain the polar representation
    theta, phi = rect2pol(vector[0], vector[1])

    # calculating the Cartesian representation in 3D
    x = 1 * np.sin(theta) * np.cos(phi)
    y = 1 * np.sin(theta) * np.sin(phi)
    z = 1 * np.cos(theta)

    return [x, y, z]

# function that generates the circuit drawing
def generate_circuit_image(circuit):

    # Generate the visual representation of the circuit using 'mpl' from Qiskit
    temp_dir = tempfile.gettempdir()  # Diretório temporário para salvar a imagem
    image_path = os.path.join(temp_dir, "quantum_circuit.png")
    circuit_drawer(circuit, output='mpl', filename=image_path)

    # Loads the image generated using Manim
    circuit_image = ImageMobject(image_path)

    # Sizing up
    circuit_image.scale(1.2)

    # Position the image in the top left corner
    circuit_image.to_corner(UL)

    return circuit_image


# custom class inheriting from QuantumCircuit
class QuantumCircuit(QuantumCircuit):
    def __init__(self, qreg_q, *args, **kwargs):
        super().__init__(qreg_q, *args, **kwargs)

        # list of vector positions on the sphere
        self.sv = []

        # list of vectors created by Arrow3D from positions
        self.arrows = []

        # simulating the circuit and getting the position of the state vector at that instant
        self.sv.append(simulator(self))

        # list of images synchronized with the vectors and changes in the circuit
        self.album = []

        # upload the image to manim and add the scene
        self.album.append(generate_circuit_image(self))

    def video(self, speed=15, frames=30):  # self, velocidade, passos,
        # creating a 3D scene
        bloch_sphere = BlochSphere()
        # starting the constructor
        bloch_sphere.construct()

        # Function that creates arrows based on the positions specified in sv
        arrows = [create_arrow(*position) for position in self.sv]

        # position on the edge of the sphere
        pos_borda = np.array(self.sv[0])

        pos_sv = ((pos_borda * 2) + origin)

        bloch_sphere.add(arrows[0])

        bloch_sphere.wait(1) # wait 1 second

        # rai = np.linalg.norm(pos_borda)
        # r = rai*2

        # list to store the trace
        vector_points = []

        for i, arrow in enumerate(arrows):
            # Adiciona a imagem do circuito correspondente a esta etapa
            circuit_image = self.album[i]

            # Adicione a imagem à cena
            bloch_sphere.add(circuit_image)

            # Adicione a imagem à cena como um objeto fixo na moldura
            bloch_sphere.add_fixed_in_frame_mobjects(circuit_image)

            if i + 1 < len(arrows):

                first_vector = arrows[i]

                pos_i = np.array(self.sv[i])  # pega o vetor [x,y,z]
                inicio_trajeto = pos_i  # ((pos_i * 2) + origin)   pega a posição final end
                pos_f = np.array(self.sv[i + 1])
                fim_trajeto = pos_f  # ((pos_f * 2) + origin)  pega a posição final end

                r = np.linalg.norm(inicio_trajeto)

                for j in range(frames + 1):  # for de 0 até frames
                    alpha = j / frames

                    # Pega os ângulos do vetor inicial
                    theta_i = np.arctan2(inicio_trajeto[1], inicio_trajeto[0])
                    phi_i = np.arccos(inicio_trajeto[2] / np.linalg.norm(inicio_trajeto))
                    # print(np.linalg.norm(inicio_trajeto))
                    # Pega os ângulos do vetor final
                    theta_f = np.arctan2(fim_trajeto[1], fim_trajeto[0])
                    phi_f = np.arccos(fim_trajeto[2] / np.linalg.norm(fim_trajeto))
                    # print(np.linalg.norm(fim_trajeto))

                    # Incrementa os ângulos em função de alpha
                    theta = (1 - alpha) * theta_i + alpha * theta_f
                    phi = (1 - alpha) * phi_i + alpha * phi_f

                    x_alpha = r * np.sin(phi) * np.cos(theta)
                    y_alpha = r * np.sin(phi) * np.sin(theta)
                    z_alpha = r * np.cos(phi)

                    x = (x_alpha * 2)
                    y = (y_alpha * 2) - 4
                    z = (z_alpha * 2) - 2

                    if j > 0:
                        prev_x, prev_y, prev_z = vector_points[-1]
                        line = Line([prev_x, prev_y, prev_z], [x, y, z], color=RED)
                        bloch_sphere.add(line)

                    vector_points.append((x, y, z))

                    intermediate_arrow = Arrow3D(start=origin, end=np.array([x, y, z]), color=BLUE)

                    # Transform cria uma animação entre as posições especificadas e run_time especifica o tempo total da animação.
                    bloch_sphere.play(Transform(first_vector, intermediate_arrow), run_time=(1 / speed))

        bloch_sphere.wait(2)
        bloch_sphere.render()



    #you need to do these 3 steps for the logic gate to work,
    # 1st send the qubit to the parent class,
    # 2nd apply the list of positions by calling the simulator to pick the position at that moment,
    # 3rd generate the image and add it to the circuit.

    # custom method for the operation X
    def x(self, qubit, **kwargs):
        super().x(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))

    # custom method for the Pauli-Y gate
    def y(self, qubit):
        super().y(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))

    # custom method for the operation s
    def s(self, qubit):
        super().s(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))

    # custom method for the operation Pauli-z
    def z(self, qubit):
        super().z(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))

    # custom method for the operation t
    def t(self, qubit):
        super().t(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))

    # custom method for the operation H
    def h(self, qubit):
        super().h(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))

    # custom method for the operation U
    def u(self, theta1, theta2, theta3, qubit):
        super().u(theta1, theta2, theta3, qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))


