import numpy as np
from datetime import datetime


class BalloonStateTrajectory:
    def __init__(
        self,
        time_list: np.ndarray,  # 時刻配列 , shape (N,)
        position_vector_list: np.ndarray,  # 位置ベクトル配列 [m], shape (N, 3)
        velocity_vector_list: np.ndarray,  # 速度ベクトル配列 [m/s], shape (N, 3)
        volume_list: np.ndarray,  # 体積配列 [m^3], shape (N,)
        gas_density_list: np.ndarray,  # ガス密度配列 [kg/m^3], shape (N,)
        cross_sectional_area_list: np.ndarray,  # 断面積配列 [m^2], shape (N,)
    ):
        self.time_list = np.array(time_list, dtype=datetime)
        self.position_vector_list = np.array(position_vector_list, dtype=float)
        self.velocity_vector_list = np.array(velocity_vector_list, dtype=float)
        self.volume_list = np.array(volume_list, dtype=float)
        self.gas_density_list = np.array(gas_density_list, dtype=float)
        self.cross_sectional_area_list = np.array(
            cross_sectional_area_list, dtype=float
        )
