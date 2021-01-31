import numpy as np


def get_ground_state(num_qubits):
    q = list([0. for _ in range(2 ** num_qubits - 1)])
    q.insert(0, 1.)
    return np.array(q)


def get_operator(total_qubits, gate_unitary, target_qubits):
    gates = {
        "i": np.identity(2),
        "x": np.array([[0, 1], [1, 0]]),
        "y": np.array([[0, -1.j], [1.j, 0]]),
        "z": np.array([[1, 0], [0, -1]]),
        "h": 1. / np.sqrt(2) * np.array([[1, 1], [1, -1]]),
        "c0": np.array([[1, 0], [0, 0]]),
        "c1": np.array([[0, 0], [0, 1]])
    }

    if gate_unitary.startswith("c"):
        moment = [[gates["i"] for _ in range(2)] for _ in range(total_qubits)]
        moment[target_qubits[0]][0] = gates["c0"]
        moment[target_qubits[0]][1] = gates["c1"]
        moment[target_qubits[1]][1] = gates[gate_unitary[1]]

        operator = [1., 1.]
        for second in moment:
            for i in range(len(second)):
                operator[i] = np.kron(operator[i], second[i])
        operator = operator[0] + operator[1]

    else:
        moment = [gates["i"] for _ in range(total_qubits)]
        for i, qubit in enumerate(target_qubits):
            moment[qubit] = gates[gate_unitary[i]]

        operator = [1.]
        for second in moment:
            operator = np.kron(operator, second)

    return np.array(operator)


def run_program(initial_state, program):
    n = int(np.log2(len(initial_state)))
    for line in program:
        unitary_operator = get_operator(n, line["gate"], line["target"])
        initial_state = np.dot(initial_state, unitary_operator)
    return initial_state


def measure_all(state_vector):
    from numpy.random import choice
    draw = choice([i for i in range(len(state_vector))], 1, p=state_vector ** 2)
    return int(draw)


def get_counts(state_vector, num_shots):
    # simply execute measure_all in a loop num_shots times and
    # return object with statistics in following form:
    #   {
    #      element_index: number_of_ocurrences,
    #      element_index: number_of_ocurrences,
    #      element_index: number_of_ocurrences,
    #      ...
    #   }
    # (only for elements which occoured - returned from measure_all)
    measurements = [0 for i in range(len(state_vector))]
    for _ in range(num_shots):
        measure = measure_all(state_vector)
        measurements[measure] += 1
    dummy = {}
    for i, measure in enumerate(measurements):
        dummy['{0:08b}'.format(i)] = measure
    return dummy


my_circuit = [
{ "gate": "h", "target": [0] },
{ "gate": "cx", "target": [0, 1] }
]


# Create "quantum computer" with 2 qubits (this is actually just a vector :) )

my_qpu = get_ground_state(2)


# Run circuit

final_state = run_program(my_qpu, my_circuit)


# Read results

counts = get_counts(final_state, 1000)

print(counts)

# Should print something like:
# {
#   "00": 502,
#   "11": 498
# }

# Voila!