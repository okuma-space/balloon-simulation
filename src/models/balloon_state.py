import numpy as np
from datetime import datetime


class BalloonState:
    def __init__(
        self,
        # time
        time: datetime,  # 時刻[UTC]
        # position/velocity
        position_vector: np.ndarray,  # 位置ベクトル [m]
        velocity_vector: np.ndarray,  # 速度ベクトル [m/s]
        # geometry
        volume: float,  # 気球体積 [m^3]
        cross_sectional_area: float,  # 断面積 [m^2]
        # gass
        gas_density: float,  # ガス密度 [kg/m^3]
        gas_mass: float,  # ガス質量 [kg]
        gas_temperature: float,  # ガス温度 [K]
    ):
        # time
        self.time = time

        # position/velocity
        self.position_vector = position_vector
        self.velocity_vector = velocity_vector

        # geometry
        self.volume = volume
        self.cross_sectional_area = cross_sectional_area

        # gass
        self.gas_density = gas_density
        self.gas_mass = gas_mass
        self.gas_temperature = gas_temperature
