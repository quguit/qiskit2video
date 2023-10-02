
from qiskit2video import *

qreg_q = QuantumRegister(1, 'q')
creg_c = ClassicalRegister(0, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.x(qreg_q[0])
circuit.h(qreg_q[0])
circuit.h(qreg_q[0])
circuit.z(qreg_q[0])
circuit.h(qreg_q[0])
circuit.y(qreg_q[0])
circuit.x(qreg_q[0])

circuit.video(1)
