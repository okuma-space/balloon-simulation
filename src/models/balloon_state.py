import numpy as np
from datetime import datetime

import physics.balloon_mechanics as balloon_mechanics
from models.balloon_model import BalloonModel


class BalloonState:
    def __init__(
        self,
        # time
        time: datetime,  # 時刻[UTC]
        # 独立状態変数(数値積分対象)
        # ------------------------------------
        # position/velocity
        position_vector: np.ndarray,  # 位置ベクトル [m]
        velocity_vector: np.ndarray,  # 速度ベクトル [m/s]
        # gas
        gas_mass: float,  # ガス質量 [kg]
        gas_temperature: float,  # ガス温度 [K]
        # ------------------------------------
        # 従属状態変数(独立状態変数から算出される状態変数)
        # ------------------------------------
        # geometry
        volume: float,  # 気球体積 [m^3]
        cross_sectional_area: float,  # 断面積 [m^2]
        # gas
        gas_density: float,  # ガス密度 [kg/m^3]
        # ------------------------------------
    ):
        # time
        self.time = time

        # position/velocity
        self.position_vector = np.asarray(position_vector, dtype=float)
        self.velocity_vector = np.asarray(velocity_vector, dtype=float)

        # gas
        self.gas_mass = float(gas_mass)
        self.gas_temperature = float(gas_temperature)

        # geometry
        self.volume = float(volume)
        self.cross_sectional_area = float(cross_sectional_area)

        # gas
        self.gas_density = float(gas_density)

    @classmethod
    def from_independent_state_variables(
        cls,
        time: datetime,
        position_vector: np.ndarray,
        velocity_vector: np.ndarray,
        gas_mass: float,
        gas_temperature: float,
        balloon_model: BalloonModel,
        out_pressure: float | None = None,
    ) -> "BalloonState":
        """
        独立状態変数から従属状態変数を計算して BalloonState を生成する.
        """

        derived_state_variables = balloon_mechanics.calculate_derived_state_variables(
            gas_temperature=gas_temperature,
            gas_mass=gas_mass,
            position_vector=position_vector,
            balloon_model=balloon_model,
            out_pressure=out_pressure,
        )

        return cls(
            time=time,
            position_vector=position_vector,
            velocity_vector=velocity_vector,
            gas_mass=gas_mass,
            gas_temperature=gas_temperature,
            volume=derived_state_variables[0],
            cross_sectional_area=derived_state_variables[1],
            gas_density=derived_state_variables[2],
        )
