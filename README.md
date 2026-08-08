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
- Reference and current aircraft weight
- Reference and current wing loading
- An inferred effective maximum lift coefficient
- A reference-vs-current maximum-lift comparison plot
- Required lift coefficient vs airspeed comparison
- CSV structure, value and source validation

## Installation and Use

Install the required Python packages from the project root:

```bash
python -m pip install -r requirements.txt
```

Run the current stable analysis:

```bash
python v1.0/aircraft_analyzer.py
```

The program reads the project data from `data/` and saves generated figures
under `plots/`.

Running the analysis does not modify the source CSV data files.

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

Python analysis version 1.0 is currently complete.

Version 0.7 compares the 500 g manufacturer reference aircraft with the
approximately 741 g current build estimate. It uses one shared maximum-lift
boundary inferred from manufacturer reference data and shows how the higher
required lift increases the estimated stall speed.

The inferred effective maximum lift coefficient is a modelling value derived
from manufacturer reference mass and stall speed. It is not measured LHK12
airfoil data.

Version 0.8 adds a required lift coefficient vs airspeed plot for both
aircraft masses. This shows that the heavier aircraft requires a higher lift
coefficient at the same airspeed and reaches the inferred maximum-lift limit
at a higher estimated stall speed.

Version 0.9 moves aircraft parameters into
`data/aircraft_parameters.csv`. Each parameter includes its value, unit and
source classification. Manufacturer reference data, modelling assumptions
and physical constants are therefore kept separate from the component mass
budget and from each other.

Version 1.0 adds validation for required CSV files, columns, parameters,
source classifications, mass status values and numerical inputs. Invalid data
now stops the analysis with a specific error instead of silently producing an
unreliable result. Dependency versions and run instructions are also included
for reproducibility.

Aircraft construction and measurement are still in progress.

Future work will include:

- Final aircraft mass measurement
- Component mass dataset
- Replacement of estimated component masses with final measurements
- Static thrust testing
- Current and power measurements
- Thrust-to-weight analysis
- Flight test documentation
- Final engineering report

