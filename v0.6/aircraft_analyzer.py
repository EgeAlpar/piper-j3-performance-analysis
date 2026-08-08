import csv
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# 3D-Printed Piper J-3 Cub Performance Analyzer
# Version 0.6
# -------------------------------------------------

# Manufacturer reference data
reference_mass_g = 500
reference_stall_speed_kmh = 15.0
max_takeoff_mass_g = 700
wing_area_dm2 = 18.15

# Aerodynamic constants
air_density_kg_m3 = 1.225
gravity_m_s2 = 9.81

# Assumed lift coefficient for basic comparison
lift_coefficient = 1.0


# -------------------------------------------------
# FILE PATHS
# -------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

mass_budget_file = (
    project_root
    / "data"
    / "mass_budget.csv"
)

plots_folder = (
    project_root
    / "plots"
)

plots_folder.mkdir(exist_ok=True)

lift_plot_file = (
    plots_folder
    / "lift_vs_airspeed.png"
)


# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------

def load_mass_budget(file_path):
    mass_data = []

    with open(
        file_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            mass_data.append(
                {
                    "component": row["component"],
                    "mass_g": float(row["mass_g"]),
                    "status": row["status"]
                }
            )

    return mass_data


def calculate_measured_mass(mass_data):
    total = 0

    for item in mass_data:
        if item["status"] == "measured":
            total += item["mass_g"]

    return total


def calculate_estimated_mass(mass_data):
    total = 0

    for item in mass_data:
        if item["status"] == "estimated":
            total += item["mass_g"]

    return total


def calculate_takeoff_mass(
    measured_mass_g,
    estimated_mass_g
):
    return measured_mass_g + estimated_mass_g


def calculate_wing_loading(takeoff_mass_g):
    return takeoff_mass_g / wing_area_dm2


def calculate_stall_speed(takeoff_mass_g):
    return (
        reference_stall_speed_kmh
        * math.sqrt(
            takeoff_mass_g
            / reference_mass_g
        )
    )


def calculate_mass_increase(takeoff_mass_g):
    return (
        (
            takeoff_mass_g
            - reference_mass_g
        )
        / reference_mass_g
    ) * 100


def calculate_mtow_difference(takeoff_mass_g):
    return (
        takeoff_mass_g
        - max_takeoff_mass_g
    )


def calculate_weight_newtons(mass_g):
    mass_kg = mass_g / 1000

    return (
        mass_kg
        * gravity_m_s2
    )


def kmh_to_ms(speed_kmh):
    return speed_kmh / 3.6


def calculate_dynamic_pressure(speed_ms):
    return (
        0.5
        * air_density_kg_m3
        * speed_ms ** 2
    )


def calculate_lift(
    speed_ms,
    wing_area_m2,
    lift_coefficient
):
    return (
        0.5
        * air_density_kg_m3
        * speed_ms ** 2
        * wing_area_m2
        * lift_coefficient
    )


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

mass_data = load_mass_budget(
    mass_budget_file
)


# -------------------------------------------------
# MASS CALCULATIONS
# -------------------------------------------------

measured_mass_g = (
    calculate_measured_mass(
        mass_data
    )
)

estimated_mass_g = (
    calculate_estimated_mass(
        mass_data
    )
)

takeoff_mass_g = (
    calculate_takeoff_mass(
        measured_mass_g,
        estimated_mass_g
    )
)

wing_loading_g_dm2 = (
    calculate_wing_loading(
        takeoff_mass_g
    )
)

stall_speed_kmh = (
    calculate_stall_speed(
        takeoff_mass_g
    )
)

mass_increase_percent = (
    calculate_mass_increase(
        takeoff_mass_g
    )
)

mtow_difference_g = (
    calculate_mtow_difference(
        takeoff_mass_g
    )
)

aircraft_weight_n = (
    calculate_weight_newtons(
        takeoff_mass_g
    )
)


# -------------------------------------------------
# UNIT CONVERSIONS
# -------------------------------------------------

wing_area_m2 = (
    wing_area_dm2
    / 100
)


# -------------------------------------------------
# NUMPY AIRSPEED ANALYSIS
# -------------------------------------------------

airspeeds_kmh = np.arange(
    10,
    45,
    1
)

airspeeds_ms = kmh_to_ms(
    airspeeds_kmh
)

dynamic_pressure_pa = (
    calculate_dynamic_pressure(
        airspeeds_ms
    )
)

lift_n = calculate_lift(
    airspeeds_ms,
    wing_area_m2,
    lift_coefficient
)


# -------------------------------------------------
# OUTPUT
# -------------------------------------------------

print("=" * 70)

print(
    "3D-PRINTED PIPER J-3 CUB "
    "PERFORMANCE ANALYZER"
)

print("VERSION 0.6")

print("=" * 70)


print("\nMASS ANALYSIS")
print("-" * 70)

print(
    f"Measured mass subtotal:      "
    f"{measured_mass_g:.1f} g"
)

print(
    f"Estimated mass subtotal:     "
    f"{estimated_mass_g:.1f} g"
)

print(
    f"Estimated takeoff mass:      "
    f"{takeoff_mass_g:.1f} g"
)

print(
    f"Aircraft weight:             "
    f"{aircraft_weight_n:.2f} N"
)


print("\nAIRCRAFT LIMITS")
print("-" * 70)

print(
    f"Manufacturer reference mass: "
    f"{reference_mass_g:.0f} g"
)

print(
    f"Manufacturer MTOW:           "
    f"{max_takeoff_mass_g:.0f} g"
)

print(
    f"Mass increase vs reference:  "
    f"{mass_increase_percent:.1f} %"
)


if takeoff_mass_g > max_takeoff_mass_g:

    print(
        f"WARNING: Estimated aircraft mass is "
        f"{mtow_difference_g:.1f} g "
        f"above manufacturer MTOW."
    )

else:

    print(
        f"Aircraft is "
        f"{abs(mtow_difference_g):.1f} g "
        f"below manufacturer MTOW."
    )


print("\nAERODYNAMIC ESTIMATES")
print("-" * 70)

print(
    f"Wing area:                   "
    f"{wing_area_m2:.4f} m^2"
)

print(
    f"Wing loading:                "
    f"{wing_loading_g_dm2:.2f} g/dm^2"
)

print(
    f"Reference stall speed:       "
    f"{reference_stall_speed_kmh:.2f} km/h"
)

print(
    f"Estimated stall speed:       "
    f"{stall_speed_kmh:.2f} km/h"
)


# -------------------------------------------------
# MATPLOTLIB PLOT
# -------------------------------------------------

plt.figure(figsize=(9, 6))

plt.plot(
    airspeeds_kmh,
    lift_n,
    label="Calculated Lift"
)

plt.axhline(
    y=aircraft_weight_n,
    linestyle="--",
    label="Aircraft Weight"
)

plt.axvline(
    x=stall_speed_kmh,
    linestyle="--",
    label="Estimated Stall Speed"
)

plt.xlabel(
    "Airspeed (km/h)"
)

plt.ylabel(
    "Lift (N)"
)

plt.title(
    "Lift vs Airspeed - Piper J-3 Cub"
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    lift_plot_file,
    dpi=300
)

plt.show()


# -------------------------------------------------
# FINAL INFORMATION
# -------------------------------------------------

print("\nPLOT GENERATED")
print("-" * 70)

print(
    f"Saved to: {lift_plot_file}"
)


print("\nASSUMPTIONS")
print("-" * 70)

print(
    f"Air density:                 "
    f"{air_density_kg_m3:.3f} kg/m^3"
)

print(
    f"Lift coefficient used:       "
    f"{lift_coefficient:.2f}"
)

print(
    "\nLift calculations use a constant "
    "assumed lift coefficient."
)

print(
    "The plotted lift curve does not represent "
    "measured aerodynamic data."
)