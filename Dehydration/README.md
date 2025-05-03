# Biogas Dehydration Column Simulation

Python implementation of an adsorption-based dehydration column for biogas purification, simulating water content removal using silica gel.

## Key Features
- Calculates component adsorption (H₂O, CO₂) using **Virial isotherm model**
- Handles real-gas behaviour through **temperature-dependent coefficients**
- Outputs adsorbed amounts and purified biogas composition
- Designed for integration with Aspen Plus via split fractions

### Key Equation Implemented:
1. **Viral Isotherm**:
   $$P = (q/k_i) * exp(A·q + B·q² + C·q³)$$
   Where:
   - `q` = adsorbed amount (kmol/kg)
   - `A,B,C` = temperature-dependent coefficients
   - `k_i` = component-specific affinity constant

2. **Partial Pressure**:
    $$P_i = (y_i) * P_total$$
    (where `y_i` is mole fraction)

## Code Structure
```python
dehydration_model.py
├── Constants            # R, feed_composition, operating conditions
├── Virial Coefficients  # A,B,C for CO₂/H₂O (temperature-dependent)
├── calculate_ABC()      # Computes A,B,C for given component
├── adsorption_equation()# Solves Virial isotherm numerically
└── Main Execution       # Calculates adsorbed amounts & outlet composition

```

## Example Output
Adsorbed Amounts (kmol):
{'CO2': 12.45, 'H2O': 1.52}

Outlet Composition (kmol/hr):
{'CO2': 20.12, 'H2O': 0.06}

## Assumptions:
1. **Isothermal operation** (T = 50°C constant)
2. **Ideal gas mixture** for partial pressure calculations
3. **Negligable mass transfer resistance** (instant equilibrium)
4. **No competative adsorption** (components treated independeltly)
