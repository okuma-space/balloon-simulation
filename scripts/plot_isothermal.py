from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from environment.atmosphere.isothermal_model import calculate_density


OUTPUT_DIR = Path("docs")


def run_isothermal_density_simulation() -> tuple[np.ndarray, np.ndarray]:
    """等温大気モデルによる密度を計算するシミュレーションを実行し、高度と密度の配列を返す。"""
    # 15[km]まで100[m]ずつ計算する
    altitudes = np.linspace(0, 15000, 100)
    densities = np.array([calculate_density(h) for h in altitudes])
    return altitudes, densities


def save_density_html(
    altitudes: np.ndarray, densities: np.ndarray, output_path: Path
) -> None:
    """高度と密度の配列をプロットしてHTMLファイルに保存。"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=densities, y=altitudes, mode="lines", name="Isothermal Model")
    )
    fig.update_layout(
        title="Isothermal Atmosphere Model",
        xaxis_title="Density [kg/m^3]",
        yaxis_title="Altitude [m]",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def save_density_png(
    altitudes: np.ndarray, densities: np.ndarray, output_path: Path
) -> None:
    """高度と密度の配列をプロットしてPNGファイルに保存。"""
    plt.figure()
    plt.plot(densities, altitudes)
    plt.title("Isothermal Atmosphere Model")
    plt.xlabel("Density [kg/m^3]")
    plt.ylabel("Altitude [m]")
    plt.grid(True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()


def main():
    # シミュレーション実行
    altitudes, densities = run_isothermal_density_simulation()

    html_path = OUTPUT_DIR / "html/isothermal_density.html"
    png_path = OUTPUT_DIR / "png/isothermal_density.png"

    # htmlとpngを保存
    save_density_html(altitudes, densities, html_path)
    save_density_png(altitudes, densities, png_path)

    print(f"saved: {html_path}")
    print(f"saved: {png_path}")


if __name__ == "__main__":
    main()
