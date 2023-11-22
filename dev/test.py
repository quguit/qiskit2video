from manim import *
from numpy import pi

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
