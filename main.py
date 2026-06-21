from qiskit2video import *

# v1.0: escopo de 1 qubit apenas
qreg_q = QuantumRegister(1, "q")
circuit = QuantumCircuit(qreg_q)

# por padrão o qubit começa em |0>
circuit.h(qreg_q[0])  # Hadamard
circuit.h(qreg_q[0])  # Hadamard
circuit.x(qreg_q[0])  # NOT

circuit.video(5, 12)  # (velocidade da transição, frames por transição)
