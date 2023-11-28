from manim import *

class ThreeDSpace(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes() #cria o eixo sem setas direcionais
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES) #posiciona a visão do usuario
        self.add(axes) # adiciona eixo a cena

        # Definindo setas de exemplo
        arrow_start = Arrow3D(
            start=np.array([0, 0, 0]), 
            end=np.array([0, 0, 3]), 
            color=BLUE)
        arrow_end = Arrow3D(
            start=np.array([0, 0, 0]), 
            end=np.array([0,0,-3]), 
            color=RED)

        self.add(arrow_start) # adicinina seta inicial a cena
        
        vector_points = []
        #lines = []        

        frames = 60 # o passo da transição do inicio ao fim
        speedup_factor = 15  # Fator de aceleração

        for i in range(frames+1): #for de 0 até frames
            alpha = i / frames 

            start_vec = arrow_start.get_end() #pega a posição final end
            end_vec = arrow_end.get_end() #pega a posição final end

            r = np.linalg.norm(start_vec)  # linalg é submodulo do numpy e norm() calcula a norma, juntos dão o comprimento do vetor 
            
            #pega os angulos do vetor inicial
            start_theta = np.arctan2(start_vec[1], start_vec[0]) 
            start_phi = np.arccos(start_vec[2] / r)
            end_theta = np.arctan2(end_vec[1], end_vec[0])
            end_phi = np.arccos(end_vec[2] / r)

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
            arrow_start.become(intermediate_arrow)

            # Transform cria uma animação entre as posições especificadas e run_time especifica o tempo total da animação.
            self.play(Transform(arrow_start, intermediate_arrow), run_time=1 / speedup_factor)
          

            

              
        self.wait(1)
        

