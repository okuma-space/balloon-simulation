import physics.balloon_mechanics as balloon_mechanics

from models.balloon_state import BalloonState
from models.balloon_state_history import BalloonStateHistory
from models.balloon_model import BalloonModel
from simulation_config import SimulationConfig
from initial_condition import InitialCondition
from control.vent_schedule import VentSchedule
import numpy as np
from datetime import datetime, timedelta
from numerics import runge_kutta
from dynamics import (
    trajectory_dynamics,
    thermal_dynamics,
    environment_state,
    gas_mass_dynamics,
)


# 独立状態変数アクセス用の定数
# state_vector = [ガス温度[K],ガス質量[Kg], position_vector[m],  velocity_vector[m/s]]
GAS_TEMPERATURE_INDEX = 0
GAS_MASS_INDEX = 1
POSITION_SLICE = slice(2, 5)
VELOCITY_SLICE = slice(5, 8)

# 従属状態変数アクセス用の定数
# derived_state_variables = [volume, cross_sectional_area, gas_density]
BALLOON_VOLUME_INDEX = 0
CROSS_SECTIONAL_AREA_INDEX = 1
GAS_DENSITY_INDEX = 2


def propagate(
    simulation_config: SimulationConfig,
    initial_condition: InitialCondition,
    balloon_model: BalloonModel,
    vent_schedule: VentSchedule,
) -> BalloonStateHistory:
    """
    指定された propagation_time にわたって気球の鉛直ダイナミクスをシミュレートする

    Parameters
    ----------
    balloon : BalloonSystem
        気球モデル
    initial_condition : InitialCondition
        初期条件
    simulation_config : SimulationConfig
        シミュレーション設定

    Returns
    -------
    BalloonStateHistory
        気球の state を記録した History オブジェクト
    """

    # 計算条件を取り出す
    current_time = initial_condition.epoch_time
    end_time = initial_condition.epoch_time + simulation_config.propagation_time
    time_step = simulation_config.time_step
    time_step_seconds = time_step.total_seconds()
    save_interval_steps = max(
        1,
        int(simulation_config.save_state_interval.total_seconds() / time_step_seconds),
    )

    # 気球初期値生成
    initial_state = BalloonState(
        time=current_time,
        position_vector=initial_condition.position,
        velocity_vector=initial_condition.velocity,
        volume=initial_condition.volume,
        cross_sectional_area=balloon_mechanics.sphere_cross_section_area(
            initial_condition.volume
        ),
        gas_density=initial_condition.gas_mass / initial_condition.volume,
        gas_mass=initial_condition.gas_mass,
        gas_temperature=initial_condition.gas_temperature,
    )
    state_history = BalloonStateHistory([initial_state])
    new_state = initial_state
    step_count = 0

    # propagation ループ
    while current_time < end_time:
        previous_state = state_history[-1] if step_count == 0 else new_state

        # 独立状態ベクトルを抽出
        # [ガス温度[K],ガス質量[Kg], position_vector[m],  velocity_vector[m/s]]
        state_vector = np.hstack(
            (
                previous_state.gas_temperature,
                previous_state.gas_mass,
                previous_state.position_vector,
                previous_state.velocity_vector,
            )
        )

        # 独立状態ベクトルの時間伝搬(4次ルンゲ-クッタ法)
        state_vector = runge_kutta.rk4_step(
            calculate_state_derivative,
            t=0.0,  # ルンゲクッタ法の中で使用される時刻は、現在の時刻からの相対的な時間であるため、0.0を渡す
            y=state_vector,
            dt=time_step_seconds,
            balloon_model=balloon_model,
            vent_schedule=vent_schedule,
            current_time=current_time,
            # ルンゲクッタ法の中で使用される時刻は、現在の時刻からの相対的な時間であるため、
            # current_timeを渡す必要はないが、将来的に環境モデルの時間変化を考慮する際に使用する可能性があるため、
            # 引数として渡すようにしている
        )

        # 更新された状態ベクトルから位置と速度を抽出
        position = state_vector[POSITION_SLICE]
        velocity = state_vector[VELOCITY_SLICE]

        # 地表面衝突判定
        if position[2] < 0.0:
            position = np.array([position[0], position[1], 0.0])
            velocity = np.array([0.0, 0.0, 0.0])
            # 地面衝突のためstateを作って返す(従属状態変数は中で計算する)
            new_state = BalloonState.from_independent_state_variables(
                time=current_time,
                position_vector=position,
                velocity_vector=velocity,
                gas_mass=state_vector[GAS_MASS_INDEX],
                gas_temperature=state_vector[GAS_TEMPERATURE_INDEX],
                balloon_model=balloon_model,
            )
            break

        # 時刻更新
        current_time += time_step
        step_count += 1

        # 新しい state を生成(従属状態変数は中で計算する)
        new_state = BalloonState.from_independent_state_variables(
            time=current_time,
            position_vector=position,
            velocity_vector=velocity,
            gas_mass=state_vector[GAS_MASS_INDEX],
            gas_temperature=state_vector[GAS_TEMPERATURE_INDEX],
            balloon_model=balloon_model,
        )

        # 保存間隔に応じて保存
        if step_count % save_interval_steps == 0:
            state_history.append(new_state)

    # 最終 state が未保存なら追加
    if state_history[-1].time != new_state.time:
        state_history.append(new_state)

    return state_history


