class BalloonSystem:
    def __init__(
        self,
        payload_mass: float,  # 質量[kg]
        ground_volume: float,  # 地表面上での体積[m^3]
        max_volume : float, # 最大体積[m^3]
        gas_mass: float,  # ガス質量[kg]
        drag_coefficient: float,  # CD値/抗力係数 (無次元) 球体では約0.47(ref:https://www.arc.id.au/CannonballDrag.html?utm_source=chatgpt.com)
    ):
        self.payload_mass = payload_mass
        self.ground_volume = ground_volume
        self.max_volume = max_volume
        self.gas_mass = gas_mass
        self.drag_coefficient = drag_coefficient
