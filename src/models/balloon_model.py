from models import gas


class BalloonModel:
    def __init__(
        self,
        payload_mass: float, # ペイロード質量[kg]
        payload_area: float,  # ペイロード表面積[m^2]
        payload_drag_coefficient: float,  # ペイロードのCD値/抗力係数 (無次元) 立方体では約1.1
        max_volume: float,  # 気球最大体積[m^3]
        balloon_drag_coefficient: float,  # 気球のCD値/抗力係数 (無次元) 球体では約0.47(ref:https://www.arc.id.au/CannonballDrag.html?utm_source=chatgpt.com)
        vent_area: float,  # 排気弁の総開口部面積[m^2]
        flow_coefficient: float,  # 排気弁の流量係数
        gas_type: gas.LiftingGasType,  # 揚力ガスの種類
    ):
        self.payload_mass = payload_mass
        self.payload_area = payload_area
        self.payload_drag_coefficient = payload_drag_coefficient
        self.max_volume = max_volume
        self.balloon_drag_coefficient = balloon_drag_coefficient
        self.vent_area = vent_area
        self.flow_coefficient = flow_coefficient
        self.gas_type = gas_type
