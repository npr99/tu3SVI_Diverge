# SVI Analysis Paper: Comparative Vulnerability Index Study

## Overview

This project conducts a comprehensive comparative analysis of Social Vulnerability Index (SVI) methodologies across Southeast Texas. It examines how three different SVI implementations rank census tracts and block groups by social vulnerability, using 2020 census data:

- **CDC ATSDR SVI** — Official CDC social vulnerability index
- **HRRC SVI** — Regional approach from Texas Planning Atlas (texasatlas.arch.tamu.edu)
- **SVInsight SVI** — Academic implementation from UT Preisser Lab

The analysis includes variable concordance matrices, correlation studies, scatter plot visualizations, margins of error, and geographic mapping of study sites in Southeast Texas (Galveston, Jefferson, Orange, Chambers, and Liberty counties).

---

## Quick Start with GitHub Codespace

### Option 1: One-Click Launch
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/)

### Option 2: Manual Setup
1. Go to your GitHub repository
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait for the environment to build (1–2 minutes)
4. Once loaded, you'll have:
   - Python 3.10 with all dependencies pre-installed
   - Jupyter server ready to run
   - All data files accessible
   - VS Code with Python, Jupyter, and Pylance extensions

### Next Steps in Codespace
1. Open the Explorer panel (Ctrl+Shift+E or Cmd+Shift+E)
2. Navigate to the `Posted/` or `WorkNPR/` folder
3. Open any `.ipynb` notebook file
4. Select "Jupyter" when prompted for the kernel
5. Run cells with Shift+Enter or click the play button

---

## Project Structure

```
.
├── SourceData/                           # Raw data files and setup scripts
│   ├── tu3svi2_0bv1_sourcedatautility_*  # Utility functions for data standardization
│   ├── texasatlas_arch_tamu_edu/         # HRRC SVI data from Texas Atlas
│   ├── UT_Preisser_SVI/                  # SVInsight data from UT Lab
│   ├── www_atsdr_cdc_gov_placeandhealth_svi/  # CDC ATSDR SVI data
│   └── www2_census_gov/                  # 2020 Census geographic files
│
├── Posted/                               # Finalized analysis notebooks & outputs
│   ├── tu3svi4_2av4_SVIoptions_*         # SVI methodology comparison options
│   ├── tu3svi4_6av1_Table1_*             # Variable comparison table
│   ├── tu3svi4_6bv2_Table2_*             # Correlation analysis table
│   ├── tu3svi4_6bv3_ScatterFigures_*     # Correlation scatter plots
│   ├── tu3svi4_6cv3_Phase1Text_*         # Phase 1 analysis narrative
│   ├── tu3svi4_6dv2_Phase2Text_*         # Phase 2 analysis narrative
│   ├── tu3svi4_6ev3_TablesFigures_*      # Comprehensive tables & figures
│   ├── tu3svi4_6fv2_Phase1MOE_*          # Margin of error calculations
│   └── tu3svi4_6gv1_MapSites_*           # Geographic mapping of study sites
│
├── WorkNPR/                              # Working/development notebooks
│   └── [Same files as Posted/ during development]
│
├── Admin/                                # Administrative files & images
├── Readings/                             # Literature and references
├── Text/                                 # Project documentation
│
├── requirements.txt                      # Python package dependencies (pip)
├── environment.yml                       # Alternative Conda environment spec
├── .devcontainer/devcontainer.json       # GitHub Codespace configuration
├── .gitignore                            # Git exclusion rules
└── README.md                             # This file
```

---

## Data Sources

### 1. CDC ATSDR Social Vulnerability Index
- **File**: `CDC_2020_TX_Tract_2023-11-09.csv`
- **Coverage**: Texas census tracts (2020)
- **Source**: https://www.atsdr.cdc.gov/placeandhealth/svi/
- **Variables**: Composite SVI + four themes (socioeconomic, household composition, minority status, housing type)

