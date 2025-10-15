# MOF-xTB

# Overview

 The GFN1-xTB method is applied to compute band gaps of a dataset of Metal-Organic Frameworks and train ML Models for accurate band gap prediction.

 # MOF-xTB Workflow

A Python-based automated workflow for analyzing the electronic structure of Metal–Organic Frameworks (MOFs) using GFN1-xTB with DFTB+ is provided.

This code:
- Parses CIF files and converts them to `.gen` format for DFTB+
- Runs GFN1-xTB calculations (via DFTB+)
- Post-processes to extract the bandgap and density of states (DOS)

## 🚀 Features

- **Batch processing** of `.cif` structure files
- Automatic **generation of DFTB+ input files**
- Calculations using **GFN1-xTB method**
- **Density of States (DOS)** calculation using `dp_dos` and bandgap estimation 

## 📦 Requirements

- Python ≥ 3.7
- [DFTB+](https://www.dftbplus.org/)
- Python packages:
  - `ase`
  - `pymatgen`
  - `matplotlib`
  - `numpy`
  - `scipy`
  - `pandas`

 # Citation
 
Coming soon! :rocket:

Please refer to the following papers if you use these codes/data:

Ashna Jose, Aron Walsh. Accurate Band Gap Prediction in Porous Materials using $\Delta$-Learning (2025)
