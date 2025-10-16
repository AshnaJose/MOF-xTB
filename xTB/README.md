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
