from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt


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


def save_gas_state_history_html(
    time_seconds: np.ndarray,
    gas_density: np.ndarray,
    gas_mass: np.ndarray,
    output_path: Path,
) -> None:
    """ガス密度とガス質量をプロットしてHTML保存"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=gas_density,
            mode="lines",
            name="Gas Density [kg/m^3]",
            yaxis="y1",
            hovertemplate="Time: %{x:.1f}<br>Gas Density: %{y:.4f} kg/m^3",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=gas_mass,
            mode="lines",
            name="Gas Mass [kg]",
            yaxis="y2",
            hovertemplate="Time: %{x:.1f}<br>Gas Mass: %{y:.3f} kg",
        )
    )

    fig.update_layout(
        title="Balloon Gas Density and Gas Mass History",
        xaxis=dict(title="Time [s]"),
        yaxis=dict(title="Gas Density [kg/m^3]", side="left"),
        yaxis2=dict(
            title="Gas Mass [kg]",
            overlaying="y",
            side="right",
        ),
        legend=dict(x=0.01, y=0.99),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_temperature_history_html(
    time_seconds: np.ndarray,
    temperature: np.ndarray,
    output_path: Path,
) -> None:
    """温度履歴をプロットしてHTML保存"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time_seconds,
            y=temperature,
            mode="lines",
            name="Temperature [K]",
            hovertemplate="Time: %{x:.1f}<br>Temperature: %{y:.2f} K",
        )
    )

    fig.update_layout(
        title="Balloon Gas Temperature History",
        xaxis=dict(title="Time [s]"),
        yaxis=dict(title="Temperature [K]"),
        legend=dict(x=0.01, y=0.99),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


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


def save_gas_state_history_png(
    time_seconds: np.ndarray,
    gas_density: np.ndarray,
    gas_mass: np.ndarray,
    output_path: Path,
) -> None:
    """ガス密度とガス質量をPNG保存"""
    fig, ax1 = plt.subplots()

    ax1.plot(time_seconds, gas_density, label="Gas Density [kg/m^3]")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Gas Density [kg/m^3]")
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.plot(time_seconds, gas_mass, linestyle="--", label="Gas Mass [kg]")
    ax2.set_ylabel("Gas Mass [kg]")

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

    plt.title("Balloon Gas Density and Gas Mass History")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def save_temperature_history_png(
    time_seconds: np.ndarray,
    temperature: np.ndarray,
    output_path: Path,
) -> None:
    """温度履歴をPNG保存"""
    fig, ax = plt.subplots()

    ax.plot(time_seconds, temperature, label="Temperature [K]")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Temperature [K]")
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

    plt.title("Balloon Gas Temperature History")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
