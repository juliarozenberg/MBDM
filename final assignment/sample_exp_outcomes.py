import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import copy

from ema_workbench import (
    Model,
    Policy,
    ema_logging,
    SequentialEvaluator,
    MultiprocessingEvaluator,
)

from dike_model_function import DikeNetwork  # @UnresolvedImport
from problem_formulation import get_model_for_problem_formulation, sum_over, sum_over_time
dike_model, planning_steps = get_model_for_problem_formulation(3)

uncertainties = copy.deepcopy(dike_model.uncertainties)
levers = copy.deepcopy(dike_model.levers)

def get_do_nothing_dict():
    return {l.name: 0 for l in dike_model.levers}


# define the 'no policy'-policy
policies = [
    Policy(
        "policy 0",
        **dict(
            get_do_nothing_dict(),
            **{"0_RfR 0": 0, "1_RfR 0": 0, "2_RfR 0": 0}
        )
    ),
]

# pass the policies list to EMA workbench experiment runs
n_scenarios = 7500
 
#with MultiprocessingEvaluator(dike_model, n_processes=1) as evaluator:
#    results = evaluator.perform_experiments(n_scenarios, policies)

with SequentialEvaluator(dike_model) as evaluator:
    results = evaluator.perform_experiments(n_scenarios, policies)


# unpack the results
experiments, outcomes = results 

#save the outcomes to a csv file
experiments_policy=pd.DataFrame(experiments)
experiments_policy.to_csv('experiments(no policy)_10k.csv', index=False)
                          
outcomes_policy=pd.DataFrame(outcomes)
outcomes_policy.to_csv('outcomes(no policy)_10k.csv', index=False)