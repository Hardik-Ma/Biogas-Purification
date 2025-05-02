# Biogas-Purification
Python simulations for biogas purification from wheat straw waste, including a dehydration column and membrane cascade. Generates split fractions for Aspen Plus when native tools are insufficient. Part of a larger biorefinery feasibility study.

## Why python
Aspen Plus lacks built-in capabilities for detailed membrane cascade modeling. This repository provides a Python-based solution to generate split fractions for Aspen's SEP module.

## Repository structure
- `src/` Python scripts for Dehydration and Membrane modules.
- `Flowsheets/` schematic Representation of the membrane cascade.
- `Data/` Input and the Output data for the dehydration column and the membrane cascade.

## Usage
1. Install dependencies:
    - Numpy
    - Scipy
    - Pandas
    - Matplotlib
    - Jupyter Notebook

2. Run simulations:

