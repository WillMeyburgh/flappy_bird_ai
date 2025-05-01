from dataclasses import dataclass


@dataclass
class Link:
    input_node_id: int
    output_node_id: int
    active: bool
    weight: float

    def clone(self) -> "Link":
        return Link(
            self.input_node_id,
            self.output_node_id,
            self.active,
            self.weight
        )