### 2. HRRC SVI (Texas Planning Atlas)
- **Files**: `HRRC_2020_TX_Tract_*.csv`, `HRRC_2020_TX_BG_*.csv`
- **Coverage**: Texas census tracts and block groups (2020)
- **Source**: https://texasatlas.arch.tamu.edu/
- **Variables**: Custom vulnerability indicators developed by Houston Regional Research Collaborative

### 3. SVInsight (UT Preisser Lab)
- **Data**: Installed from Python package or local CSV exports
- **Coverage**: Texas census tracts and block groups (2020)
- **Source**: https://mdp0023.github.io/SVInsight/
- **Variables**: UT-developed social vulnerability framework

### Data Dictionary
- File: `tu3svi2_0av3_SVIdatadictionary_2025-04-08.xlsx`
- Maps variable names across all three SVI implementations for direct comparison

---

## Notebook Guide

### Setup Notebooks (SourceData/)
Run these first to understand data transformation:

| Notebook | Purpose |
|----------|---------|
| `tu3svi2_2av3_SetupUT_*` | Load and harmonize SVInsight data |
| `tu3svi2_2bv2_SetupCDC_*` | Load and harmonize CDC SVI data |
| `tu3svi2_2cv3_SetupHRRC_*` | Load and harmonize HRRC SVI data |

### Analysis Notebooks (Posted/WorkNPR/)
Run in this order for complete analysis:

| Notebook | Purpose | Output |
|----------|---------|--------|
| `tu3svi4_2av4_SVIoptions_*` | Compare SVI methodology options | Analysis summary |
| `tu3svi4_6av1_Table1_*` | Generate variable comparison matrix | CSV table |
| `tu3svi4_6bv2_Table2_*` | Compute correlation between methods | CSV correlation matrix |
| `tu3svi4_6bv3_ScatterFigures_*` | Visualize concordance via scatter plots | PNG figures (600 DPI) |
| `tu3svi4_6cv3_Phase1Text_*` | Phase 1 narrative analysis | Formatted text output |
| `tu3svi4_6dv2_Phase2Text_*` | Phase 2 narrative analysis | Formatted text output |
| `tu3svi4_6ev3_TablesFigures_*` | Compile final tables and figures | Combined output |
| `tu3svi4_6fv2_Phase1MOE_*` | Calculate margins of error | MOE statistics |
| `tu3svi4_6gv1_MapSites_*` | Geographic mapping of study sites | Interactive/static maps |

---

## Local Setup (Without Codespace)

### Prerequisites
- Python 3.8 or higher (3.10+ recommended)
- pip or conda package manager

### Installation

**Option 1: Using pip (Recommended)**
```bash
# Clone or download the repository
cd path/to/DesignSafe-Archive

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter notebook
```

**Option 2: Using Conda**
```bash
# Create environment from file
conda env create -f environment.yml
conda activate svi-analysis

# Start Jupyter
jupyter notebook
```

### Verify Installation
Open a Jupyter notebook cell and run:
```python
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
print("✓ All dependencies installed successfully!")
```

---

## Key Features & Utilities

### Data Standardization
The utility script `tu3svi2_0bv1_sourcedatautility_*.py` provides helper functions:
- `update_varnames()` — Standardizes variable names across SVI datasets
- `quartileSVI()` — Computes percentile ranks for SVI normalization
- Geographic ID utilities for census tract/block group matching

### Data Formats
- **Input**: CSV files from three SVI sources
- **Processing**: pandas DataFrames and GeoPandas GeoDataFrames
- **Output**: CSV tables, PNG figures (600 DPI), Excel exports

### Geographic Scope
**Study Area**: Southeast Texas counties
- Galveston County (48245)
- Jefferson County (48361)
- Orange County (48199)
- Chambers County (48241)
- Liberty County (48351)

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'geopandas'"
**Solution**: Ensure requirements.txt is installed:
```bash
pip install -r requirements.txt
```

