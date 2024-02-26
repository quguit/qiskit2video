from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
import numpy as np

# Definindo os registradores quânticos e clássicos
qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# Aplicando as portas X, Z e T ao qubit
circuit.x(qreg_q[0])
circuit.z(qreg_q[0])
circuit.y(qreg_q[0])

# Simulando o circuito
backend = Aer.get_backend('statevector_simulator')
job = execute(circuit, backend)
result = job.result()

# Obtendo o vetor de estado
vector = result.get_statevector(circuit)

# Calculando a fase do estado quântico
alpha = vector[0]
beta = vector[1]

# Calculando a fase considerando a porta T
phase = np.angle(beta) - np.angle(alpha) + np.pi/4

# Ajustando a fase para estar no intervalo [0, 2*pi]
phase = (phase + 2*np.pi) % (2*np.pi)

# Convertendo a fase para graus
phase_degrees = np.rad2deg(phase)

# Imprimindo a fase do estado quântico
print("Fase do estado quântico após aplicar X, Z e T:", phase_degrees)
