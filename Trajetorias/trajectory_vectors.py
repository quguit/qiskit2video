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

            intermediate_arrow = Arrow3D(start=np.array([0, 0, 0]), end=np.array([x_alpha, y_alpha, z_alpha]), color=GREEN)

            #become faz com que um vetor assuma propriedades de outro
            first_vector.become(intermediate_arrow)

            # Transform cria uma animação entre as posições especificadas e run_time especifica o tempo total da animação.
            self.play(Transform(first_vector, intermediate_arrow), run_time=1 / speedup_factor)

        self.wait(1)

