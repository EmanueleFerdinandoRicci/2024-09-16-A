from dataclasses import dataclass

from model.state import State


@dataclass
class Edge:
    s1: State
    s2: State