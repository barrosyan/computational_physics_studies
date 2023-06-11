from qiskit import QuantumCircuit, transpile, Aer, execute
from qiskit.visualization import circuit_drawer

def optimize_quantum_circuit(circuit):
    # Transpile the circuit to optimize it
    optimized_circuit = transpile(circuit, optimization_level=3)
    return optimized_circuit

# Example usage
original_circuit = QuantumCircuit(2)
original_circuit.h(0)
original_circuit.cx(0, 1)
original_circuit.measure_all()  # Add measurement gates to the circuit
optimized_circuit = optimize_quantum_circuit(original_circuit)

# Execute the circuit
backend = Aer.get_backend('qasm_simulator')
job = execute(optimized_circuit, backend, shots=1000)
result = job.result()
counts = result.get_counts()
print(counts)