import numpy as np


class Balloon:
    def __init__(
        self,
        mass: float,  # 質量[kg]
        volume: float,  # 体積[m^3]
        gas_density: float,  # ガスの気体密度[kg/m^3]
    ):
        self.mass = mass
        self.volume = volume
        self.gas_density = gas_density
