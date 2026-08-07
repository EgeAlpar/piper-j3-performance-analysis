import csv
import math
from pathlib import Path

# -------------------------------------------------
# 3D-Printed Piper J-3 Cub Performance Analyzer
# Version 0.3
# -------------------------------------------------

# Manufacturer reference data
reference_mass_g = 500
reference_stall_speed_kmh = 15.0
max_takeoff_mass_g = 700
wing_area_dm2 = 18.15


# -------------------------------------------------
# FILE PATH
# -------------------------------------------------

project_root = Path(__file__).resolve().parent.parent
mass_budget_file = project_root / "data" / "mass_budget.csv"


# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------

def load_mass_budget(file_path):
    mass_data = []

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            component = row["component"]
            mass_g = float(row["mass_g"])
            status = row["status"]

            mass_data.append(
                {
                    "component": component,
                    "mass_g": mass_g,
                    "status": status
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


def calculate_takeoff_mass(measured_mass_g, estimated_mass_g):
    return measured_mass_g + estimated_mass_g


def calculate_wing_loading(takeoff_mass_g):
    return takeoff_mass_g / wing_area_dm2


def calculate_stall_speed(takeoff_mass_g):
    return reference_stall_speed_kmh * math.sqrt(
        takeoff_mass_g / reference_mass_g
    )


def calculate_mass_increase(takeoff_mass_g):
    return (
        (takeoff_mass_g - reference_mass_g)
        / reference_mass_g
    ) * 100


def calculate_mtow_difference(takeoff_mass_g):
    return takeoff_mass_g - max_takeoff_mass_g


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

mass_data = load_mass_budget(mass_budget_file)


# -------------------------------------------------
# CALCULATIONS
# -------------------------------------------------

measured_mass_g = calculate_measured_mass(mass_data)

estimated_mass_g = calculate_estimated_mass(mass_data)

takeoff_mass_g = calculate_takeoff_mass(
    measured_mass_g,
    estimated_mass_g
)

wing_loading_g_dm2 = calculate_wing_loading(takeoff_mass_g)

stall_speed_kmh = calculate_stall_speed(takeoff_mass_g)

mass_increase_percent = calculate_mass_increase(takeoff_mass_g)

mtow_difference_g = calculate_mtow_difference(takeoff_mass_g)


# -------------------------------------------------
# OUTPUT
# -------------------------------------------------

print("=" * 60)
print("3D-PRINTED PIPER J-3 CUB PERFORMANCE ANALYZER")
print("VERSION 0.3")
print("=" * 60)

print("\nMASS BUDGET")
print("-" * 60)

for item in mass_data:
    print(
        f"{item['component']:<20}"
        f"{item['mass_g']:>8.1f} g   "
        f"{item['status']}"
    )

print("\nMASS ANALYSIS")
print("-" * 60)

print(f"Measured mass subtotal:     {measured_mass_g:.1f} g")
print(f"Estimated mass subtotal:    {estimated_mass_g:.1f} g")
print(f"Estimated takeoff mass:     {takeoff_mass_g:.1f} g")

print("\nAIRCRAFT LIMITS")
print("-" * 60)

print(f"Manufacturer reference mass: {reference_mass_g:.0f} g")
print(f"Manufacturer MTOW:           {max_takeoff_mass_g:.0f} g")
print(f"Mass increase vs reference:  {mass_increase_percent:.1f} %")

if takeoff_mass_g > max_takeoff_mass_g:
    print(
        f"WARNING: Estimated aircraft mass is "
        f"{mtow_difference_g:.1f} g above manufacturer MTOW."
    )
else:
    print(
        f"Aircraft is "
        f"{abs(mtow_difference_g):.1f} g below manufacturer MTOW."
    )

print("\nAERODYNAMIC ESTIMATES")
print("-" * 60)

print(f"Wing area:                   {wing_area_dm2:.2f} dm^2")
print(f"Wing loading:                {wing_loading_g_dm2:.2f} g/dm^2")
print(f"Reference stall speed:       {reference_stall_speed_kmh:.2f} km/h")
print(f"Estimated stall speed:       {stall_speed_kmh:.2f} km/h")

print("\nDATA SOURCE")
print("-" * 60)

print(f"Mass budget file: {mass_budget_file}")

print("\nNOTE")
print("-" * 60)

print(
    "Stall speed is estimated by assuming the same aerodynamic "
    "configuration and maximum lift coefficient as the reference aircraft."
)