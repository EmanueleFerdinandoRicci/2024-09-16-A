from dataclasses import dataclass

from model.state import State


@dataclass
class Peso:
    s : State
    time : int