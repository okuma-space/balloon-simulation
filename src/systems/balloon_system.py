from datetime import datetime
from systems import gas


class BalloonSystem:
    def __init__(
        self,
        payload_mass: float,  # 質量[kg]
        payload_area: float,  # ペイロード表面積[m^2]
        payload_drag_coefficient: float,  # ペイロードのCD値/抗力係数 (無次元) 立方体では約1.1
        ground_volume: float,  # 地表面上での体積[m^3]
        max_volume: float,  # 最大体積[m^3]
        initial_gas_mass: float,  # 初期ガス質量[kg]
        initial_gas_temperature: float,  # 初期ガス温度[K]
        balloon_drag_coefficient: float,  # 気球のCD値/抗力係数 (無次元) 球体では約0.47(ref:https://www.arc.id.au/CannonballDrag.html?utm_source=chatgpt.com)
        vent_area: float,  # 排気弁の総開口部面積[m^2]
        flow_coefficient: float,  # 排気弁の流量係数
        gas_type: gas.LiftingGasType,  # 揚力ガスの種類
        # operation
        vent_schedule: list[
            tuple[datetime, datetime]
        ],  # 排気スケジュール [(開始時刻, 終了時刻), ...]
    ):
        self.payload_mass = payload_mass
        self.payload_area = payload_area
        self.payload_drag_coefficient = payload_drag_coefficient
        self.ground_volume = ground_volume
        self.max_volume = max_volume
        self.initial_gas_mass = initial_gas_mass
        self.initial_gas_temperature = initial_gas_temperature
        self.balloon_drag_coefficient = balloon_drag_coefficient
        self.vent_area = vent_area
        self.flow_coefficient = flow_coefficient
        self.gas_type = gas_type
        self.vent_schedule = vent_schedule