### Issue: "Relative path not found" when running notebooks
**Solution**: Make sure you're running notebooks from the correct directory. Notebooks use relative paths like `../SourceData/...` that assume the working directory is the notebook's parent folder. In Jupyter, this is usually automatic, but verify with:
```python
import os
print(os.getcwd())  # Should show the DesignSafe-Archive directory
```

### Issue: Jupyter kernel not found in Codespace
**Solution**: The dev container automatically installs the kernel. If issues persist:
1. Click **Select Kernel** in the notebook toolbar
2. Choose **Python 3.10** or the Python environment shown
3. If unavailable, restart the container (Codespaces menu → Rebuild container)

### Issue: Data files not accessible
**Solution**: Verify the folder structure matches the repository:
- All SourceData files should be in `./SourceData/`
- All notebooks should be able to reference them with `../SourceData/...`
- In Codespace, the working directory is set to the repository root automatically

### Issue: Slow notebook performance with large datasets
**Solution**: Ensure pyarrow is installed for better CSV I/O performance:
```bash
pip install --upgrade pyarrow
```

---

## Environment Variables & Configuration

### Jupyter Configuration (Optional)
For Codespace, Jupyter automatically starts on port 8888 and is configured in `.devcontainer/devcontainer.json`. To customize:

1. Generate Jupyter config (local setup only):
   ```bash
   jupyter notebook --generate-config
   ```
2. Edit `~/.jupyter/jupyter_notebook_config.py` for custom settings

### VS Code Extensions
Codespace includes:
- **Python** — Code editing, debugging, linting
- **Jupyter** — Notebook execution and visualization
- **Pylance** — Advanced Python type checking
- **GitHub Copilot** — AI-assisted coding (if licensed)

---

## For Team Members

### Getting Started
1. **First time**: Open in Codespace, wait 1–2 minutes for environment setup
2. **Open a notebook** from the `Posted/` folder
3. **Select kernel** when prompted (should be Python 3.10 auto-detected)
4. **Run a cell** to test (Shift+Enter)

### Contributing Changes
- Edit notebooks in the `WorkNPR/` folder for development
- Once finalized, copy to `Posted/` folder with updated version date
- Commit with descriptive messages (e.g., "Update Table 1 with 2026 data")

### File Naming Convention
`tu3svi[type]_[version]_[description]_[date].ipynb`
- `type`: 2 = setup, 4 = analysis
- `version`: Format like `6av1` (incrementing letters for iterations)
- `description`: Brief description of analysis
- `date`: YYYY-MM-DD format

Example: `tu3svi4_6cv3_Phase1Text_2026-02-15.ipynb`

---

## Performance Notes

### Typical Execution Times (Codespace)
- **Setup notebooks** (load & merge data): 30–60 seconds
- **Table generation** (Table 1, Table 2): 10–30 seconds
- **Scatter plots** (visualization): 15–45 seconds
- **Map generation**: 1–2 minutes (depends on complexity)

### Data Size
- All source data: < 10 MB (fits comfortably in Codespace)
- Processed data: Typically 20–50 MB during analysis (temporary)
- Output files: < 1 MB per notebook (CSVs, PNGs)

---

## References & Additional Resources

### SVI Methodology Papers
- CDC ATSDR: https://www.atsdr.cdc.gov/placeandhealth/svi/
- Texas Planning Atlas: https://texasatlas.arch.tamu.edu/
- SVInsight UT Lab: https://mdp0023.github.io/SVInsight/

### Data Sources
- 2020 Census Data: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
- Study Area: Southeast Texas Region

---

## Questions or Issues?

For questions about:
- **Analysis methods**: See individual notebook documentation and markdown cells
- **Data sources**: Check the corresponding `_ReadMe_*.txt` file in each SourceData subfolder
- **Codespace setup**: See the Troubleshooting section above
- **GitHub/Git issues**: Refer to GitHub Codespaces documentation

---

**Last Updated**: April 2026  
**Project Version**: tu3svi4  
**Python Version Required**: 3.8+  
**Codespace Support**: ✓ Full support via `.devcontainer/devcontainer.json`
