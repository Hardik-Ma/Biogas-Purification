import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
from scipy.interpolate import interp1d

# Conversion factor from Barrer to SI units (mol/m^2/s/Pa)
BARRER_TO_SI = 3.3464e-16

# FEED STREAM INPUT DATA FOR THE MEMBRANE (MEMBRANE_FEED_INPUT)
feed_composition = {
    'Hydrogen':0.180876223516669,
    'CarbonDioxide': 32.5682782016082,
    'Methane': 34.2618168715093
}

# Permeability data from the paper (MEMBRANE_PERMEABILITY_DATA)
permeability_biogas_constant = {
        'Hydrogen': 2.63*BARRER_TO_SI,
        'CarbonDioxide': 6.30*BARRER_TO_SI,
        'Methane': 0.21*BARRER_TO_SI
        }

def interpolate_permeability(x, x_data, y_data):
    """
    Function to interpolate permeability values based on the data provided.
    """
    return np.interp(x, x_data, y_data)


def simulate_membrane_module_partial_pressure_debug(
    feed_composition, feed_pressure, feed_temperature, permeability, membrane_area, stage_cut, membrane_thickness
):
    # Constants
    n_points = 1000  # Number of discretized steps
    dx = 1 / n_points  # Step size for discretization

    # Initialize pressures and flows
    feed_side_pressure = feed_pressure  # bar
    permeate_side_pressure = feed_pressure * (1 - stage_cut)  # bar
    total_feed_flow = sum(feed_composition.values())  # kmol/hr

    # Normalize feed composition to mole fractions
    feed_fraction = {comp: flow / total_feed_flow for comp, flow in feed_composition.items()}

    # Initialize flow rates and compositions
    retentate_flow = total_feed_flow
    permeate_flow = 0
    retentate_composition = feed_fraction.copy()
    permeate_composition = {comp: 0 for comp in feed_composition}

    # Data storage for plotting mole fractions
    mole_fraction_retentate = {comp: [] for comp in feed_composition}
    mole_fraction_permeate = {comp: [] for comp in feed_composition}

    # Discretized simulation loop
    for i in range(n_points):
        current_flow = retentate_flow
        current_fraction = retentate_composition

        permeation = {}
        for comp, y in current_fraction.items():
            # Partial pressure driving force
            p_feed = feed_side_pressure * y  # Partial pressure on feed side (bar)
            p_perm = permeate_side_pressure * permeate_composition.get(comp, 0)  # Partial pressure on permeate side (bar)
            driving_force = max(p_feed - p_perm, 0)  # Ensure non-negative driving force

            # Permeation flux calculation
            perm = permeability.get(comp, 0)  # Permeability (m³(STP)/m²/s/Pa)
            flux = (perm / membrane_thickness) * driving_force * 1e5  # Convert bar to Pa
            permeation[comp] = flux * membrane_area * dx  # Molar permeation rate (kmol/hr)

        # Debugging: Print permeation rates and driving forces
        if i == 0:  # Print only for the first iteration
            print(f"Component Permeation Rates (kmol/hr): {permeation}")
            print(f"Driving Forces (bar): { {comp: feed_side_pressure * y - permeate_side_pressure * permeate_composition.get(comp, 0) for comp, y in current_fraction.items()} }")

        # Total permeation flux
        total_permeation = sum(permeation.values())
        if total_permeation > current_flow:
            # Cap total permeation at the current retentate flow
            scale_factor = current_flow / total_permeation
            permeation = {comp: rate * scale_factor for comp, rate in permeation.items()}
            total_permeation = current_flow

        # Update flows
        permeate_flow += total_permeation
        retentate_flow -= total_permeation

        # Ensure retentate flow rate does not go below zero
        if retentate_flow < 0:
            retentate_flow = 0
            permeate_flow = total_feed_flow

        # Update permeate composition
        if permeate_flow > 0:
            for comp, rate in permeation.items():
                permeate_composition[comp] += rate / permeate_flow

        # Normalize permeate composition to ensure mole fractions
        if permeate_flow > 0:
            total_permeate_fraction = sum(permeate_composition.values())
            permeate_composition = {comp: x / total_permeate_fraction for comp, x in permeate_composition.items()}

        # Update retentate composition
        if retentate_flow > 0:
            for comp in current_fraction:
                retentate_composition[comp] -= permeation[comp] / retentate_flow

        # Normalize retentate composition to ensure mole fractions sum to 1
        if retentate_flow > 0:
            total_retentate_fraction = sum(retentate_composition.values())
            retentate_composition = {comp: x / total_retentate_fraction for comp, x in retentate_composition.items()}

        # Store mole fractions for plotting
        for comp in feed_composition:
            mole_fraction_retentate[comp].append(retentate_composition[comp])
            mole_fraction_permeate[comp].append(permeate_composition[comp])

    # Plotting mole fractions
    x = [i * dx for i in range(n_points)]  # Membrane position from 0 to 1
    plt.figure(figsize=(12, 8))
    for comp in feed_composition:
        plt.plot(x, mole_fraction_retentate[comp], label=f'{comp} (Retentate)', linestyle='--')
        plt.plot(x, mole_fraction_permeate[comp], label=f'{comp} (Permeate)', linestyle='-')
    plt.xlabel('Membrane Position')
    plt.ylabel('Mole Fraction')
    plt.title('Mole Fractions Across the Membrane')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Final outputs
    return {
        'feed_flow_rate': total_feed_flow,
        'retentate_flow_rate': retentate_flow,  # kmol/hr
        'permeate_flow_rate': permeate_flow,
        'retentate_composition': retentate_composition,  # mole fraction
        'permeate_composition': permeate_composition,
        'retentate_pressure': feed_side_pressure,  # bar
        'permeate_pressure': permeate_side_pressure,
    }


# Membrane Operating parameters (MEMBRANE_INPUT)
feed_pressure = 20  # bar
feed_temperature = 50 # Celsius
#membrane_area = 99000  # m^2
membrane_area = 99000  # m^2
stage_cut = 0.9

# Calculate the total molar flow rate
total_molar_flow_rate = sum(feed_composition.values())
print(total_molar_flow_rate)
# Calculate the mole fractions
mole_fractions = {component: flow_rate / total_molar_flow_rate for component, flow_rate in feed_composition.items()}

# Get permeability data
permeability = permeability_biogas_constant

results_DF_PP = simulate_membrane_module_partial_pressure_debug(
    feed_composition, feed_pressure, feed_temperature, permeability, membrane_area, stage_cut, 1e-6
)

# Extract relevant data
feed_flow_rate = results_DF_PP['feed_flow_rate']
retentate_flow_rate = results_DF_PP['retentate_flow_rate']
permeate_flow_rate = results_DF_PP['permeate_flow_rate']
retentate_composition = results_DF_PP['retentate_composition']
permeate_composition = results_DF_PP['permeate_composition']

print('feed_flow_rate')
print(feed_flow_rate)
print('ret_flow rate')
print(retentate_flow_rate)
print('perm_flow rate')
print(permeate_flow_rate)
print('ret composition')
print(retentate_composition)
print('perm comp')
print(permeate_composition)
