from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute, BasicAer, transpile, assemble
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
def create_sphere(self: object, radius: int, position: float) -> object:
    sphere = Sphere(
        center=position,  # Position of the sphere
        radius=radius,
        resolution=(12, 10),
    )
    sphere.set_fill(WHITE, 0.01) # sets the fill color of this circle to blue (WHITE, set in constants), and the fill transparency to 0.01.
    sphere.set_stroke(WHITE, width=1) # sets the stroke color of this circle to WHITE (defined in constants), and the stroke width to 1.
    return sphere


# Function to create 3D axes for visualization
def create_axes(self, radius, position):

    axis_lengths = (radius*3)   # Set axis lengths to be twice the radius

    # Position the axes relative to the center of the sphere
    axes = ThreeDAxes(
        x_length=axis_lengths * 0.9,
        y_length=axis_lengths * 1.0,
        z_length=axis_lengths * 0.8,
        tips=False
    )

    axes.move_to(position)  # Move the axes to the desired position
    return axes

# Função para calcular as posições das esferas

def calculate_sphere_positions(self, num_qubits):
    positions = []
    for i in range(num_qubits):
        x = i * 3
        positions.append((x, -4, -2))
    return positions


# Main scene class to visualize the Bloch sphere and quantum states
class BlochSphere(ThreeDScene):

    def construct(self, n_qubits=None):    # declaring only what should be started with the constructor

        # setting the radius of the vector for demonstration purposes, in practice the radius is always constant at 1.
        radius = 2
        # calculate_sphere_positions(radius, n_qubits)
        # # create the sphere and axes
        # sphere = create_sphere(radius)
        # axes = create_axes(radius)
        #
        # # Labels for scene
        # ket0 = axes.get_z_axis_label(Tex(r"$| 0 \rangle$")).rotate(0, axis=LEFT).next_to(axes.z_axis, 1.0)
        # ket1 = axes.get_z_axis_label(Tex(r"$| 1 \rangle$")).next_to(axes.z_axis, -2.0).rotate(135, Z_AXIS)
        # ketX = axes.get_x_axis_label(Tex(r"$| + \rangle$")).next_to(axes.x_axis, 2.5).rotate(-10, axis=RIGHT)
        #
        # # Add mobjects (axes, sphere, labels) to the scene
        # self.add(axes, sphere, ket0, ket1, ketX)
        #
        # # Camera setup, i.e. the user's view
        # self.set_camera_orientation( theta=135 * DEGREES, phi=60 * DEGREES, gamma=0 * DEGREES)
        # Cálculo das posições das esferas

        sphere_positions = calculate_sphere_positions(n_qubits)

        # Criação das esferas e eixos
        spheres = []
        axes = []

        for position in sphere_positions:
            sphere = create_sphere(radius, position)
            axis = create_axes(radius, position)
            spheres.append(sphere)
            axes.append(axis)

        # Labels para a cena
        ket0 = axes[0].get_z_axis_label(Tex(r"$| 0 \rangle$")).rotate(0, axis=LEFT).next_to(axes[0].z_axis, 1.0)
        ket1 = axes[0].get_z_axis_label(Tex(r"$| 1 \rangle$")).next_to(axes[0].z_axis, -2.0).rotate(135, Z_AXIS)
        ketX = axes[0].get_x_axis_label(Tex(r"$| + \rangle$")).next_to(axes[0].x_axis, 2.5).rotate(-10, axis=RIGHT)

        # Adiciona mobjects (eixos, esferas, labels) à cena
        self.add(*axes, *spheres, ket0, ket1, ketX)

        # Configuração da câmera
        self.set_camera_orientation(theta=135 * DEGREES, phi=60 * DEGREES, gamma=0 * DEGREES)


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

        self.sv = [[] for _ in range(self.num_qubits)]
        self.arrows = [[] for _ in range(self.num_qubits)]        # list of vectors created by Arrow3D from positions
        self.album = [[] for _ in range(self.num_qubits)]

        for i in range(self.num_qubits):
            # simulating the circuit and getting the position of the state vector at that instant
            self.sv[i].append(simulator(self))

            # list of images synchronized with the vectors and changes in the circuit
            self.album[i].append(generate_circuit_image(self))


    def video(self, speed=15, frames=30):  # self, velocidade, passos

        # # creating a 3D scene
        # bloch_sphere = BlochSphere()
        # # starting the constructor
        # bloch_sphere.construct()
        #
        # # Function that creates arrows based on the positions specified in sv
        # arrows = [create_arrow(*position) for position in self.sv]
        #
        # bloch_sphere.add(arrows[0])     #set the 1st vector, ket 0
        # bloch_sphere.wait(1)    # wait 1 second
        #
        # # list to store the trace
        # vector_points = []
        bloch_spheres = []  # Lista para armazenar os BlochSpheres para cada qubit
        arrows = []
        for i in range(self.num_qubits):
            bloch_sphere = BlochSphere()
            # starting the constructor
            bloch_sphere.construct(self.num_qubits)

            # Function that creates arrows based on the positions specified in sv for the i-th qubit
            arrows[i] = [create_arrow(*position) for position in self.sv[i]]
            bloch_sphere.add(arrows[i][0])

            # for arrow in arrows:
            #     bloch_sphere.add(arrow[0])  # Adiciona cada seta individualmente ao BlochSphere

            bloch_sphere.wait(1)  # Espera 1 segundo

            # Adiciona o BlochSphere atual à lista de BlochSpheres
            bloch_spheres.append(bloch_sphere)

        # list to store the trace
        vector_points = []

        for i, arrow in enumerate(arrows):
            # Add the image of the circuit corresponding to this step
            circuit_image = self.album[i]

            # Add the image to scene
            bloch_sphere.add(circuit_image)

            # transforms the image in the scene as a fixed object in the frame
            bloch_sphere.add_fixed_in_frame_mobjects(circuit_image)

            if i + 1 < len(arrows):
                # 1st vector
                first_vector = arrows[i]
                #get the vector [x, y, z]
                pos_i = np.array(self.sv[i])

                # taking the coordinates for the path that the trace will follow
                inicio_trajeto = pos_i
                pos_f = np.array(self.sv[i + 1])
                fim_trajeto = pos_f

        #         # value of the radius based on the coordinates, even knowing that the value is always equal to 1,
        #         # the algorithm doesn't work if you use the constant r =1.
        #         r = np.linalg.norm(inicio_trajeto)
        #
        #         # Take the angles of the initial vector and convert radians for degrees
        #         phi_i = np.rad2deg(np.arctan2(inicio_trajeto[1], inicio_trajeto[0]))
        #         theta_i = np.rad2deg(np.arccos(inicio_trajeto[2] / np.linalg.norm(inicio_trajeto)))
        #         print("----------------------------------------")
        #         print("theta_i", theta_i)
        #         print("phi_i", phi_i)
        #         # Take the angles of the final vector
        #         phi_f = np.rad2deg(np.arctan2(fim_trajeto[1], fim_trajeto[0]))
        #         theta_f = np.rad2deg(np.arccos(fim_trajeto[2] / np.linalg.norm(fim_trajeto)))
        #         print("theta_f", theta_f)
        #         print("phi_f", phi_f)
        #
        #         if self.gates[i] == 'h':
        #             if theta_i == 0:
        #                 phi_i = -90
        #             elif theta_i == 90:
        #                 if phi_i == 180:
        #                     phi_i = -180
        #                     phi_f = -90
        #                 else:
        #                     phi_f = +90
        #             elif theta_i == 180:
        #                 phi_i = +90
        #
        #         elif self.gates[i] == 'z':
        #             theta_i = theta_f = 90
        #         # elif self.gates[i] == 'y':
        #         #
        #         elif self.gates[i] == 'x':
        #             if theta_i == 0:
        #                 phi_i = phi_f = -90
        #             elif theta_i == 180:
        #                 phi_i = phi_f = +90
        #                 theta_f = 0
        #         elif self.gates[i] == 's':
        #             phi_i = phi_f = 90
        #
        #
        #         for j in range(frames + 1):  # for de 0 até frames
        #
        #             alpha = j / frames
        #
        #             # Interpolate angles
        #             theta = (1 - alpha) * theta_i + alpha * theta_f
        #             phi = (1 - alpha) * phi_i + alpha * phi_f
        #
        #             if self.gates[i] == 'y':
        #                 if theta < 180:
        #                     phi_f = 0
        #                 else:
        #                     phi_f = 180
        #                     theta_f = 90
        #             print("theta", theta)
        #             print("phi", phi)
        #
        #             # converting to polar
        #             x_alpha = r * np.sin(np.deg2rad(theta)) * np.cos(np.deg2rad(phi))
        #             y_alpha = r * np.sin(np.deg2rad(theta)) * np.sin(np.deg2rad(phi))
        #             z_alpha = r * np.cos(np.deg2rad(theta))
        #
        #             # moving the axes from (0,0,0) for ( 0,-4,-2)
        #             x = (x_alpha * 2)
        #             y = (y_alpha * 2) - 4
        #             z = (z_alpha * 2) - 2
        #
        #             # this section is responsible for the path trace
        #             if j > 0:
        #                 prev_x, prev_y, prev_z = vector_points[-1]
        #                 line = Line([prev_x, prev_y, prev_z], [x, y, z], color=RED)
        #                 bloch_sphere.add(line)
        #             # apply the list so that the line knows where it left off
        #             vector_points.append((x, y, z))
        #
        #             # this is the next position of the vector
        #             intermediate_arrow = Arrow3D(start=origin, end=np.array([x, y, z]), color=BLUE)
        #
        #             # apply the transformation to the next coordinate in the loop and run_time specifies the total time of the animation.
        #             bloch_sphere.play(Transform(first_vector, intermediate_arrow), run_time=(1 / speed))
        #
        # #wait 2 seconds and start scene
        # bloch_sphere.wait(1)
        # bloch_sphere.render()


    #you need to do these 3 steps for the logic gate to work,
    # 1st send the qubit to the parent class,
    # 2nd apply the list of positions by calling the simulator to pick the position at that moment,
    # 3rd generate the image and add it to the circuit.

    # custom method for the operation H
    def h(self, qubit):
        super().h(qubit)
        indic_qubit = qubit.index
        # Apply modifications to the correct index
        self.sv[indic_qubit].append(simulator(self))
        self.album[indic_qubit].append(generate_circuit_image(self))

    # custom method for the operation X
    def x(self, qubit):
        super().x(qubit)
        indic_qubit = qubit.index
        # Apply modifications to the correct index
        self.sv[indic_qubit].append(simulator(self))
        self.album[indic_qubit].append(generate_circuit_image(self))

    # custom method for the Pauli-Y gate
    def y(self, qubit):
        super().y(qubit)
        indic_qubit = qubit.index
        # Apply modifications to the correct index
        self.sv[indic_qubit].append(simulator(self))
        self.album[indic_qubit].append(generate_circuit_image(self))

    # custom method for the operation s
    def s(self, qubit):
        super().s(qubit)
        indic_qubit = qubit.index
        # Apply modifications to the correct index
        self.sv[indic_qubit].append(simulator(self))
        self.album[indic_qubit].append(generate_circuit_image(self))

    # custom method for the operation Pauli-z
    def z(self, qubit):
        super().z(qubit)
        indic_qubit = qubit.index
        # Apply modifications to the correct index
        self.sv[indic_qubit].append(simulator(self))
        self.album[indic_qubit].append(generate_circuit_image(self))

    # custom method for the operation t
    def t(self, qubit):
        super().t(qubit)
        indic_qubit = qubit.index
        # Apply modifications to the correct index
        self.sv[indic_qubit].append(simulator(self))
        self.album[indic_qubit].append(generate_circuit_image(self))

    # custom method for the operation U
    def u(self, theta1, theta2, theta3, qubit):
        super().u(theta1, theta2, theta3, qubit)
        indic_qubit = qubit.index
        # Apply modifications to the correct index
        self.sv[indic_qubit].append(simulator(self))
        self.album[indic_qubit].append(generate_circuit_image(self))



