# Machine Learning – MOF‑xTB

[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/AshnaJose/MOF-xTB)](https://github.com/AshnaJose/MOF-xTB/blob/main/LICENSE)

Machine learning tools and notebooks for analyzing MOF properties.

## 📂 Contents

- `data_analysis.ipynb` 
  Exploratory Data Analysis notebook to:
  - Inspect and visualize the MOF dataset
  - Compare xTB band gaps to reference DFT data
  - Prepare data for ML 

- `visualisation.ipynb` – produces key visual outputs such as:
  - Feature distribution histograms  
  - t-SNE plots for the dataset
 
- `training_and_testing.ipynb`
  - Load feature and target datasets (including Δ-learning targets)
  - Split data into training and testing sets 
  - Train a **XGBoost Regressor** on the **Δ-learning** target, as well as direct target.  
  - Evaluate model performance using metrics such as MAE and R².  
  - Visualize predicted vs. actual Δ-learning values with parity plots.  

