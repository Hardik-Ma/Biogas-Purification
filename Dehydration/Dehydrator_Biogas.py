import numpy as np
from scipy.optimize import fsolve

# Constants
R = 8.314  # Universal gas constant (J/mol·K)

# Input data
feed_composition = {'CO2': 32.5683, 'H2O': 1.5854}  # kmol/hr
temperature_C = 50  # Temperature in °C
pressure_bar = 20  # Pressure in bar
desiccant_mass = 9450  # kg

# Convert temperature from °C to K
temperature_K = temperature_C + 273.15

# Convert pressure from bar to kPa
pressure_kPa = pressure_bar * 100  # 1 bar = 100 kPa

# Adsorption equilibrium constants (example values)
k_i = {
    #'CH4': 2.4e-6,  # 1/kPa
    'CO2': 5e-7,  # 1/kPa
    'H2O': 1.8e-6   # 1/kPa
}

# Virial coefficients (example values)
coefficients = {
    #'CH4': {'A0': 0, 'A1': 0, 'B0': 0, 'B1': 0, 'C0': 0, 'C1': 0},  # CH4
    'CO2': {'A0': 0.119, 'A1': 92.830, 'B0': -3.5e-2, 'B1': 3.8, 'C0': 0, 'C1': 0},  # CO2
    'H2O': {'A0': 0.357, 'A1': -8.254, 'B0': -8.5e-3, 'B1': -8.520, 'C0': -5.71e-4, 'C1': 0.421}   # H2O
}

# Function to calculate A, B, C
def calculate_ABC(component, T):
    A0 = coefficients[component]['A0']
    A1 = coefficients[component]['A1']
    B0 = coefficients[component]['B0']
    B1 = coefficients[component]['B1']
    C0 = coefficients[component]['C0']
    C1 = coefficients[component]['C1']
    
    A = A0 + (A1 / T)
    B = B0 + (B1 / T)
    C = C0 + (C1 / T)
    
    return A, B, C

# Function to solve for q
def adsorption_equation(q, P, k_i, A, B, C):
    return P - (q / k_i) * np.exp(A * q + B * q**2 + C * q**3)

# Calculate partial pressures
total_molar_flow = sum(feed_composition.values())  # kmol/hr
partial_pressures = {component: (flow_rate / total_molar_flow) * pressure_kPa for component, flow_rate in feed_composition.items()}

# Calculate adsorption for each component
adsorbed_amounts = {}
for component, P in partial_pressures.items():
    A, B, C = calculate_ABC(component, temperature_K)
    k_i_component = k_i[component]
    
    # Initial guess for q
    q_guess = 0.01  # kmol/kg
    # Solve the adsorption equation for q
    q = fsolve(adsorption_equation, q_guess, args=(P, k_i_component, A, B, C))[0]
    adsorbed_amounts[component] = q * desiccant_mass  # kmol

# Update outlet composition
outlet_composition = feed_composition.copy()
for component, amount in adsorbed_amounts.items():
    outlet_composition[component] -= amount

# Output results
print("Adsorbed Amounts (kmol):", adsorbed_amounts)
print("Outlet Composition (kmol/hr):", outlet_composition)