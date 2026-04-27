import numpy as np
from models.balloon_state import BalloonState
from typing import Iterable


class BalloonStateHistory:
    def __init__(self, states: Iterable[BalloonState] | None = None):
        self.states: list[BalloonState] = list(states) if states is not None else []

    def append(self, state: BalloonState) -> None:
        self.states.append(state)

    def extend(self, states: Iterable[BalloonState]) -> None:
        self.states.extend(states)

    def __len__(self) -> int:
        return len(self.states)

    def __getitem__(self, index: int) -> BalloonState:
        return self.states[index]

    @property
    def time_list(self) -> np.ndarray:
        return np.array([state.time for state in self.states], dtype=object)

    @property
    def position_vector_list(self) -> np.ndarray:
        return np.array([state.position_vector for state in self.states], dtype=float)

    @property
    def velocity_vector_list(self) -> np.ndarray:
        return np.array([state.velocity_vector for state in self.states], dtype=float)

    @property
    def volume_list(self) -> np.ndarray:
        return np.array([state.volume for state in self.states], dtype=float)

    @property
    def cross_sectional_area_list(self) -> np.ndarray:
        return np.array(
            [state.cross_sectional_area for state in self.states],
            dtype=float,
        )

    @property
    def gas_density_list(self) -> np.ndarray:
        return np.array([state.gas_density for state in self.states], dtype=float)

    @property
    def gas_mass_list(self) -> np.ndarray:
        return np.array([state.gas_mass for state in self.states], dtype=float)

    @property
    def gas_temperature_list(self) -> np.ndarray:
        return np.array([state.gas_temperature for state in self.states], dtype=float)
