
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute, BasicAer, transpile, assemble
from numpy import pi
from qiskit.visualization import circuit_drawer
from manim import *
import numpy as np
import tempfile, os

# Function to create a 3D arrow representing a quantum state
def create_arrow(x, y, z, phase):
    origin = (0, -4, -2)
    end = np.array([2*x, (2*y)-4, (2*z)-2])

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

    axis_lengths = (3 * radius,) * 3  # Set axis lengths to be twice the radius

    # Position the axes relative to the center of the sphere
    axes = ThreeDAxes(
        x_length=axis_lengths[0]*0.8,
        y_length=axis_lengths[1]*1.05,
        z_length=axis_lengths[2]*0.8,
        tips=False
    )

    axes.move_to((0, -4, -2))  # Move the axes to the desired position
    return axes


# Main scene class to visualize the Bloch sphere and quantum states
class BlochSphere(ThreeDScene):

    def construct(self):
        #self.set_camera_orientation(phi=pi/2.5, theta=pi/4)
        radius = 2
        # Position the sphere at the center of the space
        sphere = create_sphere(radius)

        axes = create_axes(radius)

        # Labels for quantum states
        ket0 = axes.get_z_axis_label(Tex(r"$| 0 \rangle$")).rotate(0, axis=LEFT).next_to(axes.z_axis, 1.0)
        ket1 = axes.get_z_axis_label(Tex(r"$| 1 \rangle$")).next_to(axes.z_axis, -2.0).rotate(135, Z_AXIS)
        ketX = axes.get_x_axis_label(Tex(r"$| + \rangle$")).next_to(axes.x_axis, 2.5).rotate(-10, axis=RIGHT)
        ketY = axes.get_y_axis_label(Tex(r"$| - \rangle$")).next_to(axes.y_axis, 5).rotate(70, axis=UP)

        # Add objects (axes, sphere, labels) to the scene
        self.add(axes, sphere, ket0, ket1, ketX, ketY)





        # Configuração da câmera
        self.set_camera_orientation(phi=pi / 2.5, theta=pi / 4, zoom= 1.1)


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


    phase = np.angle(vector[0]) - np.angle(vector[1])

    return [x, y, z, np.degrees(phase)]

def generate_circuit_image(circuit):
    #Gere a representação visual do circuito usando 'mpl' do Qiskit
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


