import numpy as np
from datetime import datetime

class Trajectory:
    def __init__(
        self,
        time_list: np.ndarray,  # 時刻配列 , shape (N,)
        position_vector_list: np.ndarray,  # 位置ベクトル配列 [m], shape (N, 3)
        velocity_vector_list: np.ndarray,  # 速度ベクトル配列 [m/s], shape (N, 3)
    ):
        self.time_list = np.array(time_list, dtype=datetime)
        self.position_vector_list = np.array(position_vector_list, dtype=float)
        self.velocity_vector_list = np.array(velocity_vector_list, dtype=float)
