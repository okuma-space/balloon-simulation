import phys_const


# 浮力の計算式
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
