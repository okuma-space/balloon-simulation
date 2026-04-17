import sys
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

sys.path.append("./py")

from environment.atmosphere.isothermal_model import calculate_density


OUTPUT_DIR = Path("docs")

def main():
    # 15[km]まで100[m]ずつ計算する
    altitudes = np.linspace(0, 15000, 100)
    densities = [calculate_density(h) for h in altitudes]

    # Plotly（HTML）で保存する
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=densities, y=altitudes, mode="lines", name="Isothermal Model")
    )

    fig.update_layout(
        title="Isothermal Atmosphere Model",
        xaxis_title="Density [kg/m^3]",
        yaxis_title="Altitude [m]",
    )

    html_path = OUTPUT_DIR / "html/isothermal_density.html"
    fig.write_html(str(html_path), include_plotlyjs="cdn")

    # matplotlib（PNG）で保存する
    plt.figure()
    plt.plot(densities, altitudes)
    plt.title("Isothermal Atmosphere Model")
    plt.xlabel("Density [kg/m^3]")
    plt.ylabel("Altitude [m]")
    plt.grid(True)

    png_path = OUTPUT_DIR / "png/isothermal_density.png"
    plt.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close()

    # 出力
    print(f"saved: {html_path}")
    print(f"saved: {png_path}")


if __name__ == "__main__":
    main()
