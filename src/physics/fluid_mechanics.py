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
    wind_velocity: float,
    target_velocity: float,
    drag_coefficient: float,
    cross_sectional_area: float,
) -> float:
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
    return (
        0.5
        * density
        * drag_coefficient
        * cross_sectional_area
        * relative_velocity
        * relative_velocity_norm
    )
