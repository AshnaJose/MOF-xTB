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
pip install ase pymatgen numpy matplotlib scipy pandas
```

You must also have:

**DFTB+** installed and accessible in your `$PATH`

**dp_dos** utility compiled and accessible

📁 Directory Structure

<pre>
project/
│
├── xTB_automated_workflow.py      # Workflow script
├── results_and_data.csv           # Generated results summary
├── input_cifs/                    # Your .cif files go here
└── save_directory/                # Output from each calculation
    └── <structure_name>/
        └── scf/
            ├── structure.gen
            ├── dftb_in.hsd
            ├── band.out
            ├── detailed.out
            ├── dos_total.dat
            ├── dftb.out
            ├── dftb.err
            └── _dp_dos.png
</pre>

⚙️ Usage

Edit and run the script with:

```bash
if __name__ == "__main__":
    batch_process_cifs("/path_to_folder_of_cifs/", "save_directory")
```

Replace:

`"/path_to_folder_of_cifs/"` with the directory containing your `.cif` files

`"save_directory"` with the desired output directory

Run the script:

```bash
python your_script.py
```
