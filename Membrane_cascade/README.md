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