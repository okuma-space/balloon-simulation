import numpy as np
from datetime import datetime, timedelta

class InitialCondition:
    def __init__(
        self,
        epoch_time: datetime,  # epoch時刻
        position: np.ndarray,  # 初期位置ベクトル[m]
        velocity: np.ndarray,  # 初期速度ベクトル[m/s]
        volume: float,  # 地表面上での体積[m^3]
        gas_mass: float,  # 初期ガス質量[kg]
        gas_temperature: float,  # 初期ガス温度[K]
    ):
        self.epoch_time = epoch_time
        self.position = np.asarray(position, dtype=float)
        self.velocity = np.asarray(velocity, dtype=float)
        self.volume = float(volume)
        self.gas_mass = float(gas_mass)
        self.gas_temperature = float(gas_temperature)