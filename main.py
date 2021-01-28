import cirq
import numpy as np
import math
import random
from scipy.optimize import minimize
import networkx as nx
from matplotlib import pyplot as plt


class Graph:
    def __init__(self, edges_set):
        self.edges_set = edges_set
        self.node_set = []
        for i in edges_set:
            if i.start_node not in self.node_set:
                self.node_set.append(i.start_node)
            if i.end_node not in self.node_set:
                self.node_set.append(i.end_node)


class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight


set_edges = [Edge(0, 1, 0.6), Edge(1, 2, 0.3), Edge(2, 3, 0.2), Edge(3, 4, 0.4)]

G = nx.Graph()

for z in set_edges:
    G.add_edge(str(z.start_node), str(z.end_node), weight=z.weight)

nx.draw(G)
plt.savefig('graph.png')
plt.clf()

# Defines the list of qubits

num = 5
depth = 4
rep = 1000
qubits = [cirq.GridQubit(0, i) for i in range(0, num)]


# Defines the initialization

def initialization(qubits):
    for i in qubits:
        yield cirq.H.on(i)


# Defines the cost unitary

def cost_unitary(qubits, gamma):
    for i in set_edges:
        yield cirq.ZZPowGate(exponent=-1 * gamma / math.pi).on(qubits[i.start_node], qubits[i.end_node])


# Defines the mixer unitary

def mixer_unitary(qubits, alpha):
    for i in range(0, len(qubits)):
        yield cirq.XPowGate(exponent=-1 * alpha / math.pi).on(qubits[i])


# Executes the circuit

def create_circuit(params):
    gamma = [params[0], params[2], params[4], params[6]]
    alpha = [params[1], params[3], params[5], params[7]]

    circuit = cirq.Circuit()
    circuit.append(initialization(qubits))
    for i in range(0, depth):
        circuit.append(cost_unitary(qubits, gamma[i]))
        circuit.append(mixer_unitary(qubits, alpha[i]))
    circuit.append(cirq.measure(*qubits, key='x'))
    print(circuit)

    simulator = cirq.Simulator()
    results = simulator.run(circuit, repetitions=rep)
    results = str(results)[2:].split(", ")
    new_res = []
    for i in range(0, rep):
        hold = []
        for j in range(0, num):
            hold.append(int(results[j][i]))
        new_res.append(hold)

    return new_res


# Defines the cost function

def cost_function(params):
    av = create_circuit(params)
    total_cost = 0
    for i in range(0, len(av)):
        for j in set_edges:
            total_cost += 0.5 * (((1 - 2 * av[i][j.start_node]) * (1 - 2 * av[i][j.end_node])) - 1)
    total_cost = float(total_cost) / rep

    print("Cost: " + str(total_cost))

    return total_cost


# Defines the optimization method

init = [float(random.randint(-314, 314)) / float(100) for i in range(0, 8)]
out = minimize(cost_function, x0=init, method="COBYLA", options={'maxiter': 100})
print(out)

optimal_params = out['x']
f = create_circuit(optimal_params)

# Creates visualization of the optimal state

nums = []
freq = []

for i in range(0, len(f)):
    number = 0
    for j in range(0, len(f[i])):
        number += 2 ** (len(f[i]) - j - 1) * f[i][j]
    if number in nums:
        freq[nums.index(number)] = freq[nums.index(number)] + 1
    else:
        nums.append(number)
        freq.append(1)

freq = [s / sum(freq) for s in freq]

print(nums)
print(freq)

x = range(0, 2 ** num)
y = []
for i in range(0, len(x)):
    if i in nums:
        y.append(freq[nums.index(i)])
    else:
        y.append(0)

plt.bar(x, y)
plt.savefig('probabilities.png')
plt.clf()
