
from main.qiskit2video import *

qreg_q = QuantumRegister(1, 'q')  # declaring one quantum registers

creg_c = ClassicalRegister(0, 'c')  # and zero classic registers

circuit = QuantumCircuit(qreg_q, creg_c)  # creating a Quantum circuit

# by default the qubit starts at ket 0 or state zero

circuit.h(qreg_q[0])  # applying the Haddamard gatw

circuit.h(qreg_q[0])  # applying again Haddamard gate

circuit.x(qreg_q[0])  # applying the Pauli-X gate

circuit.x(qreg_q[0])  # applying the Pauli-X gate

circuit.z(qreg_q[0])  # apllying the Pauli-Z gate


circuit.y(qreg_q[0])  # apllying the Pauli-Y gate

circuit.y(qreg_q[0])  # apllying the Pauli-Y gate

circuit.video(15, 30)  # create the animation of scene,passing the parameters transition speed and frames respectively

