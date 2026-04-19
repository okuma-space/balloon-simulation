from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from systems.balloon_system import BalloonSystem
import dynamics.vertical_dynamics as vertical_dynamics
import json

OUTPUT_DIR = Path("docs")


def simulate_balloon_trajectory(
    balloon: BalloonSystem,
    epoch_time: datetime,
    initial_position: np.ndarray,
    initial_velocity: np.ndarray,
    time_step: timedelta,
    save_state_interval: timedelta,
    propagation_time: timedelta,
) -> tuple[np.ndarray, np.ndarray]:
    """指定されたpropagation_timeにわたって気球の鉛直ダイナミクスをシミュレートし、stateの配列を返す。"""
    traj = vertical_dynamics.propagate(
        balloon,
        epoch_time,
        initial_position,
        initial_velocity,
        time_step,
        save_state_interval,
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

    return (
        times,
        altitude,
        vertical_velocity,
        traj.volume_list,
        traj.gas_density_list,
        traj.cross_sectional_area_list,
    )


def save_position_trajectory_html(
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
            hovertemplate="Time: %{x:.1f}<br>Altitude: %{y:.1f} m",
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
            hovertemplate="Time: %{x:.1f}<br>Velocity: %{y:.1f} m/s",
        )
    )

    fig.update_layout(
        title="Balloon Position and Velocity Trajectory",
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


def save_volume_area_history_html(
    time_seconds: np.ndarray,
    volume: np.ndarray,
    area: np.ndarray,
    output_path: Path,
) -> None:
    """体積と断面積をプロットしてHTML保存"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=volume,
            mode="lines",
            name="Volume [m^3]",
            yaxis="y1",
            hovertemplate="Time: %{x:.1f}<br>Volume: %{y:.1f} m^3",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=area,
            mode="lines",
            name="Area [m^2]",
            yaxis="y2",
            hovertemplate="Time: %{x:.1f}<br>Area: %{y:.1f} m^2",
        )
    )

    fig.update_layout(
        title="Balloon Volume and Area History",
        xaxis=dict(title="Time [s]"),
        yaxis=dict(title="Volume [m^3]", side="left"),
        yaxis2=dict(
            title="Area [m^2]",
            overlaying="y",
            side="right",
        ),
        legend=dict(x=0.01, y=0.99),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_gas_density_history_html(
    time_seconds: np.ndarray,
    gas_density: np.ndarray,
    output_path: Path,
) -> None:
    """ガス密度をプロットしてHTML保存"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=gas_density,
            mode="lines",
            name="Gas Density [kg/m^3]",
        )
    )

    fig.update_layout(
        title="Balloon Gas Density History",
        xaxis=dict(title="Time [s]"),
        yaxis=dict(title="Gas Density [kg/m^3]"),
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
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        fontsize=6,
        frameon=True,
        framealpha=0.8,
        labelspacing=0.2,
        handlelength=1.0,
        handletextpad=0.3,
        borderpad=0.2,
    )

    plt.title("Balloon Position and Velocity Trajectory")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def save_volume_area_history_png(
    time_seconds: np.ndarray,
    volume: np.ndarray,
    area: np.ndarray,
    output_path: Path,
) -> None:
    """体積と断面積をPNG保存"""
    fig, ax1 = plt.subplots()

    ax1.plot(time_seconds, volume, label="Volume [m^3]")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Volume [m^3]")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(time_seconds, area, linestyle="--", label="Area [m^2]")
    ax2.set_ylabel("Area [m^2]")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        fontsize=6,
        frameon=True,
        framealpha=0.8,
        labelspacing=0.2,
        handlelength=1.0,
        handletextpad=0.3,
        borderpad=0.2,
    )

    plt.title("Balloon Volume and Area History")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def save_gas_density_history_png(
    time_seconds: np.ndarray,
    gas_density: np.ndarray,
    output_path: Path,
) -> None:
    """ガス密度をPNG保存"""
    fig, ax = plt.subplots()

    ax.plot(time_seconds, gas_density, label="Gas Density [kg/m^3]")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Gas Density [kg/m^3]")
    ax.grid(True)

    ax.legend(
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        fontsize=6,
        frameon=True,
        framealpha=0.8,
        labelspacing=0.2,
        handlelength=1.0,
        handletextpad=0.3,
        borderpad=0.2,
    )

    plt.title("Balloon Gas Density History")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def main():
    config = load_config("config.json")

    # configからBalloonSystemオブジェクトを作成
    balloon_cfg = config["balloon"]
    balloon = BalloonSystem(**balloon_cfg)

    # trajectoryの初期条件をconfigから読み込む
    traj_cfg = config["trajectory"]

    epoch = datetime.fromisoformat(traj_cfg["epoch"].replace("Z", "+00:00"))

    initial_position = np.array(traj_cfg["initial_position"], dtype=float)
    initial_velocity = np.array(traj_cfg["initial_velocity"], dtype=float)

    # 計算条件をconfigから読み込む
    calc_cfg = config["calculate"]

    time_step = timedelta(seconds=calc_cfg["time_step_seconds"])
    save_state_interval = timedelta(seconds=calc_cfg["save_state_interval_seconds"])
    propagation_duration = timedelta(seconds=calc_cfg["propagation_duration_seconds"])

    # simulation
    (
        time_seconds,
        altitude,
        vertical_velocity,
        volume,
        gas_density,
        area,
    ) = simulate_balloon_trajectory(
        balloon,
        epoch,
        initial_position,
        initial_velocity,
        time_step,
        save_state_interval,
        propagation_duration,
    )

    # 出力ファイルのパスを定義
    html_path = OUTPUT_DIR / "html/balloon_posvel_trajectory.html"
    png_path = OUTPUT_DIR / "png/balloon_posvel_trajectory.png"
    volume_area_html_path = OUTPUT_DIR / "html/balloon_volume_area_history.html"
    volume_area_png_path = OUTPUT_DIR / "png/balloon_volume_area_history.png"
    gas_density_html_path = OUTPUT_DIR / "html/balloon_gas_density_history.html"
    gas_density_png_path = OUTPUT_DIR / "png/balloon_gas_density_history.png"

    # HTMLとPNGを保存
    save_position_trajectory_html(time_seconds, altitude, vertical_velocity, html_path)
    save_trajectory_png(time_seconds, altitude, vertical_velocity, png_path)

    save_volume_area_history_html(
        time_seconds,
        volume,
        area,
        volume_area_html_path,
    )
    save_volume_area_history_png(
        time_seconds,
        volume,
        area,
        volume_area_png_path,
    )

    save_gas_density_history_html(
        time_seconds,
        gas_density,
        gas_density_html_path,
    )
    save_gas_density_history_png(
        time_seconds,
        gas_density,
        gas_density_png_path,
    )


if __name__ == "__main__":
    main()
