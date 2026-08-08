import csv
import math
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# 3D-Printed Piper J-3 Cub Performance Analyzer
# Version 0.9
# -------------------------------------------------

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

comparison_plot_file = (
    plots_folder
    / "reference_vs_current_lift.png"
)

aircraft_parameters_file = (
    project_root
    / "data"
    / "aircraft_parameters.csv"
)

required_cl_plot_file = (
    plots_folder
    / "required_cl_vs_airspeed.png"
)


# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------

def load_aircraft_parameters(file_path):
    parameters = {}

    with open(
        file_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            parameters[row["parameter"]] = {
                "value": float(row["value"]),
                "unit": row["unit"],
                "source": row["source"]
            }

    return parameters

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


def calculate_inferred_max_lift_coefficient(
    reference_weight_n,
    reference_stall_speed_ms,
    wing_area_m2
):
    """Infer an effective CL_max from manufacturer reference data."""

    return (
        2
        * reference_weight_n
        / (
            air_density_kg_m3
            * reference_stall_speed_ms ** 2
            * wing_area_m2
        )
    )


def calculate_required_lift_coefficient(
    aircraft_weight_n,
    speed_ms,
    wing_area_m2
):
    """Calculate the CL required for steady level flight."""

    return (
        2
        * aircraft_weight_n
        / (
            air_density_kg_m3
            * speed_ms ** 2
            * wing_area_m2
        )
    )


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

aircraft_parameters = load_aircraft_parameters(
    aircraft_parameters_file
)

reference_mass_g = aircraft_parameters[
    "reference_mass_g"
]["value"]

reference_stall_speed_kmh = aircraft_parameters[
    "reference_stall_speed_kmh"
]["value"]

max_takeoff_mass_g = aircraft_parameters[
    "max_takeoff_mass_g"
]["value"]

wing_area_dm2 = aircraft_parameters[
    "wing_area_dm2"
]["value"]

air_density_kg_m3 = aircraft_parameters[
    "air_density_kg_m3"
]["value"]

gravity_m_s2 = aircraft_parameters[
    "gravity_m_s2"
]["value"]

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

reference_wing_loading_g_dm2 = (
    calculate_wing_loading(
        reference_mass_g
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

reference_weight_n = (
    calculate_weight_newtons(
        reference_mass_g
    )
)


# -------------------------------------------------
# UNIT CONVERSIONS
# -------------------------------------------------

wing_area_m2 = (
    wing_area_dm2
    / 100
)

reference_stall_speed_ms = kmh_to_ms(
    reference_stall_speed_kmh
)

inferred_max_lift_coefficient = (
    calculate_inferred_max_lift_coefficient(
        reference_weight_n,
        reference_stall_speed_ms,
        wing_area_m2
    )
)


# -------------------------------------------------
# NUMPY AIRSPEED ANALYSIS
# -------------------------------------------------

airspeeds_kmh = np.arange(10, 30.25, 0.25)

airspeeds_ms = kmh_to_ms(
    airspeeds_kmh
)

maximum_lift_n = calculate_lift(
    airspeeds_ms,
    wing_area_m2,
    inferred_max_lift_coefficient
)

reference_required_cl = calculate_required_lift_coefficient(
    reference_weight_n,
    airspeeds_ms,
    wing_area_m2
)

current_required_cl = calculate_required_lift_coefficient(
    aircraft_weight_n,
    airspeeds_ms,
    wing_area_m2
)


# -------------------------------------------------
# OUTPUT
# -------------------------------------------------

print("=" * 70)

print(
    "3D-PRINTED PIPER J-3 CUB "
    "PERFORMANCE ANALYZER"
)

print("VERSION 0.9")

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

print(
    f"Reference aircraft weight:   "
    f"{reference_weight_n:.2f} N"
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
    f"Current wing loading:        "
    f"{wing_loading_g_dm2:.2f} g/dm^2"
)

print(
    f"Reference wing loading:      "
    f"{reference_wing_loading_g_dm2:.2f} g/dm^2"
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
    maximum_lift_n,
    linewidth=2,
    label="Inferred Maximum-Lift Boundary"
)

plt.axhline(
    y=reference_weight_n,
    color="tab:green",
    linestyle="--",
    label="Reference Weight - 500 g (Manufacturer)"
)

plt.axhline(
    y=aircraft_weight_n,
    color="tab:red",
    linestyle="--",
    label="Current Weight - 741 g (Estimated)"
)

plt.axvline(
    x=reference_stall_speed_kmh,
    color="tab:green",
    linestyle=":",
    label="Reference Stall Speed - 15 km/h (Manufacturer)"
)

plt.axvline(
    x=stall_speed_kmh,
    color="tab:red",
    linestyle=":",
    label=f"Current Stall Speed - {stall_speed_kmh:.2f} km/h (Estimated)"
)

plt.scatter(
    [reference_stall_speed_kmh],
    [reference_weight_n],
    color="tab:green",
    zorder=5
)

plt.scatter(
    [stall_speed_kmh],
    [aircraft_weight_n],
    color="tab:red",
    zorder=5
)

plt.xlabel(
    "Airspeed (km/h)"
)

plt.ylabel(
    "Lift (N)"
)

plt.title(
    "Reference vs Current Aircraft - Maximum-Lift Comparison"
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    comparison_plot_file,
    dpi=300
)

plt.show()


# -------------------------------------------------
# REQUIRED LIFT COEFFICIENT PLOT
# -------------------------------------------------

plt.figure(figsize=(9, 6))

plt.plot(
    airspeeds_kmh,
    reference_required_cl,
    color="tab:green",
    linewidth=2,
    label="Reference Aircraft - 500 g (Manufacturer)"
)

plt.plot(
    airspeeds_kmh,
    current_required_cl,
    color="tab:red",
    linewidth=2,
    label="Current Aircraft - 741 g (Estimated)"
)

plt.axhline(
    y=inferred_max_lift_coefficient,
    color="tab:blue",
    linestyle="--",
    label=f"Inferred Effective CL_max = {inferred_max_lift_coefficient:.2f}"
)

plt.scatter(
    [reference_stall_speed_kmh],
    [inferred_max_lift_coefficient],
    color="tab:green",
    zorder=5
)

plt.scatter(
    [stall_speed_kmh],
    [inferred_max_lift_coefficient],
    color="tab:red",
    zorder=5
)

plt.xlabel("Airspeed (km/h)")
plt.ylabel("Required Lift Coefficient, CL")

plt.title(
    "Required Lift Coefficient vs Airspeed - Reference and Current Aircraft"
)

plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    required_cl_plot_file,
    dpi=300
)

plt.show()


# -------------------------------------------------
# FINAL INFORMATION
# -------------------------------------------------

print("\nPLOT GENERATED")
print("-" * 70)

print(
    f"Saved to: {comparison_plot_file}"
)

print(
    f"Saved to: {required_cl_plot_file}"
)


print("\nASSUMPTIONS")
print("-" * 70)

print(
    f"Air density:                 "
    f"{air_density_kg_m3:.3f} kg/m^3"
)

print(
    f"Inferred effective CL_max:   "
    f"{inferred_max_lift_coefficient:.2f}"
)

print(
    "\nThe maximum-lift boundary uses an effective CL_max "
    "inferred from manufacturer reference data."
)

print(
    "The same aerodynamic boundary is used for both masses; "
    "mass changes the required lift, not the lift equation."
)

print(
    "The inferred effective CL_max is derived from the "
    "manufacturer reference mass and stall speed."
)

print(
    "It is not a measured lift coefficient for the "
    "LHK12 airfoil."
)

print(
    "Required CL values above the inferred CL_max indicate "
    "that steady level flight is not supported by this model."
)

print("\nDATA SOURCES")
print("-" * 70)

print(f"Mass budget:                 {mass_budget_file}")
print(f"Aircraft parameters:         {aircraft_parameters_file}")

print(
    "Parameter sources are classified as manufacturer, "
    "modelling_assumption or physical_constant."
)
