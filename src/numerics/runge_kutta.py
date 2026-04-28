import numpy as np


def rk4_step(
    func, t: float, y: np.ndarray, dt: float, *args_for_func, **kwargs_for_func
) -> np.ndarray:
    """
    4次ルンゲクッタ法による数値積分法1ステップの計算.
    数値計算[新訂版] P.41
    Parameters
    ----------
    func : callable
        微分方程式 dy/dt = func(t, y)
        関数オブジェクトで、引数は時刻tと状態ベクトルyを受け取り、dy/dtを返す関数
    t : float
        現在時刻 [s]
    y : np.ndarray
        現在の状態ベクトル
    dt : float
        時間刻み [s]
    **args_for_func : dict
        funcに渡す追加の引数をキーワード引数で指定
        環境外乱モデルやシステム状態など、funcの計算に必要な追加の引数をキーワード引数で指定することができる

    Returns
    -------
    np.ndarray
        次ステップの状態ベクトル
    """

    # RK4の更新式
    # 数値計算[新訂版] P.42 式(4.19)
    k1 = func(t, y, *args_for_func, **kwargs_for_func)
    k2 = func(t + 0.5 * dt, y + 0.5 * dt * k1, *args_for_func, **kwargs_for_func)
    k3 = func(t + 0.5 * dt, y + 0.5 * dt * k2, *args_for_func, **kwargs_for_func)
    k4 = func(t + dt, y + dt * k3, *args_for_func, **kwargs_for_func)
    return y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def euler_step(
    func, t: float, y: np.ndarray, dt: float, *args_for_func, **kwargs_for_func
) -> np.ndarray:
    """
    試験用オイラー
    """
    k1 = func(t, y, *args_for_func, **kwargs_for_func)

    return y + dt * k1
