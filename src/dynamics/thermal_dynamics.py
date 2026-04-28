def calculate_temperature(out_temperature: float, gas_temperature: float) -> float:
    """
    気球ガスの温度を計算する.

    外部温度と現在のガス温度から,気球内のガス温度を更新する.
    計算式は簡易的に (out_temperature - gas_temperature) / 1000.0 + gas_temperature を用いる.

    Parameters
    ----------
    out_temperature : float
        外部温度 [K]
    gas_temperature : float
        現在のガス温度 [K]

    Returns
    -------
    float
        更新後のガス温度 [K]
    """
    delta_gas_temperature = (out_temperature - gas_temperature) / 2000.0
    return delta_gas_temperature
