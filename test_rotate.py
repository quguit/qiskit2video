from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import DensityMatrix, entropy

# Crie um circuito quântico com dois qubits
circuito = QuantumCircuit(2)

# Aplique uma porta Hadamard no primeiro qubit
circuito.h(0)

# Aplique uma porta CNOT (controlada-X) entre os qubits
circuito.cx(0, 1)

# Execute o circuito e obtenha a matriz de densidade resultante
simulator = Aer.get_backend('statevector_simulator')
resultado = execute(circuito, simulator).result()
print(resultado.get_statevector())
matriz_densidade = DensityMatrix(resultado.get_statevector())

# Calcule a entropia de entrelaçamento entre os qubits 0 e 1
entrelacamento = entropy(matriz_densidade, base=2)

print(f"Entropia de entrelaçamento: {entrelacamento} bits")
