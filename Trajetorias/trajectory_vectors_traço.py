from manim import *

origin = np.array([0, -4, -2]) #variable global

class ThreeDSpace(ThreeDScene):
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
        #self.set_camera_orientation(phi=pi / 2.5, theta=pi / 4, zoom=1.1)
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)


        # Definindo setas de exemplo
        first_vector = Arrow3D(
            start=origin, 
            end=np.array([0, 0, 1]), 
            color=BLUE)
        next_vector = Arrow3D(
            start=origin, 
            end=np.array([0,0,-5]), 
            color=RED)

        self.add(first_vector) # adicinina seta inicial a cena
        
        vector_points = []
        #lines = []        

        frames = 60 # o passo da transição do inicio ao fim
        speedup_factor = 15  # Fator de aceleração

        for i in range(frames+1): #for de 0 até frames
            alpha = i / frames 

            inicio_trajeotira = first_vector.get_end() #pega a posição final end
            fim_trajeotira = next_vector.get_end() #pega a posição final end

            r = np.linalg.norm(inicio_trajeotira)  # linalg é submodulo do numpy e norm() calcula a norma, juntos dão o comprimento do vetor 
            
            #pega os angulos do vetor inicial
            start_theta = np.arctan2(inicio_trajeotira[1], inicio_trajeotira[0]) 
            start_phi = np.arccos(inicio_trajeotira[2] / r)
            end_theta = np.arctan2(fim_trajeotira[1], fim_trajeotira[0])
            end_phi = np.arccos(fim_trajeotira[2] / r)

            #incrementa do angulo em função de theta
            theta = (1 - alpha) * start_theta + alpha * end_theta
            phi = (1 - alpha) * start_phi + alpha * end_phi

            x_alpha = r * np.sin(phi) * np.cos(theta)
            y_alpha = r * np.sin(phi) * np.sin(theta)
            z_alpha = r * np.cos(phi)

            if i > 0:    
                prev_x, prev_y, prev_z = vector_points[-1]
                line = Line([prev_x, prev_y, prev_z], [x_alpha, y_alpha, z_alpha], color=RED)
                #lines.append(line)
                self.add(line)
            
            vector_points.append((x_alpha, y_alpha, z_alpha))


            intermediate_arrow = Arrow3D(start=origin, end=np.array([x_alpha, y_alpha, z_alpha]), color=GREEN)

            #become faz com que um vetor assuma propriedades de outro
            first_vector.become(intermediate_arrow)

            # Transform cria uma animação entre as posições especificadas e run_time especifica o tempo total da animação.
            self.play(Transform(first_vector, intermediate_arrow), run_time=1 / speedup_factor)
          

            

              
        self.wait(1)
        


def create_arrow(x, y, z):
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
