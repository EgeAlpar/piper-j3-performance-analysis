import csv
import math
from pathlib import Path

# -------------------------------------------------
# 3D-Printed Piper J-3 Cub Performance Analyzer
# Version 0.4
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


def calculate_weight_newtons(mass_g):
    mass_kg = mass_g / 1000
    return mass_kg * gravity_m_s2


def kmh_to_ms(speed_kmh):
    return speed_kmh / 3.6


def calculate_dynamic_pressure(speed_ms):
    return 0.5 * air_density_kg_m3 * speed_ms ** 2


def calculate_lift(speed_ms, wing_area_m2, lift_coefficient):
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

mass_data = load_mass_budget(mass_budget_file)


# -------------------------------------------------
# MASS CALCULATIONS
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

aircraft_weight_n = calculate_weight_newtons(takeoff_mass_g)


# -------------------------------------------------
# UNIT CONVERSIONS
# -------------------------------------------------

wing_area_m2 = wing_area_dm2 / 100


# -------------------------------------------------
# AIRSPEED ANALYSIS
# -------------------------------------------------

airspeeds_kmh = [
    10,
    15,
    20,
    25,
    30,
    35,
    40
]


# -------------------------------------------------
# OUTPUT
# -------------------------------------------------

print("=" * 65)
print("3D-PRINTED PIPER J-3 CUB PERFORMANCE ANALYZER")
print("VERSION 0.4")
print("=" * 65)

print("\nMASS ANALYSIS")
print("-" * 65)

print(f"Measured mass subtotal:      {measured_mass_g:.1f} g")
print(f"Estimated mass subtotal:     {estimated_mass_g:.1f} g")
print(f"Estimated takeoff mass:      {takeoff_mass_g:.1f} g")
print(f"Aircraft weight:             {aircraft_weight_n:.2f} N")

print("\nAIRCRAFT LIMITS")
print("-" * 65)

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
print("-" * 65)

print(f"Wing area:                   {wing_area_m2:.4f} m^2")
print(f"Wing loading:                {wing_loading_g_dm2:.2f} g/dm^2")
print(f"Reference stall speed:       {reference_stall_speed_kmh:.2f} km/h")
print(f"Estimated stall speed:       {stall_speed_kmh:.2f} km/h")

print("\nLIFT ANALYSIS")
print("-" * 65)

print(
    f"{'Speed':>10}"
    f"{'Speed':>12}"
    f"{'Dyn. Pressure':>18}"
    f"{'Lift':>12}"
)

print(
    f"{'(km/h)':>10}"
    f"{'(m/s)':>12}"
    f"{'(Pa)':>18}"
    f"{'(N)':>12}"
)

print("-" * 65)

for speed_kmh in airspeeds_kmh:
    speed_ms = kmh_to_ms(speed_kmh)

    dynamic_pressure_pa = calculate_dynamic_pressure(
        speed_ms
    )

    lift_n = calculate_lift(
        speed_ms,
        wing_area_m2,
        lift_coefficient
    )

    print(
        f"{speed_kmh:>10.1f}"
        f"{speed_ms:>12.2f}"
        f"{dynamic_pressure_pa:>18.2f}"
        f"{lift_n:>12.2f}"
    )

print("\nASSUMPTIONS")
print("-" * 65)

print(f"Air density:                 {air_density_kg_m3:.3f} kg/m^3")
print(f"Lift coefficient used:       {lift_coefficient:.2f}")

print(
    "\nLift values are theoretical estimates calculated "
    "using a constant lift coefficient."
)

print(
    "They do not represent measured aircraft lift or "
    "the actual lift coefficient of the LHK12 airfoil."
)