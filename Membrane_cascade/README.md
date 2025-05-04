# Biogas Membrane Cascade Simulation

Python implementation of a multi-stage membrane cascade for biogas purification, focusing on CH₄/CO₂ separation using hollow fiber membranes.

## Key Features
- Simulates **single membrane unit** behavior with partial pressure-driven permeation
- Handles **multi-component mixtures** (H₂, CO₂, CH₄)
- Outputs retentate/permeate flows and compositions
- Designed for **cascade integration** (MEMB-1 → MEMB-2 → MEMB-PUR)

## Theoretical Basis
This implementation is based on the solution-diffusion model described in:<br>
**Vrbova, V., & Ciahotny, K. (2017).** *Upgrading biogas to biomethane using membrane separation*. Energy & Fuels, 31(9), 9393-9401.<br>
DOI: 10.1021/acs.energyfuels.7b00120

### Key Equations:
1. **Permeation Flux**:  
   $$J_i = (P_i / δ) × (p_feed × y_i - p_perm × x_i)$$  
   Where:
   - `P_i` = Permeability (Barrer)
   - `δ` = Membrane thickness (μm)
   - `y_i`, `x_i` = Feed/permeate mole fractions

2. **Stage Cut**:  
   $$θ = Q_perm / Q_feed$$

## Process Flow
[Membrane Cascade Flowsheet](flowsheets/Membrane_Cascade.png)  
**Cascade Configuration**:
1. **MEMB-1**: Concentrates CH₄ in retentate (PBG-01), sends permeate to MEMB-2  
2. **MEMB-2**: Recovers residual CH₄ (PBG-04) from MEMB-1 permeate  
3. **MEMB-PUR**: Further purifies CH₄ (mixed PBG-01+PBG-04), vents CO₂ (WBG-02)  

## Code Structure
```python
membrane_model.py
├── Constants               # Permeability (Barrer), feed conditions
├── interpolate_permeability()  # For T-dependent properties (future use)
├── simulate_membrane_module_partial_pressure_debug()  # Core solver
├── Membrane_Unit_Specifications # Inputs for membrane unit
└── Main Execution          # Runs single-module simulation + plots
```

## Installation

### Prerequisites
- Python 3.x

### Dependencies
- Python 3.x
- Required libraries:
  - NumPy
  - SciPy
  - matplotlib
  - CoolProp


## Assumptions
1. **Isothermal operation** (T=50°C constant)
2. **Negligible retentate pressure drop** (Ideal hollow fiber)
3. **No cross-flow mixing** (plug flow assumed)
4. **Constant permeability**

## **Usage Instructions**
**Current Workflow (Single-Module Simulation)**<br>
This code simulates **one membrane unit** at a time. To model the full cascade:

1.**Sets Feed Composition**<br>
Modify the `MEMBRANE_FEED_INPUT` section with dehydrated biogas composition (output from the dehydration column): 
```python
# FEED STREAM INPUT DATA FOR THE MEMBRANE (MEMBRANE_FEED_INPUT)
feed_composition = {
    'Hydrogen':0.180876223516669, # Kmol/hr
    'CarbonDioxide': 32.5682782016082, #Kmol/hr
    'Methane': 34.2618168715093 #Kmol/hr
}
```
2. **Adjust Membrane Parameters**<br>
Tune in the `Membrane_INPUT` section to target desired CH₄ purity:
```python
# Membrane Operating parameters (MEMBRANE_INPUT)
feed_pressure = 20  # bar
feed_temperature = 50 # Celsius
membrane_area = 99000  # m^2
stage_cut = 0.9
```
3. **Run Simulation**<br>
```bash
python membrane_DF_PP_biogas_memb_1.py
```
4. **Cascade Implementation**<br>
Use the retentate and permete composition results from the first membrane to calculate the split fractions for **Aspen Plus** Flow sheet and use the retentate and permeate stream component molar flow data as input for the subsequent membranes:<br>

-**MEMB-2**<br>
The permeate stream composition from **MEMB-1** is used in the `MEMBRANE_FEED_INPUT` section.
```python
# Permeate stream composition of MEMB-1 (MEMBRANE_FEED_INPUT)
feed_composition = {
    'Hydrogen': ...,  #Kmol/hr
    'CarbonDioxide': ..., #Kmol/hr
    'Methane': ... #Kmol/hr
}
```

-**MEMB-PUR**<br>
Mixed **PBG-01** and **PBG-04** stream composition is used in the `MEMBRANE_FEED_INPUT` section.
```python
#  Mixed PBG-01+PBG-04 stream composition (MEMBRANE_FEED_INPUT)
feed_composition = {
    'Hydrogen': ...,  #Kmol/hr
    'CarbonDioxide': ..., #Kmol/hr
    'Methane': ... #Kmol/hr
}
```

5. **Optimization**<br>
Iteratively adjust `membrane_area` and `stage_cut` for each module to meet:
    - Target CH₄ purity in final retentate (e.g., >95%)
    - Minimal CH₄ loss in permeate vents

## Example Output
feed_flow rate<br>
67.01097129663417<br>
ret_flow rate<br>
24.709411913206534<br>
perm_flow rate<br>
42.301559383427744<br>
ret composition<br>
{'Hydrogen': 0.0004831376605370541, 'CarbonDioxide': 0.07641864719903857, 'Methane': 0.9230982151404243}<br>
perm comp<br>
{'Hydrogen': 0.0039873282696945705, 'CarbonDioxide': 0.7246277615169759, 'Methane': 0.2713849102133295}

## **Note**
- **Current Scope**: Single-module simulation with debug outputs
- **Future Work**:<br>
    -Dynamic cascade performance analysis<br>
    -Optimizer for `membrane_area` and `stage_cut`