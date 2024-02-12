
from qiskit2video import *

qreg_q = QuantumRegister(3, 'q')            # declaring one quantum registers
 
creg_c = ClassicalRegister(0, 'c')          # and zero classic registers

circuit = QuantumCircuit(qreg_q, creg_c)    # creating a Quantum circuit

# by default the qubit starts at ket 0 or state zero
#
# circuit.h(qreg_q[0])        # applying the Haddamard gatw
#
# circuit.h(qreg_q[1])        # applying again Haddamard gate
#
# circuit.x(qreg_q[2])        # applying the Pauli-X gate
#
# circuit.h(qreg_q[0])        # applying the Haddamard gatw
#
# circuit.z(qreg_q[1])
#
# circuit.y(qreg_q[2])
#
# circuit.y(qreg_q[0])
#
# circuit.h(qreg_q[1])        # applying again Haddamard gate
#
# circuit.x(qreg_q[2])        # apllying the Pauli-X gate



circuit.video(5, 12)   # create the animation of scene,passing the parameters transition speed and frames respectively

