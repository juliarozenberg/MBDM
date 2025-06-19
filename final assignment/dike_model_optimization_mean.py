from ema_workbench import (
    Model,
    MultiprocessingEvaluator,
    ScalarOutcome,
    IntegerParameter,
    optimize,
    Scenario,
)
from ema_workbench.em_framework.optimization import EpsilonProgress
from ema_workbench.util import ema_logging

from problem_formulation import get_model_for_problem_formulation
import matplotlib.pyplot as plt
import seaborn as sns
import random
from ema_workbench.em_framework import sample_uncertainties
from ema_workbench import ScalarOutcome
from ema_workbench.em_framework.optimization import ArchiveLogger, EpsilonProgress
import multiprocessing 
import os
import numpy as np

# Optimization for mean outcomes
if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)
    seeds = [1,2,3,4,5]
    for seed in seeds:
        print(f"Running for seed {seed}")
        np.random.seed(seed)
        random.seed(seed)
        model, steps = get_model_for_problem_formulation(2)
        
        n_scenarios = 10
        scenarios = sample_uncertainties(model, n_scenarios)

        # Define robustness functions
        robustness_functions = [
            ScalarOutcome("Gelderland Expected Number of Deaths", function=np.mean, kind=ScalarOutcome.MINIMIZE),
            ScalarOutcome("Overijssel Expected Annual Damage", function=np.mean, kind=ScalarOutcome.MINIMIZE),
            ScalarOutcome("Overijssel Dike Investment Costs", function=np.mean, kind=ScalarOutcome.MINIMIZE),
            ScalarOutcome("Overijssel Expected Number of Deaths", function=np.mean, kind=ScalarOutcome.MINIMIZE),
            ScalarOutcome("RfR Total Costs", function=np.mean, kind=ScalarOutcome.MINIMIZE),
            ScalarOutcome("Expected Evacuation Costs", function=np.mean, kind=ScalarOutcome.MINIMIZE),
        ]
        # Using less pocessors to avoid overloading the system
        n_processes = multiprocessing.cpu_count() - 2
        print(f"Using {n_processes} out of {multiprocessing.cpu_count()} processors.")
        
        nfe = int(40000)
        
        # Create a directory to save results
        archive_dir = f"./archives_mean_seed_{seed}"
        os.makedirs(archive_dir, exist_ok=True)  # This creates the directory if it doesn't exist

        # Define convergence metrics
        convergence_metrics = [
            ArchiveLogger(
                f"./archives_mean_seed_{seed}",
                [l.name for l in model.levers],
                [o.name for o in robustness_functions],
                base_filename=f"robust_optimization_seed_{seed}.tar.gz",
            ),
            EpsilonProgress(),
        ]
        
        # Run the optimization
        with MultiprocessingEvaluator(model,n_processes=n_processes) as evaluator:
            results, convergence = evaluator.robust_optimize(
                robustness_functions,
                scenarios,
                nfe=nfe,
                epsilons=[0.1] * len(robustness_functions),
                convergence=convergence_metrics,
            )

        # Save results to a CSV file
        csv_path = os.path.join(archive_dir, f"results_seed_{seed}.csv")
        results.to_csv(csv_path, index=False)
        print(f"Results saved to {csv_path}")

        #Create and save convergence plot
        fig, ax1 = plt.subplots(ncols=1)
        ax1.plot(convergence.epsilon_progress)
        ax1.set_xlabel("nr. of generations")
        ax1.set_ylabel(r"$\epsilon$ progress")
        sns.despine()
        plot_filename = f"convergence_plot_seed_{seed}.png"
        fig.savefig(plot_filename, dpi=300, bbox_inches='tight')  
        plt.close(fig) 
        print(results)


