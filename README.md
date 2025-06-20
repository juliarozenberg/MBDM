Dike Model Network analysis Waterboard Groot Salland - Model Based Descision Making (EPA141A)

Created by:
- Emile Wouters
- Julia Rozenberg
- Floris van Amersfoort


This respository contains a decision-support toolkit for evaluating flood protection strategies along the IJssel River. This project applies exploratory modeling, scenario discovery, and multi-objective optimization to identify policies under deep uncertainty. The conducted analyses are mainly conducted using the EMA workbench. 

---

# Project Overview

This project supports the Groot-Salland Water Board in identifying flood protection policies that perform well across a wide range of future scenarios. It combines open exploration, scenario discovery, and a directed search using evolutionary optimization.

Key features include:

- Simulations of river floods on different locations over a long period, with a wide range of uncertainties and possible policy levers
- Initial open explorations of experiments
- Scenario discovery using PRIM and dimensional stacking
- Sensitivity analysis of conducted experiments
- Robust optimization using a Multi-Objective Evolutionary Algorithm (MORO)
- Regret-based policy robustness analysis

---

# Repository structure

> Requirements.txt

Contains a list with the libaries/dependencies which have to be installed to use the code in the repository


> Map: final assignment (MBDM > final assignment)

🔧 Model Execution                  File	Description
- dike_model_function.py	        Specifies the model structure
- dike_model_simulation	          Simulating the flood model
- funs_dikes.py	                  Specifies functions for the specific dikes in the model
- funs_economy.py                 Specifies economic functions
- funs_generate_network.py        Creates the network which is used as a base of the simulation model
- funs_hydrostat.py               Specifies water related functions
- problem_formulation.py          Specify which uncertainties and policy levers are used in the simulation, and which data you want to collect during a simulation run

Analysis & Post-processing
File	                            Descriptopn
Dimensional_Stacking.ipynb        Notebook containing all the steps to perform dimensional stacking, used in the open exploration phase
Feature Scoring.ipynb             Notebook containing all the steps to perform Feature Scoring, used in the open exploration phase
MORO_merge_and_filter.ipynb       Notebook containing all steps to reduce the MORO results to one small promising policy set, fit for further analysis
PRIM_no_policy.ipynb              Notebook containing all the steps to a Prime Induction Method on the no policy exploration sample, part of open exploration
PRIM_policy.ipynb                 Notebook containing all the steps to a Prime Induction Method on the policy exploration sample, part of open exploration
PRIM_DS.ipynb                     Notebook containing all the steps to a Prime Induction Method on the final promising policy set, part of direct search
Problem Formulations.ipynb        Notebook containing steps to create experiment samples with the model, based on a specified problem formulation
Robustness_Analysis.ipynb         Notebook containing all the steps to a robustness analysis using regret on the policy exploration sample, part of direct search
Sobol Sensitivity Analysis.ipynb  Notebook containing all the steps to perform a sobol sensitivity analysis, part of open exploration
dike_model_optimization.py        Python file which forms a base to perform policy optimization experiments with the simulation model 
dike_model_optimization_90.py     Python file to conduct a MORO with the simulation model using the specified problem formulation(2). p90-based evalution. 
dike_model_optimization_mean.py     Python file to conduct a MORO with the simulation model using the specified problem formulation(2). mean-based evalution. 



Data Files

File                              Description
experiments(no policy).csv        Experiments sample created in Problem Formulations.ipynb without policy levers, input for open exploration analyses
experiments(no policy)_10k.csv    Larger experiments sample created in Problem Formulations.ipynb without policy levers, input dimensional stacking
experiments(policy).csv           Experiments sample created in Problem Formulations.ipynb with policy levers, input for open exploration analyses
experiments.csv                   Experiments sample created in MORO_merge_and_filter.ipynb with promising policies, input for robustness analysis and PRIM_DS
outcomes(no policy).csv           Outcomes of experiments created in Problem Formulations.ipynb without policy levers, input for open exploration analyses
outcomes(no policy)_10k.csv       Outcomes of larger experiments sample created in Problem Formulations.ipynb without policy levers, input dimensional stacking
outcomes(policy).csv              Outcomes of experiments created in Problem Formulations.ipynb with policy levers, input for open exploration analyses

Map: archives_90_seed_N (MBDM > final asignment > archives_90_seed_N)

Contains the resulst of 90th percentile based MORO's, of the two respective seed runs. These results are used as input for MORO_merge_and_filter.ipynb. These maps are created in the dike_model_optimization_90.py file if they don't exist yet.


Map: archives_mean_seed_N (MBDM > final asignment > archives_mean_seed_N)

Contains the resulst of mean-based MORO's, of the two respective seed runs. These results are used as input for MORO_merge_and_filter.ipynb. These maps are created in the dike_model_optimization_mean.py file if they don't exist yet.


Map: data (MBDM > final aisgnment > data)

Contains all necessary input files to create and simulate the model


Map: results (MBDM > final asignment > data)

Contains the results of the conducted experiments with the finale promising policy sample. The contents are an output of the MORO_merge_and_filter notebook. The map is created in this notebook if it doesn't exist yet. 


Research conducted with the dike model and repository

The conducted research project with this repository consisted of a few general phases:
- (pre research: the simulation model was already created before)
- Specify problem formulation of interest in the problem_formulation.py. We made use of PF_2. This PF could reflect the objectives of Waterboard Groot Salland best.
- Create first experiment samples, using the Problem Formulations notebook.
- Conduct the Open Exploration analyses (initial exploration, scenario discovery consisting of PRIM and Dimensional stacking, feature scoring and Sobal Sensitivity Analysis)
- Conduct the MORO's (both mean-based and p90-based, both with two different seeds). This can take a long time/could be done using a super computer!
- Analyse and filter the MORO results, in the MORO_merge_and_filter notebook. This included pareto filtering, k-means clustering and creating new experiments with more scenarios.
- Conduct a robustness analysis with the saved policy set. Hereby, mean- and max-regret analyses were conducted.
- A second round of scenario discovery using PRIMA, based on the experiments created in the MORO_merge_and_filter notebook.




# How to Run

1. **Clone the repo**
   ```bash
   git clone https://github.com/juliarozenberg/MBDM.git
   cd MBDM

2. Install dependencies

bash
pip install -r requirements.txt



