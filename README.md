# GRA_TriLevel_TraitCorrelation
Implements computationally efficient weighted Grey Relational Analysis (GRA) with AHP-optimized weights to automate optimal model selection for complex phenotypic traits evaluation.

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📦 Installation
```bash
git clone https://github.com/ShuangWu221/GRA_TriLevel_TraitCorrelation.git
cd GRA_TriLevel_TraitCorrelation
pip install -r requirements.txt
```

## 🚀 Usage
```bash
python GRA_TriLevel_TraitCorrelation.py \
[input_phenotype_data.xlsx] \
[output_dir] \
[weight_config.txt] \
--num_indices=[n_significant_indicators] \
--r=[distinguishing_coefficient] (range:0-1, default=0.5) \
--category_1=[n_category_1_samples] \
--category_2=[n_category_2_samples]
```
The GRA_TriLevel_TraitCorrelation.py script requires: (1) Phenotype dataset (TraitData.xlsx) in standard Excel format containing sample IDs and normalized dimensionless values (e.g., Z-score) for all observed traits; (2) Weight configuration file (weight.txt) as space-delimited text listing ordered weights (∑weights=1) for weighted GRA; (3) --num_indices specifying OPLS-DA derived discriminatory variables count; (4) --r (distinguishing coefficient, range: 0-1, default=0.5) controlling GRA sensitivity; (5) --category_1 indicating sample size of the first phenotypic category, and --category_2 for the second category, requiring summed counts match total dataset size. Prerequisites include numpy≥1.20, pandas≥1.3, and matplotlib≥3.5 installations.


## 🔍 Workflow
1. **Data Ingestion**  
   - Reads Excel trait data → Converts to NumPy arrays
2. **Ideotype Generation**  
   - Generates 8,192 binary ideotypes (13-bit combinations)
3. **Trait Correlation**  
   - Computes weighted grey relational grades (GRA + AHP)
4. **Germplasm Classification**  
   - Tier Ⅰ: Category-1  
   - Tier Ⅱ: Intermediate-type  
   - Tier Ⅲ: Category-2 
5. **Model Validation**  
   - Accuracy = Correct classifications / Total samples
6. **Optimal Model Selection**  
   - Identifies highest-accuracy variable combination

## 📂 File Structure
```
├── GRA_TriLevel_TraitCorrelation.py  # Main script
├── data/                             # Example datasets
└── LICENSE
```

## 📊 Sample Output
```text
[RESULTS]
[0 1 1 1 0 0 1 0 0 0 0 0 0]	0.830357143
[0 0 0 0 0 0 1 0 0 0 1 1 0]	0.821428571
[0 0 0 0 0 0 0 0 1 0 1 1 0]	0.803571429
……total 8192 rows
```
Optimal ideotype: 0 1 1 1 0 0 1 0 0 0 0 0 0
Classification accuracy: 83.04%

## 📜 License
Distributed under the MIT License. See [LICENSE](LICENSE) for details.
