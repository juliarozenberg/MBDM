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


if __name__ == "__main__":
    import numpy as np
    ema_logging.log_to_stderr(ema_logging.INFO)
    seeds = [0, 1, 2, 3, 4]
    for seed in seeds:
        print(f"Running for seed {seed}")
        np.random.seed(seed)
        random.seed(seed)
        model, steps = get_model_for_problem_formulation(2)

        from ema_workbench.em_framework import sample_uncertainties
        n_scenarios = 100
        scenarios = sample_uncertainties(model, n_scenarios)

        from ema_workbench import ScalarOutcome


        robustness_functions = [
            ScalarOutcome("Gelderland Expected Number of Deaths", function=lambda x: np.percentile(x, 90), kind=ScalarOutcome.MINIMIZE),
            ScalarOutcome("Overijssel Expected Annual Damage", function=lambda x: np.percentile(x, 90), kind=ScalarOutcome.MINIMIZE),
            ScalarOutcome("Overijssel Dike Investment Costs", function=lambda x: np.percentile(x, 90), kind=ScalarOutcome.MINIMIZE),
            ScalarOutcome("Overijssel Expected Number of Deaths", function=lambda x: np.percentile(x, 90), kind=ScalarOutcome.MINIMIZE),
            ScalarOutcome("RfR Total Costs", function=lambda x: np.percentile(x, 90), kind=ScalarOutcome.MINIMIZE),
            ScalarOutcome("Expected Evacuation Costs", function=lambda x: np.percentile(x, 90), kind=ScalarOutcome.MINIMIZE),
        ]

        from ema_workbench.em_framework.optimization import ArchiveLogger, EpsilonProgress


        nfe = int(20000)
        import os

        archive_dir = f"./archives_seed_{seed}"
        os.makedirs(archive_dir, exist_ok=True)  # This creates the directory if it doesn't exist

        convergence_metrics = [
            ArchiveLogger(
                f"./archives_seed_{seed}",
                [l.name for l in model.levers],
                [o.name for o in robustness_functions],
                base_filename=f"robust_optimization_seed_{seed}.tar.gz",
            ),
            EpsilonProgress(),
        ]

        with MultiprocessingEvaluator(model) as evaluator:
            results, convergence = evaluator.robust_optimize(
                robustness_functions,
                scenarios,
                nfe=nfe,
                epsilons=[0.1] * len(robustness_functions),
                convergence=convergence_metrics,
            )




        #fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True)
        fig, ax1 = plt.subplots(ncols=1)
        ax1.plot(convergence.epsilon_progress)
        ax1.set_xlabel("nr. of generations")
        ax1.set_ylabel(r"$\epsilon$ progress")
        sns.despine()
        plot_filename = f"convergence_plot_seed_{seed}.png"
        fig.savefig(plot_filename, dpi=300, bbox_inches='tight')  # Save with high resolution
        plt.close(fig)  # Close the figure to free up memory
        print(results)


