import physics.balloon_mechanics as balloon_mechanics

from models.balloon_model import BalloonModel
from control.vent_schedule import VentSchedule
import physics.fluid_mechanics as fluid_mechanics
from datetime import datetime


def calculate_gas_mass_rate(
    absolute_time: datetime,
    balloon_model: BalloonModel,
    vent_schedule: VentSchedule,
    gas_temperature: float,
    gas_mass: float,
    gas_density: float,
    balloon_volume: float,
    out_pressure: float,
) -> float:
    """
    排気による気球内ガス質量の時間変化率を計算する.

    バルブが閉じている場合は 0.0 を返す.
    バルブが開いている場合は, 気球内圧と外気圧の差から
    排気流量を計算し, ガス質量変化率 [kg/s] を返す.

    Parameters
    ----------
    absolute_time : datetime
        現在の絶対時刻.
    balloon_model : BalloonModel
        気球モデル.
    vent_schedule : VentSchedule
        排気スケジュール.
    gas_temperature : float
        気球内ガス温度 [K].
    gas_mass : float
        気球内ガス質量 [kg].
    gas_density : float
        気球内ガス密度 [kg/m^3].
    balloon_volume : float
        気球体積 [m^3].
    out_pressure : float
        外気圧 [Pa].

    Returns
    -------
    float
        気球内ガス質量の時間変化率 [kg/s].
        排気時は負値, 非排気時は 0.0.
    """

    # ガス質量[Kg]
    # 排気スケジュールを確認して、現在の時刻が排気操作の期間内にあるかを判断する
    vent_flow_mass_rate = 0.0
    inner_pressure = 0.0
    if vent_schedule.is_open(absolute_time):
        # 気球内圧
        inner_pressure = balloon_mechanics.calculate_balloon_pressure(
            gas_temperature,
            gas_mass,
            balloon_volume,
            balloon_model.gas_type,
        )

        # 大気圧と気球内圧の差を計算
        pressure_diff = inner_pressure - out_pressure

        # ガス流量[kg/s]を計算
        vent_flow_mass_rate = fluid_mechanics.calculate_vent_flow_mass_rate(
            balloon_model.flow_coefficient,
            balloon_model.vent_area,
            pressure_diff,
            gas_density,
        )

    # 流出量なので基本は負値
    return -vent_flow_mass_rate
