from dataclasses import dataclass

import environment.atmosphere.isothermal_model as isothermal_model
from environment.atmosphere import layered_temperature_model


@dataclass(frozen=True)
class EnvironmentState:
    out_temperature: float  # 外気温[K]
    out_density: float  # 外気密度[kg/m^3]
    out_pressure: float  # 外気圧[Pa]


def calculate_environment(altitude: float) -> EnvironmentState:
    """
    指定高度における外部環境状態を計算する.

    Parameters
    ----------
    altitude : float
        高度 [m].

    Returns
    -------
    EnvironmentState
        外気温, 外気密度, 外気圧をまとめた外部環境状態.
    """
    out_temperature = layered_temperature_model.calculate_temperature(altitude)
    out_density = isothermal_model.calculate_density(altitude)
    out_pressure = isothermal_model.calculate_pressure(out_density)

    return EnvironmentState(
        out_temperature=out_temperature,
        out_density=out_density,
        out_pressure=out_pressure,
    )
