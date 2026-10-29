"""
generate_sky_map.py
Reads an observational CSV log and renders a polar sky dome projection map.
Requires: pandas, matplotlib, numpy
Run: python3 generate_sky_map.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CSV_FILE = "astronomy_sky_log_template.csv"
OUTPUT_IMAGE = "my_sky_map.png"

def plot_sky_map():
    df = pd.read_csv(CSV_FILE)
    
    # Filter rows with valid numerical Alt and Az
    df = df.dropna(subset=["altitude_deg", "azimuth_deg"])
    df["altitude_deg"] = pd.to_numeric(df["altitude_deg"], errors="coerce")
    df["azimuth_deg"] = pd.to_numeric(df["azimuth_deg"], errors="coerce")
    df = df.dropna(subset=["altitude_deg", "azimuth_deg"])

    if df.empty:
        print("No valid coordinates found in CSV to plot.")
        return

    # Setup polar figure (dark night theme)
    fig = plt.figure(figsize=(9, 9), facecolor="#0d1117")
    ax = fig.add_subplot(111, polar=True, facecolor="#161b22")

    # Set orientation: 0 deg at North, running clockwise (N -> E -> S -> W)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    # In polar plots, radius r = 0 is center (Zenith = 90 deg alt), r = 90 is horizon (0 deg alt)
    r = 90 - df["altitude_deg"]
    theta = np.radians(df["azimuth_deg"])

    # Scatter targets
    ax.scatter(theta, r, c="#58a6ff", s=110, edgecolors="#ffffff", linewidth=0.8, zorder=5)

    # Label each target
    for _, row in df.iterrows():
        name = str(row["target_name"])
        t_r = 90 - float(row["altitude_deg"])
        t_th = np.radians(float(row["azimuth_deg"]))
        ax.annotate(
            name,
            xy=(t_th, t_r),
            xytext=(6, 6),
            textcoords="offset points",
            color="#c9d1d9",
            fontsize=9,
            weight="bold"
        )

    # Rings and angle labels
    ax.set_ylim(0, 90)
    ax.set_yticks([0, 30, 60, 90])
    ax.set_yticklabels(['90° (Zenith)', '60°', '30°', '0° (Horizon)'], color="#8b949e", fontsize=9)
    ax.set_xticks(np.radians([0, 45, 90, 135, 180, 225, 270, 315]))
    ax.set_xticklabels(['N (0°)', 'NE', 'E (90°)', 'SE', 'S (180°)', 'SW', 'W (270°)', 'NW'], color="#c9d1d9", fontsize=11, weight="bold")

    ax.grid(color="#30363d", linestyle="--", linewidth=0.8)
    ax.spines['polar'].set_color('#30363d')

    plt.title("Sky Dome Observation Map\n", color="#f0f6fc", fontsize=14, weight="bold")
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, dpi=200, facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"Map successfully rendered and saved to {OUTPUT_IMAGE}")

if __name__ == "__main__":
    plot_sky_map()
