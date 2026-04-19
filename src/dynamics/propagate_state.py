from systems.balloon_system import BalloonSystem
import environment.atmosphere.isothermal_model as isothermal_model
import numpy as np
import physics.fluid_mechanics as fluid_mechanics
import physics.balloon_mechanics as balloon_mechanics
from datetime import datetime
from environment.atmosphere import layered_temperature_model


def propagate_state(
    balloon: BalloonSystem,
    current_time: datetime,
    position_vector: np.ndarray,
    velocity_vector: np.ndarray,
    gas_mass_list: np.ndarray,
    volume_list: np.ndarray,
    cross_sectional_area_list: np.ndarray,
    gas_density_list: np.ndarray,
    gas_temperature_list: np.ndarray,
    time_step_seconds: float,
) -> tuple[float, float, float, float, float]:
    """
    気球状態を1ステップ進めて物理量を更新する.

    現在時刻と位置,高度に基づき外気温度と外気圧を計算し,
    ガス質量の変化、体積・断面積・ガス密度・
    ガス温度の更新を行う.

    またガスの排出スケジュールに従ったガス排出も実施する.

    Parameters
    ----------
    balloon : BalloonSystem
        気球オブジェクト
    current_time : datetime
        現在時刻
    position_vector : np.ndarray
        位置ベクトル [x, y, z] [m]
    velocity_vector : np.ndarray
        速度ベクトル [vx, vy, vz] [m/s]
    gas_mass_list : np.ndarray
        直前のガス質量履歴 [kg]
    volume_list : np.ndarray
        直前の体積履歴 [m^3]
    cross_sectional_area_list : np.ndarray
        直前の断面積履歴 [m^2]
    gas_density_list : np.ndarray
        直前のガス密度履歴 [kg/m^3]
    gas_temperature_list : np.ndarray
        直前のガス温度履歴 [K]
    time_step_seconds : float
        計算タイムステップ [s]

    Returns
    -------
    tuple[float, float, float, float, float]
        更新後の状態を表すタプル
        (gas_mass, volume, cross_sectional_area, gas_density, gas_temperature)
    """
    # 温度[K]の更新(外気温と同一とする)
    altitude = position_vector[2]  # 高度[m]
    out_temperature = layered_temperature_model.calculate_temperature(altitude) # 外気温[K]
    gas_temperature = balloon_mechanics.calculate_temperature(
        out_temperature, gas_temperature_list[-1]
    )

    # 大気圧
    out_pressure = isothermal_model.calculate_pressure(
        isothermal_model.calculate_density(position_vector[2]),
        position_vector[2],
    )

    # ガス質量更新
    gas_mass = gas_mass_list[-1]

    # 排気スケジュールを確認して、現在の時刻が排気操作の期間内にあるかを判断する
    for vent_start_time, vent_end_time in balloon.vent_schedule:
        if vent_start_time <= current_time <= vent_end_time:
            # 排気操作が必要な場合、ガス質量を更新する
            # ここでは、単純に流量係数と排気弁の面積に基づいてガス質量を減少させる例を示す
            # 気球内圧
            inner_pressure = balloon_mechanics.calculate_balloon_pressure(
                balloon.initial_gas_temperature,
                gas_mass,
                volume_list[-1],
                balloon.gas_type,
            )

            # 大気圧と気球内圧の差を計算
            pressure_diff = inner_pressure - out_pressure

            # ガス流量[kg/s]を計算
            vent_flow_mass_rate = fluid_mechanics.calculate_vent_flow_mass_rate(
                balloon.flow_coefficient,
                balloon.vent_area,
                pressure_diff,
                gas_density_list[-1],
            )

            # ガス質量を計算
            # 前回ガス質量[kg] - ガス流量[kg/s] * 計算ステップ[s]
            gas_mass = gas_mass_list[-1] - vent_flow_mass_rate * time_step_seconds
            break

    # 体積[m^3]を更新
    volume = balloon_mechanics.calculate_volume_at_altitude(
        out_pressure, gas_temperature, gas_mass, balloon.gas_type, balloon.max_volume
    )

    # 体積の上限を設定
    volume = min(volume, balloon.max_volume)

    # 断面積[m^2]の更新(ペイロード断面積が気球断面積を上回る場合はペイロード断面積を用いる)
    cross_sectional_area = balloon_mechanics.sphere_cross_section_area(volume)
    cross_sectional_area = max(cross_sectional_area, balloon.payload_area)

    # ガス密度[kg/m^3]の更新
    gas_density = fluid_mechanics.calculate_density(gas_mass, volume)

    return (gas_mass, volume, cross_sectional_area, gas_density, gas_temperature)
