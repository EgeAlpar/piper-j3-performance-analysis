# 3D-Printed Piper J-3 Cub Performance Analysis

## Project Objective

This project investigates how the increased manufacturing mass of a
3D-printed Piper J-3 Cub RC aircraft affects basic flight performance.

The aircraft is based on the 3DLabPrint Piper J-3 Cub design and is
manufactured using pre-foamed LW-PLA.

The main objective is to compare the manufactured aircraft with the
manufacturer reference configuration using mass analysis, aerodynamic
estimation, propulsion testing and flight testing.

## Aircraft Reference Data

- Wingspan: 1068 mm
- Wing area: 18.15 dm²
- Manufacturer reference takeoff mass: 500 g
- Manufacturer maximum takeoff mass: 700 g
- Manufacturer stall speed: 15 km/h
- Recommended CG: 44 mm from leading edge

## Current Build

- Printed airframe mass: 377 g
- Current estimated takeoff mass: 741 g
- Motor: SunnySky X2212 980KV
- Battery: 3S 1300mAh LiPo
- Propeller: 8x4 three-blade

The current takeoff mass is an estimate and will be replaced by a
measured final aircraft mass after assembly is completed.

## Python Analysis

The current Python tool calculates:

- Known measured mass
- Estimated additional mass
- Estimated takeoff mass
- Wing loading
- Mass increase compared with reference aircraft
- MTOW difference
- Estimated stall speed

Current calculated results:

- Estimated takeoff mass: 741 g
- Wing loading: 40.83 g/dm²
- Estimated stall speed: 18.26 km/h
- Mass increase compared with reference: 48.2%

## Project Methodology

Manufacture → Measure → Model → Test → Compare → Improve

Planned project phases:

1. Mass analysis
2. Aerodynamic analysis
3. Propulsion testing
4. CG and pre-flight verification
5. Flight testing
6. Comparison with manufacturer reference data
7. Performance evaluation and possible improvements

## Current Status

Python analysis version 0.2 is currently complete.

Aircraft construction and measurement are still in progress.

Future work will include:

- Final aircraft mass measurement
- Component mass dataset
- Lift calculations
- Lift vs airspeed plots
- Static thrust testing
- Current and power measurements
- Thrust-to-weight analysis
- Flight test documentation
- Final engineering report