def calculate_state_derivative(
    relative_time: float,
    state_vector: np.ndarray,
    balloon_model: BalloonModel,
    vent_schedule,
    current_time: datetime,
) -> np.ndarray:
    """
    状態ベクトルの時間微分を計算する関数.
    ルンゲクッタ法の中で呼び出されることを想定しており、追加の引数として気球モデルを受け取る.
    Parameters
    ----------
    relative_time : float
        ルンゲクッタ法の中で使用される相対時刻 [s]
    state_vector :  np.ndarray
        状態ベクトル.
        そのステージの仮状態としての気球の状態変数を想定している.
        抽象的だが将来的にカルマンフィルタなどで扱いやすいようにベクトルにしておく.
        [0] = ガス温度[K],
        [1] = ガス質量[Kg],
        [2] = position_x[m],
        [3] = position_y[m],
        [4] = position_z[m],
        [5] = velocity_x[m/s],
        [6] = velocity_y[m/s],
        [7] = velocity_z[m/s]]
    balloon_model : BalloonModel
        気球オブジェクト.
    vent_schedule : VentSchedule
        ガスの排出スケジュール.

    Returns
    -------
    np.ndarray
        状態ベクトルの時間微分
        [ delta_gas_temperature,
        vent_flow_mass_rate,
        previous_balloon_state.velocity_vector,
        acceleration_vector]
    """
    time_delta = timedelta(seconds=relative_time)

    # 現在の時刻を計算.
    # 絶対時刻にルンゲクッタ計算内部での相対時刻を加算する.
    absolute_time = current_time + time_delta

    # 高度[m]
    altitude = state_vector[POSITION_SLICE][2]

    # 外部環境モデルの更新
    environment = environment_state.calculate_environment(altitude)

    # 従属状態変数を計算
    # [0] = 気球体積[m^3],
    # [1] = 気球断面積[m^2],
    # [2] = ガス密度[kg/m^3]
    derived_state_variables = calculate_derived_state_variables(
        state_vector,
        balloon_model,
        environment.out_pressure,
    )

    # 内部状態モデルの時間微分を計算する
    # ガス温度[K]
    delta_gas_temperature = thermal_dynamics.calculate_temperature(
        environment.out_temperature, state_vector[GAS_TEMPERATURE_INDEX]
    )

    # ガス質量[Kg]
    gass_mass_rate = gas_mass_dynamics.calculate_gas_mass_rate(
        absolute_time,
        balloon_model,
        vent_schedule,
        state_vector[GAS_TEMPERATURE_INDEX],
        state_vector[GAS_MASS_INDEX],
        derived_state_variables[GAS_DENSITY_INDEX],
        derived_state_variables[BALLOON_VOLUME_INDEX],
        environment.out_pressure,
    )

    # 加速度[m/s^2]計算する
    acceleration_vector = trajectory_dynamics.calculate_acceleration_vector(
        state_vector[VELOCITY_SLICE],
        balloon_model,
        environment.out_density,
        derived_state_variables[GAS_DENSITY_INDEX],
        state_vector[GAS_MASS_INDEX],
        derived_state_variables[BALLOON_VOLUME_INDEX],
        state_vector[CROSS_SECTIONAL_AREA_INDEX],
    )

    # 状態ベクトルの時間微分
    return np.array(
        [
            delta_gas_temperature,
            gass_mass_rate,
            state_vector[VELOCITY_SLICE][0],
            state_vector[VELOCITY_SLICE][1],
            state_vector[VELOCITY_SLICE][2],
            acceleration_vector[0],
            acceleration_vector[1],
            acceleration_vector[2],
        ],
        dtype=float,
    )


def calculate_derived_state_variables(
    state_vector: np.ndarray,
    balloon_model: BalloonModel,
    out_pressure: float,
) -> np.ndarray:
    """
    状態ベクトルから気球の従属状態変数を計算する.
    状態ベクトルをballoon mechanicsへ直接渡さないためのラッパ関数となる.

    Parameters
    ----------
    state_vector : np.ndarray
        独立状態ベクトル.
        各要素の並びは以下を想定する.
        [0] = ガス温度 [K]
        [1] = ガス質量 [kg]
        [2] = position_x [m]
        [3] = position_y [m]
        [4] = position_z [m]
        [5] = velocity_x [m/s]
        [6] = velocity_y [m/s]
        [7] = velocity_z [m/s]

    balloon_model : BalloonModel
        気球モデル.

    out_pressure : float
        外気圧 [Pa].

    Returns
    -------
    np.ndarray
        従属状態変数ベクトル.
        各要素の並びは以下を想定する.
        [0] = 気球体積 [m^3]
        [1] = 気球断面積 [m^2]
        [2] = ガス密度 [kg/m^3]
    """
    return balloon_mechanics.calculate_derived_state_variables(
        gas_temperature=state_vector[GAS_TEMPERATURE_INDEX],
        gas_mass=state_vector[GAS_MASS_INDEX],
        position_vector=state_vector[POSITION_SLICE],
        out_pressure=out_pressure,
        balloon_model=balloon_model,
    )
