from manim import *
import numpy as np

class RotatingVector(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        radius = 3
        axis_lengths = (radius * 3)  # Set axis lengths to be twice the radius

        # Position the axes relative to the center of the sphere
        axes = ThreeDAxes(
            x_length=axis_lengths * 0.9,
            y_length=axis_lengths * 1.0,
            z_length=axis_lengths * 0.8,
            tips=False
        )
        sphere = Sphere(
            center=(0, 0, 0),  # Posição da esfera
            radius=radius,
            resolution=(12, 10),
        )
        sphere.set_fill(BLUE_D, 0.1)
        sphere.set_stroke(width=1)
        self.add(axes, sphere)

        radius = 3
        initial_theta = 0
        initial_phi = 0

        num_passos = 5
        delta_theta = num_passos * DEGREES
        delta_phi = num_passos * DEGREES

        arrows = VGroup()
        rotating_vector = Arrow3D(start=np.array([0, 0, 0]), end=np.array([0, 0, 0]), color=BLUE)

        for i in range(18):
            # Atualiza o vetor com as novas coordenadas
            x = radius * np.sin(initial_theta) * np.cos(initial_phi)
            y = radius * np.sin(initial_theta) * np.sin(initial_phi)
            z = radius * np.cos(initial_theta)

            # Cria um novo vetor
            new_arrow = Arrow3D(start=np.array([0, 0, 0]), end=np.array([x, y, z]), color=GREEN)

            # Adiciona o novo vetor ao grupo
            arrows.add(new_arrow)

            # Atualiza o vetor existente
            rotating_vector.become(new_arrow)

            # Atualiza os ângulos
            initial_theta += delta_theta
            # Condição para inverter o sentido de theta
            if i < 9:
                initial_theta -= 2 * delta_theta
            initial_phi += delta_phi

            # Adiciona a trajetória à medida que o vetor se move
            if i > 0:
                prev_x, prev_y, prev_z = arrows[-2].get_end()
                line = Line([prev_x, prev_y, prev_z], [x, y, z], color=RED)
                self.add(line)

            # Rotação do vetor
            rotating_vector.rotate(angle=0.1, axis=OUT)
            self.add(rotating_vector)

        # Animação de transição suave
        self.play(
            *[
                Transform(arrows[i], arrows[i + 1])
                for i in range(len(arrows) - 1)
            ],
            run_time=3
        )

        self.wait(1) 
from manim import *

class ThreeDSpace(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes() #cria o eixo sem setas direcionais
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES) #posiciona a visão do usuario
        self.add(axes) # adiciona eixo a cena

        # Definindo setas de exemplo
        first_vector = Arrow3D(
            start=np.array([0, 0, 0]), 
            end=np.array([0, 0, 3]), 
            color=BLUE)
        next_vector = Arrow3D(
            start=np.array([0, 0, 0]), 
            end=np.array([0,0,-3]), 
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


            intermediate_arrow = Arrow3D(start=np.array([0, 0, 0]), end=np.array([x_alpha, y_alpha, z_alpha]), color=GREEN)

            #become faz com que um vetor assuma propriedades de outro
            first_vector.become(intermediate_arrow)

            # Transform cria uma animação entre as posições especificadas e run_time especifica o tempo total da animação.
            self.play(Transform(first_vector, intermediate_arrow), run_time=1 / speedup_factor)
          

            

              
        self.wait(1)
        


