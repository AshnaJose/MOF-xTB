# MOF-xTB Workflow

This repository provides a Python-based workflow for running **GFN1-xTB** electronic structure calculations on a batch of **MOF (Metal–Organic Framework)** structures in `.cif` format using **DFTB+**. 

## 🔍 Features

- Batch processing of `.cif` structure files
- Automatic generation of DFTB+ input files (`dftb_in.hsd`)
- Runs **GFN1-xTB** calculations using DFTB+
- Computes and plots total Density of States (DOS)
- Extracts Fermi level, CBM, VBM, and calculates band gap
- Saves results with structure metadata
- Saves high-resolution DOS plots

## 🧪 Dependencies

Install the required Python libraries before running the workflow:

```bash
pip install ase pymatgen numpy matplotlib scipy pandas```

You must also have:

DFTB+ installed and accessible in your $PATH

dp_dos utility compiled and accessible (used for DOS processing)
