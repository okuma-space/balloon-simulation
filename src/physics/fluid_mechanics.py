import phys_const
import numpy as np


def buoyant_force(density_out: float, density_in: float, volume: float) -> float:
    """
    浮力の計算式
    Parameters
    ----------
    density_out : float
        外部の密度 [kg/m^3]
    density_in : float
        内部の密度 [kg/m^3]
    volume : float
        体積 [m^3]

    Returns
    -------
    float
        浮力 [N]
    """

    # 気球工学 P.15 (2.4)
    # 浮力[N] = (外部の密度[kg/m^3] - 内部の密度[kg/m^3]) * 体積[m^3] * 重力加速度[m/s^2]
    return (density_out - density_in) * volume * phys_const.GRAVITY_ACCELERATION


def drag_force(
    density: float,
    wind_velocity: np.ndarray,
    target_velocity: np.ndarray,
    drag_coefficient: float,
    cross_sectional_area: float,
) -> np.ndarray:
    """
    抗力の計算式
    Parameters
    ----------
    density : float
        流体の密度 [kg/m^3]
    wind_velocity : np.ndarray
        風速 [m/s]
    target_velocity : np.ndarray
        対象物体の速度 [m/s]
    drag_coefficient : float
        抗力係数 (無次元)
    cross_sectional_area : float
        物体の投影面積 [m^2]

    Returns
    -------
    np.ndarray
        抗力ベクトル [N]
    """
    # 相対速度ベクトル [m/s]
    relative_velocity = wind_velocity - target_velocity
    # 相対速度ノルム [m/s]
    relative_velocity_norm = np.linalg.norm(relative_velocity)

    # 気球工学 P.53 (2.62)
    # 抗力[N] = 0.5 * 流体の密度[kg/m^3]  * 抗力係数 * 物体の投影面積[m^2] * 相対速度ベクトル[m/s] * 相対速度ベクトルノルム[m/s]
    # 抗力として向きを考慮するために、相対速度ベクトルの符号を保持している。
    drag_force = (
        0.5
        * density
        * drag_coefficient
        * cross_sectional_area
        * relative_velocity
        * relative_velocity_norm
    )

    return drag_force


def calculate_density(mass: float, volume: float) -> float:
    """密度[kg/m^3]を計算する関数"""
    # 質量/体積が0を下回ったときの対策
    if mass <= 0.0 or volume <= 0.0:
        return 0.0

    # 密度[kg/m^3] = 質量[kg] / 体積[m^3]
    return mass / volume


def calculate_vent_flow_mass_rate(
    flow_coefficient: float,
    vent_area: float,
    pressure_difference: float,
    gas_density: float,
) -> float:
    """
    排気ガスの質量流量[kg/s]を計算する関数
    気球工学 P.56 (2.79)

    Parameters
    ----------
    flow_coefficient : float
        流量係数 (無次元)
    vent_area : float
        排気弁の総開口部面積 [m^2]
    pressure_difference : float
        排気弁開口部における圧力差 [Pa]
    gas_density : float
        内部のガス密度 [kg/m^3]

    Returns
    -------
    float
        排気ガスの質量流量 [kg/s]
    """

    # 圧力差もしくは密度が0以下の場合は流量が発生しないため、質量流量も0とする。
    if pressure_difference <= 0.0 or gas_density <= 0.0:
        return 0.0

    # 気球工学 P.56 (2.79)
    # 浮揚ガスの体積流量[m^3/s] = 流出速度流量係数 * 排気弁の総開口部面積[m^2] sqrt(2 * 排気弁開口部における圧力差[Pa] / 内部のガス密度[kg/m^3])
    flow_volume_rate = (
        flow_coefficient * vent_area * np.sqrt(2 * pressure_difference / gas_density)
    )

    # 質量流量[kg/s] = 体積流量[m^3/s] * 密度[kg/m^3]
    flow_mass_rate = flow_volume_rate * gas_density
    return flow_mass_rate
