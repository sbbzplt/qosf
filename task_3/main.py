import numpy as np


def get_ground_state(num_qubits):
    q = list([0. for _ in range(2 ** num_qubits - 1)])
    q.insert(0, 1.)
    return np.array(q)


def get_operator(total_qubits, gate_unitary, target_qubits):
    # return unitary operator of size 2**n x 2**n for given gate and target qubits


    # TODO: replace return state with actual operator.
    return np.identity(2 ** total_qubits)


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
