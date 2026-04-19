import numpy as np
import environment.atmosphere.isothermal_model as isothermal_model


def calculate_ground_volume(altitude: float, target_volume: float) -> float:
    """
    指定した高度で指定した体積となる気球の地表面上での体積を求める。

    Parameters
    ----------
    altitude : float
        高度 [m]
    target_volume : float
        指定した高度での体積 [m^3]

    Returns
    -------
    float
        地表面上での体積 [m^3]
    """
    # 指定した高度での大気密度を計算
    air_density_at_altitude = isothermal_model.calculate_density(altitude)

    # 指定した高度での大気圧を計算
    air_pressure_at_altitude = isothermal_model.calculate_pressure(
        air_density_at_altitude, altitude
    )

    # 地表面上での大気密度を計算
    air_density_at_ground = isothermal_model.calculate_density(0.0)

    # 地表面での大気圧を計算
    air_pressure_at_ground = isothermal_model.calculate_pressure(
        air_density_at_ground, 0.0
    )

    # 地表体積の計算（ボイル則）
    ground_volume = target_volume * air_pressure_at_altitude / air_pressure_at_ground

    return ground_volume


def calculate_volume_at_altitude(altitude: float, ground_volume: float) -> float:
    """
    地表面上での体積から指定した高度での体積を求める。

    Parameters
    ----------
    altitude : float
        高度 [m]
    ground_volume : float
        地表面上での体積 [m^3]

    Returns
    -------
    float
        指定した高度での体積 [m^3]
    """
    # 指定した高度での大気密度[kg/m^3]を計算
    air_density_at_altitude = isothermal_model.calculate_density(altitude)

    # 指定した高度での大気圧[Pa]を計算
    air_pressure_at_altitude = isothermal_model.calculate_pressure(
        air_density_at_altitude, altitude
    )

    # 地表面上での大気密度[kg/m^3]を計算
    air_density_at_ground = isothermal_model.calculate_density(0.0)

    # 地表面での大気圧を計算
    air_pressure_at_ground = isothermal_model.calculate_pressure(
        air_density_at_ground, 0.0
    )

    # 指定した高度での体積[m^3]の計算（ボイル則）
    # 指定した高度での体積 [m^3] =地表面上での体積 [m^3] * 地表面上での大気密度[kg/m^3] / 指定した高度での大気密度[kg/m^3]
    volume_at_altitude = (
        ground_volume * air_pressure_at_ground / air_pressure_at_altitude
    )

    return volume_at_altitude


def sphere_cross_section_area(volume) -> float:
    """球体の断面積[m^2]を計算する"""

    # 体積V[m^3]から半径r[m]を求める式
    # V = (4/3) * π * r^3  =>  r = (3V / (4π))^(1/3)
    r = (3 * volume / (4 * np.pi)) ** (1 / 3)

    # 断面積[m^2]を計算して返す
    # πr^2
    return np.pi * r**2
