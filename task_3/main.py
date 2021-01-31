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
    # choose element from state_vector using weighted random and return it's index
    return


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
    return
