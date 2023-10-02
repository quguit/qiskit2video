
**Using the qiskit2video library, we can create animated images demonstrating the quantum state of a qubit in terms of bloch sphere. This tool shows flexibility by allowing the user to choose the animation speed and the duration of play-back.**

**It's a valuable tool that enables visual exploration of the complex structure of quantum circuits.**


# Analysis of a Qubit on the Bloch Sphere

This project focuses on evaluating and representing both the current status of a single qubit within a quantum circuit and how it changes when depicted on the Bloch sphere.

## Introdução

The fundamental building block of quantum information processing is called a qubit, which acts as an equivalent counterpart to classical bits but with added capabilities such as existing in different base states simultaneously ($\ket{0}$ and $\ket{1}$). In order to represent these base states, one uses vectors in Hilbert space having complex components which correspond to a finite space equipped with an inner product.
			
The current state of a qubit can be analyzed using:

$\ket{\psi} = \alpha\ket{1} + \beta\ket{0}$


Real or imaginary, $\alpha$ e $\beta$ assume various values whose addition yields a modulus sum equaling $|\alpha|+|\beta|=1$. By understanding this concept, it becomes apparent how probabilities for observing different states arise upon measuring $\ket{\psi}$, ultimately leading to a collapse in its superposition form towards one particular base state.

 Quantum gates modify the system's state through unitary matrices that consist of complex elements.

## Project stages

In this project, we took the following steps:

1. A function that receives the 1 qubit circuit and returns the state vector
2. The state vector is stored in a list.
3. At the end, the list with the state vectors must be passed to a function that builds a Manin-based video showing the state transitions in the bloch sphere.
4. **Quantum Gates:** For a qubit, we brought examples with Hadamard and Pauli-x gates.
![Matriz](matrix.png)

## To use this project, follow these steps:

1. **Clone the Repository:** Clone this repository on your local machine using the following command:
```github
git clone https://github.com/qguit/knowledge-representation.git
```
3. **Execute Code:**: Open the source code and follow the instructions to analyze the qubit and visualize its transformations on the Bloch sphere.

4. **Contributions:**: Feel free to contribute improvements or corrections to this project. Just fork the repository, make your changes and send a pull request.
5. 
## Prerequisites

Make sure you have the following libraries and tools installed on your machine:

- [Python3](https://packaging.python.org/pt_BR/latest/guides/installing-using-pip-and-virtual-environments/)
  
- [Bibliotecas de computação quântica (Qiskit)](https://qiskit.org/documentation/stable/0.24/locale/pt_BR/install.html)
  
- [Biblioteca Manim ](https://docs.manim.community/en/stable/installation.html)

## Example of use:

```python
# Exemplo de código Python para representar um qubit na esfera de Bloch
import numpy as np
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute, BasicAer, transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from qiskit.visualization import array_to_latex
from qiskit.visualization import plot_state_qsphere, plot_bloch_multivector

bell = QuantumCircuit(2, 2)
bell.h(0)
bell.cx(0, 1)

meas = QuantumCircuit(2, 2)
meas.measure([0,1], [0,1])

# execute the quantum circuit
backend = BasicAer.get_backend('qasm_simulator') # the device to run on
circ = bell.compose(meas)
result = backend.run(transpile(circ, backend), shots=1000).result()
counts  = result.get_counts(circ)
print(counts)

backend = BasicAer.get_backend('statevector_simulator') # the device to run on
result = backend.run(transpile(bell, backend)).result()
psi = result.get_statevector(bell)
print(psi)
vector = psi
#
# # Simulação do circuito para obter o estado final
# simulator = Aer.get_backend('qasm_simulator')
# result = execute(circuit, backend=simulator).result()
# print(np.array(result.get_statevector), np.array(result.get_counts(circuit)))
# vector = np.asarray(result.get_statevector)
# print(vector)
#
# # Converter o vetor de estado para o formato desejado
# formatted_vector = np.asarray(vector)
#
# print(formatted_vector)

plot_state_qsphere(psi)
plot_bloch_multivector(psi)
```

Contributions are welcome! 

In the event that you come across bugs, problems or have ideas for 
additional features, feel free to open an 
issue or send a pull request.

This project is governed by the MIT License - check the LICENSE file for more information.

 Have fun discovering the wonders of quantum computing and exploring the analysis of qubits on the Bloch sphere.


