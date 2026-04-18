import numpy as np


class Balloon:
    def __init__(
        self,
        mass: float,  # 質量[kg]
        volume: float,  # 体積[m^3]
        gas_density: float,  # ガスの気体密度[kg/m^3]
        drag_coefficient: float,  # CD値/抗力係数 (無次元) 球体では約0.47(ref:https://www.arc.id.au/CannonballDrag.html?utm_source=chatgpt.com)
    ):
        self.mass = mass
        self.volume = volume
        self.gas_density = gas_density
        self.drag_coefficient = drag_coefficient

    @property
    def cross_section_area(self) -> float:
        """断面積[m^2]を計算するプロパティ"""

        # 体積V[m^3]から半径r[m]を求める式
        # V = (4/3) * π * r^3  =>  r = (3V / (4π))^(1/3)
        r = (3 * self.volume / (4 * np.pi)) ** (1 / 3)

        # 断面積[m^2]を計算して返す
        # πr^2
        return np.pi * r**2
