





from typing import Dict, List, Set

from flappy_bird_ai.v2.neat.genome import Genome
from flappy_bird_ai.v2.neat.link import Link


class Phenotype:
    def __init__(self, genome: Genome):
        self.genome = genome
        self.generate_links()
        self.generate_layers()
        self.outputs = {}
        
    def pop_layer(self, nodes: Set[int], processed: Set[int]) -> List[int]:
        output_nodes = set()

        for node in nodes:
            output_nodes.update(self.links.get(node, set()))

        layer = nodes.difference(output_nodes)
        
        for node in layer:
            nodes.remove(node)
            processed.add(node)

        return list(layer)

    def generate_layers(self):
        self.layers: List[List[int]] = []

        nodes = set(self.genome.nodes.keys())
        processed = set()

        while len(nodes) > 0:
            self.layers.append(self.pop_layer(nodes, processed))

    def generate_links(self):
        self.links: Dict[int, Set[int]] = {}

        for (left, right), _ in self.genome.links.items():
            if left not in self.links:
                self.links[left] = set()

            self.links[left].add(right)

    def forward(self, inputs: List[float]) -> List[float]:
        self.outputs = {i:inputs[i] for i in range(self.genome.input_size)}

        for i in range(len(self.layers)):
            for input in self.layers[i]:
                try:
                    input_node = self.genome.nodes[input]
                    self.outputs[input] = input_node.activation(self.outputs[input] + input_node.bias)
                except KeyError as e:
                    print("E", self.layers, self.links)
                    raise e

                if input in self.links:
                    for output in self.links[input]:
                        if output not in self.outputs:
                            self.outputs[output] = 0
                        link: Link = self.genome.links[(input, output)]
                        if link.active:
                            self.outputs[output] += self.outputs[input]*link.weight

        result = []

        for i in range(self.genome.input_size, self.genome.input_size + self.genome.output_size):
            result.append(self.outputs[i])

        return result