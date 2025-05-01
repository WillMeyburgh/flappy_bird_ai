import random
from typing import Dict, List, Tuple

import numpy as np
from flappy_bird_ai.v2.neat.genome import Genome
from flappy_bird_ai.v2.neat.link import Link
from flappy_bird_ai.v2.neat.node import Node


class GenomeManager:
    N_MUTATE_RATE = 0.2
    N_REPLACE_RATE = 0.05
    N_MUTATE_POWER = 1.2
    S_ADD_LINK_MUTATE_RATE = 0.05
    S_REMOVE_LINK_MUTATE_RATE = 0.04
    S_ADD_NODE_MUTATE_RATE = 0.1
    S_REMOVE_NODE_MUTATE_RATE = 0.05

    def __init__(self, input_size, output_size):
        self.node_id = input_size + output_size
        self.input_size = input_size
        self.output_size = output_size
        self.rng = random.Random()

    def new(self) -> Genome:
        nodes = {}
        links = {}

        for i in range(0, self.input_size):
            nodes[i] = Node.input(i)

        for j in range(self.input_size, self.input_size+self.output_size):
            nodes[j] = Node.sigmoid(j)

        for i in range(0, self.input_size):
            for j in range(self.input_size, self.input_size+self.output_size):
                links[(i,j)] = Link(i,j,True,2*self.rng.random()-1)

        return Genome(self.input_size, self.output_size,nodes, links)
    
    def new_node(self) -> Node:
        node = Node.sigmoid(self.node_id)
        self.node_id+= 1
        return node
    
    def mutate_add_node(self, genome: Genome):
        link_id = self.rng.choice(list(genome.links.keys()))

        node = self.new_node()
        genome.nodes[node.id] = node
        link = genome.links.pop(link_id)
        genome.links[(link_id[0], node.id)] = Link(link_id[0], node.id,True,1)
        genome.links[(node.id,link_id[1])] = Link(node.id,link_id[1],True,link.weight)

    def delete_node(self, genome: Genome, node):
        del genome.nodes[node]

        for (left, right) in list(genome.links.keys()):
            if left == node or right == node:
                del genome.links[(left, right)]

        genome._phenotype = None

    def mutate_remove_node(self, genome: Genome):
        nodes = set(genome.nodes.keys())

        for i in range(self.input_size+self.output_size):
            nodes.remove(i)

        if len(nodes) > 0:
            node = self.rng.choice(list(nodes))

            self.delete_node(genome, node)

        while len(genome.phenotype.layers[0]) > self.input_size:
            for node in genome.phenotype.layers[0]:
                if node >= self.input_size:
                    self.delete_node(genome, node)

    def mutate_add_link(self, genome: Genome):
        left = self.rng.choice(list(genome.nodes.keys()))

        found = False
        nodes = set()

        for i, layer in enumerate(genome.phenotype.layers):
            if left in layer:
                found = True
            elif found:
                nodes.update(layer)

        nodes = nodes.difference(genome.phenotype.links.get(left, set()))

        if len(nodes) > 0:

            right = self.rng.choice(list(nodes))

            genome.links[(left, right)] = Link(left, right,True,2*self.rng.random()-1)

            genome._phenotype = None

    def mutate_remove_link(self, genome: Genome):
        active = {l for l in genome.links if genome.links[l].active}

        if len(active) > 0:
            genome.links[self.rng.choice(list(active))].active = False

    def mutate_weights(self, genome: Genome):
        for link in genome.links.values():
            if self.rng.random() <= self.N_MUTATE_RATE:
                link.weight = np.clip(link.weight+self.rng.gauss(0, self.N_MUTATE_POWER),-2,2)
            elif self.rng.random() <= self.N_REPLACE_RATE:
                link.weight = 2*self.rng.random()-1

    def mutate_bias(self, genome: Genome):
        for node in genome.nodes.values():
            if node.id >= self.input_size+self.output_size:
                if self.rng.random() <= self.N_MUTATE_RATE:
                    node.bias = np.clip(node.bias+self.rng.gauss(0, self.N_MUTATE_POWER),-1,1)
                elif self.rng.random() <= self.N_REPLACE_RATE:
                    node.bias = 2*self.rng.random()-1

    def mutate(self, genome: Genome):
        self.mutate_weights(genome)
        self.mutate_bias(genome)

        mutation = None

        if self.rng.random() <= self.S_ADD_LINK_MUTATE_RATE:
            self.mutate_add_link(genome)
            mutation = "ADD_LINK"
        elif self.rng.random() <= self.S_REMOVE_LINK_MUTATE_RATE:
            self.mutate_remove_link(genome)
            mutation = "REMOVE_LINK"
        elif self.rng.random() <= self.S_ADD_NODE_MUTATE_RATE:
            self.mutate_add_node(genome)
            mutation = "ADD_NODE"
        elif self.rng.random() <= self.S_REMOVE_NODE_MUTATE_RATE:
            self.mutate_remove_node(genome)
            mutation = "REMOVE_NODE"

        if len(genome.phenotype.layers[0]) > self.input_size:
            print(f"CHANGE: {mutation}")

    def crossover_nodes(self, dominent: Genome, recessive: Genome) -> Dict[int, Node]:
        return {id:dominent.nodes[id].clone() for id in dominent.nodes}

    def crossover_links(self, dominent: Genome, recessive: Genome) -> Dict[Tuple[int,int], Node]:
        crossover_links = set(dominent.links.keys()).intersection(recessive.links.keys())
        keep = set(dominent.links.keys()).difference(crossover_links)
        dominent_subset = set(self.rng.choices(list(crossover_links), k = len(crossover_links)//2))
        recessive_subset = crossover_links.difference(dominent_subset)

        result = {}


        for link in dominent_subset:
            result[link] = dominent.links[link].clone()
        for link in recessive_subset:
            result[link] = recessive.links[link].clone()
        for link in keep:
            result[link] = dominent.links[link].clone()

        return result

    def crossover(self, dominent: Genome, recessive: Genome) -> Genome:
        result = Genome(
            self.input_size,
            self.output_size,
            self.crossover_nodes(dominent, recessive),
            self.crossover_links(dominent, recessive)
        )

        self.mutate(result)

        return result