import os
import subprocess
from pathlib import Path
from ase.io import read, write
from ase.dft.kpoints import bandpath
from ase import Atoms
import shutil
import pymatgen
from pymatgen.core import Element
from pymatgen.ext.matproj import MPRester
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.symmetry.bandstructure import HighSymmKpath
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.ndimage import gaussian_filter1d
import pandas as pd


# Running the MOF-xTB workflow for a set of structures stored in .cif formats

def batch_process_cifs(cif_folder, output_folder):
    cif_files = list(Path(cif_folder).glob("*.cif"))
    print('Looking for cif files')
    if not cif_files:
        print(":x: No CIF files found.") 
        return
    output_root = Path(output_folder)
    output_root.mkdir(exist_ok=True)
    for cif in cif_files:
        try:
            print('Processing ', cif)
            mof_xtb_workflow(cif, output_root)
        except Exception as e:
            print(f":x: Error processing {cif.name}: {e}")
            

# Main workflow

def mof_xtb_workflow(cif_path, output_root):
    
    # Load CIF file
    atoms = read(cif_path)
    num_atoms = len(atoms)
    print('Number of atoms: ',num_atoms)
    name = cif_path.stem
    base_dir = output_root / name
    scf_dir = base_dir / "scf"
    for d in [scf_dir]:
        d.mkdir(parents=True, exist_ok=True)

    print('Creating .gen structure file')
    write(scf_dir / "structure.gen", atoms, format="gen")
    
    elements = sorted(set(atoms.get_chemical_symbols()))
    formula = atoms.get_chemical_formula()
    volume = atoms.get_volume()
    volume_per_atom = volume / len(atoms)
    
    # Write SCF input and run DFTB+ calculation
    print('Writing DFTB+ input file...')
    write_dftb_input_scf(elements, scf_dir)
    print('Running GFN1-xTB calculation...')
    run_dftb(scf_dir)
    
    bandout_file = scf_dir / "band.out"
    detailed_file = scf_dir / "detailed.out"
    dp_dos_output_file = scf_dir / "dos_total.dat"
    dp_dos_plot_file = scf_dir / f"{name}_dp_dos.png"
    results_csv = Path("results_and_data.csv")

    with open(dp_dos_output_file, 'w') as f:
        pass 

    if bandout_file.exists():
        print("Running dp_dos to generate DOS...")
        try:
            subprocess.run(["dp_dos", "-b", "0.02", str(bandout_file), str(dp_dos_output_file)])
            print("dp_dos completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f":x: dp_dos failed: {e}")

        # Compute bandgap 
        print("Computing bandgap:")
        vbm_dp, cbm_dp, gap_dp = compute_bandgap_from_dp_dos(dp_dos_output_file, detailed_file)
        print(f"vbm: {vbm_dp:.4f} eV")
        print(f"cbm: {cbm_dp:.4f} eV")
        print(f"Band gap: {gap_dp:.4f} eV")
        
        if dp_dos_output_file.exists():
            print("Plotting and saving density of states...")
            plot_dp_dos(dp_dos_output_file, detailed_file, output_path=dp_dos_plot_file, mof_name=name, bandgap=gap_dp)

        print('Writing results...')
        if gap_dp is not None:
            write_bandgap_csv(results_csv, name, formula, vbm_dp, cbm_dp, gap_dp, volume_per_atom,num_atoms)
            print('Results written successfully.')
            
    else:
        print(":warning: band.out not found for DOS generation.")
        

# Function to wrote the DFTB+ input file, dftb_in.hsd

def write_dftb_input_scf(elements, output_path):
    with open(output_path / "dftb_in.hsd", "w") as f:
        f.write("Geometry = GenFormat {\n  <<< \"structure.gen\"\n}\n")
        f.write("Hamiltonian = xTB {\n  Method = GFN1-xTB\n")
        f.write("  MaxAngularMomentum {\n")
        for el in elements:
            l = default_angular_momentum(el)
            f.write(f"    {el} = \"{l}\"\n")
        f.write("  }\n")
        f.write("KPointsAndWeights = SupercellFolding {\n")
        f.write("2 0 0\n 0 2 0\n 0 0 2\n 0.0 0.0 0.0 \n} \n")
        f.write("  }\n")
        f.write("Options { WriteDetailedXML = Yes }\n")
        f.write("ParserOptions { IgnoreUnprocessedNodes = Yes }\n")
        f.write("Analysis { CalculateForces = Yes }\n")


# Command to run DFTB+ calculation

def run_dftb(input_dir):
    subprocess.run(
        ["dftb+"],
        cwd=input_dir,
        stdout=open(input_dir / "dftb.out", "w"),
        stderr=open(input_dir / "dftb.err", "w"))
        

def default_angular_momentum(el):
    elem = Element(el)
    if elem.is_alkali or elem.is_alkaline:
        return "s"
    if elem.is_transition_metal:
        return "d"
    if elem.is_lanthanoid or elem.is_actinoid:
        return "f"
    if elem.Z <= 2:
        return "s"
    return "p"


def compute_bandgap_from_dp_dos(dos_file, detailed_out_path, threshold=1e-4):
    fermi_level = parse_fermi_level(detailed_out_path)
    print('Fermi level:', fermi_level)
    data = np.loadtxt(dos_file)
    energies = data[:, 0] - fermi_level
    dos = data[:, 1]

    occupied = energies[energies <= 0]
    dos_occ = dos[energies <= 0]
    unoccupied = energies[energies > 0]
    dos_unocc = dos[energies > 0]

    vbm = None
    cbm = None
    bandgap = None

    if np.any(dos_occ > threshold):
        vbm = occupied[dos_occ > threshold].max()
    if np.any(dos_unocc > threshold):
        cbm = unoccupied[dos_unocc > threshold].min()
    if vbm is not None and cbm is not None:
        bandgap = cbm - vbm

    return vbm, cbm, bandgap


def parse_fermi_level(detailed_out_path):
    """Extracts the Fermi level from the 'detailed.out'."""
    fermi_level = None
    with open(detailed_out_path, 'r') as f:
        for line in f:
            if "Fermi level:" in line:
                # Extract the Fermi level value in eV
                parts = line.split()
                fermi_level = float(parts[-2])  
                break
    if fermi_level is None:
        raise ValueError("Fermi level not found in the detailed.out file.")
    return fermi_level
    

def plot_dp_dos(dos_file, detailed_out_path, output_path, mof_name, bandgap):
    fermi_level = parse_fermi_level(detailed_out_path)
    data = np.loadtxt(dos_file)
    energies = data[:, 0] - fermi_level  # Shift to Fermi level
    dos = data[:, 1]
    plt.figure(figsize=(6, 5))
    plt.plot(energies, dos, label="DOS", color='blue', linewidth=0.7)
    plt.axvline(0, color='red', linestyle='--', linewidth=1, label="Fermi Level")
    x_pos = -10 + 0.025 * 20  # 3% from left edge
    y_pos = max(dos)*1.01  # 97% of max height (near top)

    if mof_name is not None and bandgap is not None:
        annotation_text = f"E$_g$ ({mof_name}) = {bandgap:.2f} eV"
        plt.text(x_pos, y_pos, annotation_text, verticalalignment='top', horizontalalignment='left', fontsize=10)
    plt.xlabel("Energy (eV)")
    plt.ylabel("Density of States")
    plt.grid(True)
    plt.legend()
    #plt.title("Density of States")
    plt.xlim(-10,10)
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300)
        print(f"dp_dos plot saved to {output_path}")
    else:
        plt.show()


def write_bandgap_csv(csv_path, structure_name, formula, vbm, cbm, gap, volume_per_atom,num_atoms):
    file_exists = csv_path.exists()
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Structure", "Formula", "vbm (eV)", "cbm (eV)", "Band Gap (eV)",
                             "Classification", "Volume/Atom (Å³)","num_atoms"])
        classification = "Metal" if gap is None or gap < 0.01 else "Semiconductor" if gap < 2.0 else "Insulator"
        writer.writerow([structure_name, formula, f"{vbm:.4f}", f"{cbm:.4f}", f"{gap:.4f}",
                         classification, f"{volume_per_atom:.4f}",num_atoms])
        
            
# Run the workflow for a batch of structures

if __name__ == "__main__":
    batch_process_cifs("/path_to_folder_of_cifs/", "save_directory")
