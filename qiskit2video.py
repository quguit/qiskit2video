from bloch_sphere import *


# Crie uma classe personalizada que herda de QuantumCircuit
class QuantumCircuit(QuantumCircuit):
    def __init__(self, qreg_q, *args, **kwargs):
        super().__init__(qreg_q, *args, **kwargs)
        self.sv = []  # lista de posições
        self.arrows = []  # lista de vetores criados Arrow3D
        self.sv.append(simulator(self))
        self.album = []
        self.album.append(generate_circuit_image(self))
        #self.entanglement = []  # Dicionário para rastrear o entrelaçamento
    # Adicione um método personalizado para a operação X
    def x(self, qubit, **kwargs):
        super().x(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))
        #self.add_entanglement(qubit)

    # Adicione métodos personalizados para as operações quânticas aqui

    # def add_entanglement(self, qubit):
    #     """
    #     Registra o entrelaçamento entre dois qubits.
    #     """
    #     if qubit not in self.entanglement:
    #         self.entanglement.append([])
    #     self.entanglement.append(qubit)




    # Adicione um método personalizado para a operação Pauli y
    def y(self, qubit):
        super().y(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))
        #self.add_entanglement(qubit)


    # Adicione um método personalizado para a operação s
    def s(self, qubit):
        super().s(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))
        #self.add_entanglement(qubit)


    # Adicione um método personalizado para a operação Pauli-z
    def z(self, qubit):
        super().z(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))
        #self.add_entanglement(qubit)


    # Adicione um método personalizado para a operação t
    def t(self, qubit):
        super().t(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))


    # Adicione um método personalizado para a operação H
    def h(self, qubit):
        super().h(qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))
        #self.add_entanglement(self.calculate_entanglement(qubit))


    # Adicione um método personalizado para a operação U
    def u(self, theta1, theta2, theta3, qubit):
        super().u(theta1, theta2, theta3, qubit)
        self.sv.append(simulator(self))
        self.album.append(generate_circuit_image(self))
        #self.add_entanglement(self.calculate_entanglement(qubit))



    def video(self, speed): # bideo, velocidade, exportação,
        # criando uma cena 3D
        bloch_sphere = BlochSphere()
        # executando o construtor
        bloch_sphere.construct()
        # Função que cria setas com base nas posições especificadas em sv
        arrows = [create_arrow(*position) for position in self.sv]

        for i, arrow in enumerate(arrows):
            # Adicione a imagem do circuito correspondente a esta etapa
            circuit_image = self.album[i]

            # Adicione a imagem à cena
            bloch_sphere.add(circuit_image)

            # Adicione a imagem à cena como um objeto fixo na moldura
            bloch_sphere.add_fixed_in_frame_mobjects(circuit_image)

            #aguarda o tempo em segundos da variavel speed
            bloch_sphere.wait(speed)

            #adiciona o vetor a cena
            bloch_sphere.play(Create(arrow))


            # # Adicione informações sobre o entrelaçamento à cena
            # entanglement_text = Text(f"Entanglement: {entanglement[i]:.2f}")
            # entanglement_text.to_corner(UL)
            # bloch_sphere.add_fixed_in_frame_mobjects(entanglement_text)

            # Verifique se existe um próximo vetor na lista
            if i < len(arrows) - 1:
                next_arrow = arrows[i + 1]
                transition_time = 0.5  # Ajuste o tempo de transição conforme necessário
                bloch_sphere.play(Transform(arrow, next_arrow, run_time=transition_time))

            # Remova a seta anterior
            if i > 0:
                bloch_sphere.remove(arrows[i - 1])

        bloch_sphere.render( )

