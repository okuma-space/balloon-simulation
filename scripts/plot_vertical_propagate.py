from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from systems.balloon import Balloon
import dynamics.vertical_dynamics as vertical_dynamics

OUTPUT_DIR = Path("docs")


def simulate_balloon_trajectory(
    balloon: Balloon,
    epoch_time: datetime,
    initial_position: np.ndarray,
    initial_velocity: np.ndarray,
    time_step: timedelta,
    propagation_time: timedelta,
) -> tuple[np.ndarray, np.ndarray]:
    """指定されたpropagation_timeにわたって気球の鉛直ダイナミクスをシミュレートし、時刻と高度の配列を返す。"""
    traj = vertical_dynamics.propagate(
        balloon,
        epoch_time,
        initial_position,
        initial_velocity,
        time_step,
        propagation_time,
    )
    # 時刻,位置,速度の配列を取得
    # 時刻はepoch_timeからの経過秒数に変換
    times = np.array([(t - epoch_time).total_seconds() for t in traj.time_list])
    positions = np.array(traj.position_vector_list)
    velocities = np.array(traj.velocity_vector_list)

    # 高度と鉛直速度を抽出
    altitude = positions[:, 2]
    vertical_velocity = velocities[:, 2]

    return times, altitude, vertical_velocity


def save_trajectory_html(
    time_seconds: np.ndarray,
    altitude: np.ndarray,
    velocity: np.ndarray,
    output_path: Path,
) -> None:
    """高度と速度と時刻の配列をプロットしてHTMLファイルに保存。"""
    fig = go.Figure()

    # 高度（左軸）
    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=altitude,
            mode="lines",
            name="Altitude [m]",
            yaxis="y1",
        )
    )

    # 速度（右軸）
    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=velocity,
            mode="lines",
            name="Vertical Velocity [m/s]",
            yaxis="y2",
        )
    )

    fig.update_layout(
        title="Balloon Trajectory",
        xaxis=dict(title="Time [s]"),
        yaxis=dict(
            title="Altitude [m]",
            side="left",
        ),
        yaxis2=dict(
            title="Velocity [m/s]",
            overlaying="y",
            side="right",
        ),
        legend=dict(x=0.01, y=0.99),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_trajectory_png(
    time_seconds: np.ndarray,
    altitude: np.ndarray,
    velocity: np.ndarray,
    output_path: Path,
) -> None:
    """高度・速度と時刻の配列をプロットしてPNGファイルに保存。"""
    fig, ax1 = plt.subplots()

    # altitude（左軸）
    ax1.plot(time_seconds, altitude, label="Altitude [m]")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Altitude [m]")
    ax1.grid(True)

    # velocity（右軸）
    ax2 = ax1.twinx()
    ax2.plot(time_seconds, velocity, linestyle="--", label="Vertical Velocity [m/s]")
    ax2.set_ylabel("Velocity [m/s]")

    # 凡例統合（ここが重要）
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="upper right",
        fontsize=8,
        frameon=True,
        labelspacing=0.3,
        handlelength=1.5,
        borderpad=0.3,
    )

    plt.title("Balloon Trajectory")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    # 気球の初期条件を定義
    balloon = Balloon(
        mass=1.0,  # [kg]
        gas_density=0.178,  # [kg/m^3] (ヘリウムの密度)　(https://daitoh-mg.jp/1990/01/-helium.html?utm_source=chatgpt.com)
        volume=1.0,  # [m^3]
        drag_coefficient=0.47,  # (無次元) 球体では約0.47 (https://www.arc.id.au/CannonballDrag.html?utm_source=chatgpt.com)
    )

    # 初期位置と速度を定義
    epoch = datetime(2026, 1, 1, 0, 0, 0)
    initial_position = np.array([0.0, 0.0, 0.0])
    initial_velocity = np.array([0.0, 0.0, 0.0])

    # 伝播時間とタイムステップを定義
    time_step = timedelta(seconds=1)
    propagation_duration = timedelta(seconds=2000)

    # シミュレーションを実行して時刻と高度の配列を取得
    time_seconds, altitude, velocity = simulate_balloon_trajectory(
        balloon,
        epoch,
        initial_position,
        initial_velocity,
        time_step,
        propagation_duration,
    )

    html_path = OUTPUT_DIR / "html/balloon_trajectory.html"
    png_path = OUTPUT_DIR / "png/balloon_trajectory.png"

    # HTMLとPNGを保存
    save_trajectory_html(time_seconds, altitude, velocity, html_path)
    save_trajectory_png(time_seconds, altitude, velocity, png_path)


if __name__ == "__main__":
    main()
