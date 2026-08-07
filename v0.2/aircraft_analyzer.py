import math

# -------------------------------------------------
# 3D-Printed Piper J-3 Cub Performance Analyzer
# Version 0.2
# -------------------------------------------------

# Manufacturer reference data
reference_mass_g = 500
reference_stall_speed_kmh = 15.0
max_takeoff_mass_g = 700
wing_area_dm2 = 18.15

# Our aircraft - measured masses
printed_airframe_g = 377
motor_g = 63
esc_g = 40
servos_g = 60
receiver_g = 15
propeller_g = 11
landing_gear_g = 13
battery_g = 115

# Estimated components
wheels_g = 20
pushrods_g = 15
glue_g = 12


# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------

def calculate_known_mass():
    return (
        printed_airframe_g
        + motor_g
        + esc_g
        + servos_g
        + receiver_g
        + propeller_g
        + landing_gear_g
        + battery_g
    )


def calculate_estimated_extra_mass():
    return (
        wheels_g
        + pushrods_g
        + glue_g
    )


def calculate_takeoff_mass():
    known_mass = calculate_known_mass()
    estimated_extra_mass = calculate_estimated_extra_mass()

    return known_mass + estimated_extra_mass


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
# CALCULATIONS
# -------------------------------------------------

known_mass_g = calculate_known_mass()

estimated_extra_mass_g = calculate_estimated_extra_mass()

takeoff_mass_g = calculate_takeoff_mass()

wing_loading_g_dm2 = calculate_wing_loading(takeoff_mass_g)

stall_speed_kmh = calculate_stall_speed(takeoff_mass_g)

mass_increase_percent = calculate_mass_increase(takeoff_mass_g)

mtow_difference_g = calculate_mtow_difference(takeoff_mass_g)


# -------------------------------------------------
# OUTPUT
# -------------------------------------------------

print("=" * 50)
print("3D-PRINTED PIPER J-3 CUB PERFORMANCE ANALYZER")
print("VERSION 0.2")
print("=" * 50)

print("\nMASS ANALYSIS")
print("-" * 50)

print(f"Known measured mass:       {known_mass_g:.1f} g")
print(f"Estimated additional mass: {estimated_extra_mass_g:.1f} g")
print(f"Estimated takeoff mass:     {takeoff_mass_g:.1f} g")

print("\nAIRCRAFT LIMITS")
print("-" * 50)

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
print("-" * 50)

print(f"Wing area:                  {wing_area_dm2:.2f} dm^2")
print(f"Wing loading:               {wing_loading_g_dm2:.2f} g/dm^2")
print(f"Reference stall speed:      {reference_stall_speed_kmh:.2f} km/h")
print(f"Estimated stall speed:      {stall_speed_kmh:.2f} km/h")

print("\nNOTE")
print("-" * 50)

print(
    "Stall speed is estimated by assuming the same aerodynamic "
    "configuration and maximum lift coefficient as the reference aircraft."
)