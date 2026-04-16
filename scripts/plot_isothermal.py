import sys
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

sys.path.append("./py")

from environment.atmosphere.isothermal_model import calculate_density


OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    altitudes = np.linspace(0, 40000, 500)
    densities = [calculate_density(h) for h in altitudes]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=densities,
            y=altitudes,
            mode="lines",
            name="Isothermal Model"
        )
    )

    fig.update_layout(
        title="Isothermal Atmosphere Model",
        xaxis_title="Density [kg/m^3]",
        yaxis_title="Altitude [m]",
    )

    output_path = OUTPUT_DIR / "isothermal_density.html"
    fig.write_html(str(output_path))

    print(f"saved: {output_path}")


if __name__ == "__main__":
    main()